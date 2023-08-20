import BigWorld
from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.standard.standard_spg_controller import OverriddenSPGGunMarkerController


# gun_marker_ctrl
class DispersionSPGGunMarkerController(OverriddenSPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(DispersionSPGGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                               reticle.getSpgDataProvider(),
                                                               enabledFlag=enabledFlag)

    def _updateDispersionData(self):
        # dispersionAngle = self._gunRotator.dispersionAngle
        dispersionAngle = getFocusedDispersionAngle()

        # here we avoid replay-specific code, it is handled by vanilla controllers
        # even if their markers may not be present

        self._dataProvider.setupConicDispersion(dispersionAngle)


def getFocusedDispersionAngle():
    playerAvatar = BigWorld.player()
    vehicleDesc = playerAvatar._PlayerAvatar__getDetailedVehicleDescriptor()

    # gun dispersion per 1m unit
    shotDispersionAngle = vehicleDesc.gun.shotDispersionAngle

    # multiplier that accounts crew, food, etc.
    # PlayerAvatar -> getOwnVehicleShotDispersionAngle
    #   aimingInfo[0] = aimingStartTime
    #   aimingInfo[1] = aimingStartFactor
    #   aimingInfo[2] = multFactor
    #   aimingInfo[3] = gunShotDispersionFactorsTurretRotation
    #   aimingInfo[4] = chassisShotDispersionFactorsMovement
    #   aimingInfo[5] = chassisShotDispersionFactorsRotation
    #   aimingInfo[6] = aimingTime
    shotDispMultiplierFactor = playerAvatar._PlayerAvatar__aimingInfo[2]

    # just return actual angle for conic dispersion
    return shotDispersionAngle * shotDispMultiplierFactor
