import BigWorld, BattleReplay, Math
from AvatarInputHandler.gun_marker_ctrl import _SPGGunMarkerController, _MARKER_FLAG, _MARKER_TYPE

from dispersionreticle.settings.config_param import g_configParams


# gun_marker_ctrl
class OverriddenSPGGunMarkerController(_SPGGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, isServer, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(OverriddenSPGGunMarkerController, self).__init__(gunMakerType, dataProvider, enabledFlag=enabledFlag)
        self._isServer = isServer
        self._evaluatedSize = 0

    def update(self, markerType, position, direction, size, relaxTime, collData):
        super(_SPGGunMarkerController, self).update(markerType, position, direction, size, relaxTime, collData)
        positionMatrix = Math.createTranslationMatrix(position)
        self._updateMatrixProvider(positionMatrix, relaxTime)
        self._size = size[0]

        sizeMultiplier = g_configParams.reticleSizeMultiplier()
        self._evaluatedSize = self._interceptSize(self._size, position, direction, relaxTime, collData) * sizeMultiplier

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

    def isServerController(self):
        return self._isServer

    def _interceptSize(self, size, pos, direction, relaxTime, collData):
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
            if replayCtrl.isServerAim and isServerAim:
                replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)
            elif not isServerAim:
                replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)

        return dispersionAngle

    def _interceptAngle(self, dispersionAngle):
        return dispersionAngle
