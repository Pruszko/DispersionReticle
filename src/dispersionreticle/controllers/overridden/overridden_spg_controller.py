import BattleReplay, Math
from AvatarInputHandler.gun_marker_ctrl import _SPGGunMarkerController, _MARKER_FLAG, _MARKER_TYPE

from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.utils import isClientWG


# gun_marker_ctrl
class OverriddenSPGGunMarkerController(_SPGGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, isServer, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(OverriddenSPGGunMarkerController, self).__init__(gunMakerType, dataProvider, enabledFlag=enabledFlag)
        self._isServer = isServer
        self._evaluatedSize = 0

    # WG specific
    # Lesta specific
    #
    # differences in method signatures and code
    def update(self, *args, **kwargs):
        if isClientWG():
            self.wg_update(*args, **kwargs)
        else:
            self.lesta_update(*args, **kwargs)

    def wg_update(self, markerType, gunMarkerInfo, supportMarkersInfo, relaxTime):
        from VehicleGunRotator import GunMarkerInfo
        gunMarkerInfo = gunMarkerInfo  # type: GunMarkerInfo

        super(_SPGGunMarkerController, self).update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        positionMatrix = Math.createTranslationMatrix(gunMarkerInfo.position)
        self._updateMatrixProvider(positionMatrix, relaxTime)
        self._size = gunMarkerInfo.size + gunMarkerInfo.sizeOffset

        sizeMultiplier = g_configParams.reticleSizeMultiplier()
        self._evaluatedSize = self._interceptSize(self._size, gunMarkerInfo.position) * sizeMultiplier

        self._update()

    def lesta_update(self, markerType, position, direction, size, relaxTime, collData):
        super(_SPGGunMarkerController, self).update(markerType, position, direction, size, relaxTime, collData)
        positionMatrix = Math.createTranslationMatrix(position)
        self._updateMatrixProvider(positionMatrix, relaxTime)
        self._size = size[0]

        sizeMultiplier = g_configParams.reticleSizeMultiplier()
        self._evaluatedSize = self._interceptSize(self._size, position) * sizeMultiplier

        self._update()

    def _update(self):
        pos3d, vel3d, gravity3d = self._getCurrentShotInfo()
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            self._SPGGunMarkerController__updateRelaxTime()
        self._updateDispersionData()

        size = self._evaluatedSize

        self._dataProvider.update(pos3d, vel3d, gravity3d, size)
        self._interceptPostUpdate(size)

    def _updateDispersionData(self):
        dispersionAngle = self._gunRotator.dispersionAngle

        dispersionAngle = self._interceptReplayLogic(dispersionAngle)
        dispersionAngle = self._interceptAngle(dispersionAngle)

        self._dataProvider.setupConicDispersion(dispersionAngle)

    def isClientController(self):
        return not self._isServer

    def isServerController(self):
        return self._isServer

    def _interceptSize(self, size, pos):
        return size

    def _interceptPostUpdate(self, size):
        pass

    def _interceptReplayLogic(self, dispersionAngle):
        isServerAim = self._gunMarkerType == _MARKER_TYPE.SERVER
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            d, s = replayCtrl.getSPGGunMarkerParams()
            if d != -1.0 and s != -1.0:
                dispersionAngle = d
        elif replayCtrl.isRecording:
            # IMPORTANT
            # when both client-side and server-side reticles are enabled
            # we MUST write only server-side data, because
            # VehicleGunRotator in that state writes server data to replays
            if self._areBothModesEnabled():
                if replayCtrl.isServerAim and isServerAim:
                    replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)
            else:
                # update is always done for all reticles,
                # so we can use any reticle to write data to replay
                # but for simplicity, use client reticle
                if not isServerAim:
                    replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)

        return dispersionAngle

    def _interceptAngle(self, dispersionAngle):
        return dispersionAngle

    def _isAnyModeEnabled(self):
        return self._isClientModeEnabled() or self._isServerModeEnabled()

    def _areBothModesEnabled(self):
        return self._isClientModeEnabled() and self._isServerModeEnabled()

    def _isClientModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED

    def _isServerModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED
