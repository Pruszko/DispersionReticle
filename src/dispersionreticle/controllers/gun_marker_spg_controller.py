import BigWorld, BattleReplay
from AvatarInputHandler.gun_marker_ctrl import _SPGGunMarkerController

from dispersionreticle.utils import version


# gun_marker_ctrl
class NewSPGGunMarkerController(_SPGGunMarkerController):
    def _update(self):
        pos3d, vel3d, gravity3d = self._getCurrentShotInfo()
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            self._SPGGunMarkerController__updateRelaxTime()
        self._updateDispersionData()

        newSize = self._size
        if version.IS_X0_6:
            newSize *= 0.6

        self._dataProvider.update(pos3d, vel3d, gravity3d, newSize)


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
