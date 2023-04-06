import BigWorld, BattleReplay
from AvatarInputHandler.gun_marker_ctrl import _SPGGunMarkerController, _MARKER_FLAG, _MARKER_TYPE

from dispersionreticle.settings.config import g_config


# gun_marker_ctrl
class NewSPGGunMarkerController(_SPGGunMarkerController):
    def __init__(self, gunMakerType, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED, isMainReticle=True):
        super(NewSPGGunMarkerController, self).__init__(gunMakerType, dataProvider, enabledFlag=enabledFlag)
        self.__isMainReticle = isMainReticle
        self.__serverDispersionAngle = None

    def _update(self):
        pos3d, vel3d, gravity3d = self._getCurrentShotInfo()
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            self._SPGGunMarkerController__updateRelaxTime()
        self._updateDispersionData()

        newSize = self._size * g_config.getReticleSizeMultiplier()

        self._dataProvider.update(pos3d, vel3d, gravity3d, newSize)

    def _updateDispersionData(self):
        dispersionAngle = self._gunRotator.dispersionAngle
        if self.__serverDispersionAngle is not None:
            dispersionAngle = self.__serverDispersionAngle

        # avoid replays if not main reticle
        if self.__isMainReticle:
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

        self._dataProvider.setupConicDispersion(dispersionAngle)

    def setServerDispersionAngle(self, serverDispersionAngle):
        self.__serverDispersionAngle = serverDispersionAngle


# gun_marker_ctrl
class FocusSPGGunMarkerController(_SPGGunMarkerController):
    def _updateDispersionData(self):
        # dispersionAngle = self._gunRotator.dispersionAngle
        dispersionAngle = getFocusedDispersionAngle()

        # here we avoid replay-specific code, it is handled by vanilla controllers

        self._dataProvider.setupConicDispersion(dispersionAngle)


def getFocusedDispersionAngle():
    playerAvatar = BigWorld.player()
    vehicleDesc = playerAvatar._PlayerAvatar__getDetailedVehicleDescriptor()

    # gun dispersion per 1m unit
    shotDispersionAngle = vehicleDesc.gun.shotDispersionAngle

    # multiplier that accounts crew, food, etc.
    shotDispMultiplierFactor = playerAvatar._PlayerAvatar__aimingInfo[2]

    # just return actual angle for conic dispersion
    return shotDispersionAngle * shotDispMultiplierFactor
