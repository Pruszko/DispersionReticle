import BigWorld, Math, BattleReplay
from AvatarInputHandler.gun_marker_ctrl import _DefaultGunMarkerController, _makeWorldMatrix, _MARKER_FLAG
from aih_constants import GUN_MARKER_TYPE

from dispersionreticle.config import g_config


# gun_marker_ctrl
class NewDefaultGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED, isMainReticle=True):
        super(NewDefaultGunMarkerController, self).__init__(gunMakerType, dataProvider, enabledFlag=enabledFlag)
        self.__isMainReticle = isMainReticle

    def update(self, markerType, pos, direction, sizeVector, relaxTime, collData):
        super(_DefaultGunMarkerController, self).update(markerType, pos, direction, sizeVector, relaxTime, collData)
        positionMatrix = Math.Matrix()
        positionMatrix.setTranslate(pos)
        self._updateMatrixProvider(positionMatrix, relaxTime)

        size = sizeVector[0]
        idealSize = sizeVector[1]

        # avoid replay recording if not main reticle
        if self.__isMainReticle:
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isPlaying and replayCtrl.isClientReady:
                s = replayCtrl.getArcadeGunMarkerSize()
                if s != -1.0:
                    size = s
            elif replayCtrl.isRecording:
                if replayCtrl.isServerAim and self._gunMarkerType == GUN_MARKER_TYPE.SERVER:
                    replayCtrl.setArcadeGunMarkerSize(size)
                elif self._gunMarkerType == GUN_MARKER_TYPE.CLIENT:
                    replayCtrl.setArcadeGunMarkerSize(size)

        # this have to be here, we don't want to corrupt replays
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


# gun_marker_ctrl
class FocusGunMarkerController(_DefaultGunMarkerController):

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
    cameraPos = BigWorld.camera().position
    shotDir = positionMatrix.applyToOrigin() - cameraPos
    shotDist = shotDir.length

    playerAvatar = BigWorld.player()
    vehicleDesc = playerAvatar._PlayerAvatar__getDetailedVehicleDescriptor()

    # gun dispersion per 1m unit
    gunDispersionAngle = vehicleDesc.gun.shotDispersionAngle

    # multiplier that accounts crew, food, etc.
    shotDispMultiplierFactor = playerAvatar._PlayerAvatar__aimingInfo[2]

    # actual dispersion per 1m unit
    dispersionAngle = gunDispersionAngle * shotDispMultiplierFactor

    # size is diameter that scales with distance
    return 2.0 * shotDist * dispersionAngle
