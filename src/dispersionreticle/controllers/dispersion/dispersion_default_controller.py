import BigWorld, Math
from AvatarInputHandler import AimingSystems
from AvatarInputHandler.gun_marker_ctrl import _DefaultGunMarkerController, _makeWorldMatrix, _MARKER_FLAG

from dispersionreticle.settings.config import g_config


# gun_marker_ctrl
class DispersionDefaultGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(DispersionDefaultGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                                   reticle.getStandardDataProvider(),
                                                                   enabledFlag=enabledFlag)

    def update(self, markerType, pos, direction, sizeVector, relaxTime, collData):
        super(_DefaultGunMarkerController, self).update(markerType, pos, direction, sizeVector, relaxTime, collData)
        positionMatrix = Math.Matrix()
        positionMatrix.setTranslate(pos)
        self._updateMatrixProvider(positionMatrix, relaxTime)

        # size = sizeVector[0]
        # idealSize = sizeVector[1]
        size = getFocusedSize(positionMatrix)
        idealSize = size

        # here we avoid replay-specific code, it is handled by vanilla controllers
        # even if their markers may not be present

        sizeMultiplier = g_config.getReticleSizeMultiplier()

        size *= sizeMultiplier
        idealSize *= sizeMultiplier

        positionMatrixForScale = BigWorld.checkAndRecalculateIfPositionInExtremeProjection(positionMatrix)
        worldMatrix = _makeWorldMatrix(positionMatrixForScale)

        currentSize = BigWorld.markerHelperScale(worldMatrix, size) * self._DefaultGunMarkerController__screenRatio
        idealSize = BigWorld.markerHelperScale(worldMatrix, idealSize) * self._DefaultGunMarkerController__screenRatio

        self._DefaultGunMarkerController__sizeFilter.update(currentSize, idealSize)
        self._DefaultGunMarkerController__curSize = self._DefaultGunMarkerController__sizeFilter.getSize()

        if self._DefaultGunMarkerController__replSwitchTime > 0.0:
            self._DefaultGunMarkerController__replSwitchTime -= relaxTime
            self._dataProvider.updateSize(self._DefaultGunMarkerController__curSize, 0.0)
        else:
            self._dataProvider.updateSize(self._DefaultGunMarkerController__curSize, relaxTime)


def getFocusedSize(positionMatrix):
    playerAvatar = BigWorld.player()
    vehicleDesc = playerAvatar._PlayerAvatar__getDetailedVehicleDescriptor()

    # this doesn't account for arcade view
    # but let's leave it commented as a last resort
    # gunPos = BigWorld.camera().position

    gunPos = getSniperViewportPosition()

    shotDir = positionMatrix.applyToOrigin() - gunPos
    shotDist = shotDir.length

    # gun dispersion per 1m unit
    gunDispersionAngle = vehicleDesc.gun.shotDispersionAngle

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

    # actual dispersion per 1m unit
    dispersionAngle = gunDispersionAngle * shotDispMultiplierFactor

    # size is diameter that scales with distance
    return 2.0 * shotDist * dispersionAngle


def getSniperViewportPosition():
    gunRotator = BigWorld.player().gunRotator
    gunMatrix = AimingSystems.getPlayerGunMat(gunRotator.turretYaw, gunRotator.gunPitch)
    return gunMatrix.translation
