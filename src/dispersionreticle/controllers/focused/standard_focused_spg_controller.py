import BigWorld
from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.overridden.overridden_spg_controller import OverriddenSPGGunMarkerController


# gun_marker_ctrl
class StandardFocusedSPGGunMarkerController(OverriddenSPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(StandardFocusedSPGGunMarkerController, self).__init__(reticle.gunMarkerType,
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
    # PlayerAvatar -> updateTargetingInfo
    # dispersionInfo[0] = shotDispMultiplierFactor
    # dispersionInfo[1] = gunShotDispersionFactorsTurretRotation
    # dispersionInfo[2] = chassisShotDispersionFactorsMovement
    # dispersionInfo[3] = chassisShotDispersionFactorsRotation
    # dispersionInfo[4] = aimingTime
    shotDispMultiplierFactor = playerAvatar._PlayerAvatar__dispersionInfo[0]

    # just return actual angle for conic dispersion
    return shotDispersionAngle * shotDispMultiplierFactor
