import BattleReplay
import BigWorld
import Math
import constants
from AvatarInputHandler.gun_marker_ctrl import _DefaultGunMarkerController, _makeWorldMatrix, _MARKER_FLAG
from aih_constants import GUN_MARKER_TYPE

from dispersionreticle.utils import isClientWG
from dispersionreticle.utils.reticle_registry import ReticleRegistry


# gun_marker_ctrl
class OverriddenDefaultGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, isServer, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(OverriddenDefaultGunMarkerController, self).__init__(gunMakerType, dataProvider, enabledFlag=enabledFlag)
        self._isServer = isServer

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
        super(_DefaultGunMarkerController, self).update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)

        positionMatrix = Math.Matrix()
        positionMatrix.setTranslate(gunMarkerInfo.position)
        self._updateMatrixProvider(positionMatrix, relaxTime)

        size = self._getMarkerSize(gunMarkerInfo)
        size = self._interceptReplayLogic(size)

        # this have to be here, we don't want to corrupt replays
        sizeMultiplier = ReticleRegistry.getReticleSizeMultiplierFor(gunMarkerType=markerType)

        size = self._interceptSize(size, gunMarkerInfo.position) * sizeMultiplier

        positionMatrixForScale = BigWorld.checkAndRecalculateIfPositionInExtremeProjection(positionMatrix)
        worldMatrix = _makeWorldMatrix(positionMatrixForScale)
        markerHelperScale = BigWorld.markerHelperScale
        self._DefaultGunMarkerController__currentSize = markerHelperScale(worldMatrix, size) * self._DefaultGunMarkerController__screenRatio
        self._DefaultGunMarkerController__currentSizeOffset = markerHelperScale(worldMatrix, gunMarkerInfo.sizeOffset) * self._DefaultGunMarkerController__screenRatio

        # handle Responsive Reticle mod presence
        # we have to call it BEFORE self._dataProvider.updateSizes(...) method
        # otherwise we won't precisely know if we should skip updates as well
        shouldUpdateExtendedReticleSize = self._shouldUpdateExtendedReticleSize()

        self._dataProvider.updateSizes(self._DefaultGunMarkerController__currentSize,
                                       self._DefaultGunMarkerController__currentSizeOffset,
                                       relaxTime,
                                       self._DefaultGunMarkerController__offsetInertness)
        if self._DefaultGunMarkerController__offsetInertness == self._OFFSET_DEFAULT_INERTNESS:
            self._DefaultGunMarkerController__offsetInertness = self._OFFSET_SLOWDOWN_INERTNESS

        if shouldUpdateExtendedReticleSize:
            self._interceptPostUpdate(self._DefaultGunMarkerController__currentSize)

    def lesta_update(self, markerType, pos, direction, sizeVector, relaxTime, collData):
        super(_DefaultGunMarkerController, self).update(markerType, pos, direction, sizeVector, relaxTime, collData)

        positionMatrix = Math.Matrix()
        positionMatrix.setTranslate(pos)
        self._updateMatrixProvider(positionMatrix, relaxTime)

        size = sizeVector[0]
        idealSize = sizeVector[1]

        size = self._interceptReplayLogic(size)

        # this have to be here, we don't want to corrupt replays
        sizeMultiplier = ReticleRegistry.getReticleSizeMultiplierFor(gunMarkerType=markerType)

        size = self._interceptSize(size, pos) * sizeMultiplier
        idealSize *= self._interceptSize(idealSize, pos) * sizeMultiplier

        positionMatrixForScale = BigWorld.checkAndRecalculateIfPositionInExtremeProjection(positionMatrix)
        worldMatrix = _makeWorldMatrix(positionMatrixForScale)
        currentSize = BigWorld.markerHelperScale(worldMatrix, size) * self._DefaultGunMarkerController__screenRatio
        idealSize = BigWorld.markerHelperScale(worldMatrix, idealSize) * self._DefaultGunMarkerController__screenRatio
        self._DefaultGunMarkerController__sizeFilter.update(currentSize, idealSize)
        self._DefaultGunMarkerController__curSize = self._DefaultGunMarkerController__sizeFilter.getSize()

        # handle Responsive Reticle mod presence
        # we have to call it BEFORE self._dataProvider.updateSize(...) method
        # otherwise we won't precisely know if we should skip updates as well
        shouldUpdateExtendedReticleSize = self._shouldUpdateExtendedReticleSize()

        if self._DefaultGunMarkerController__replSwitchTime > 0.0:
            self._DefaultGunMarkerController__replSwitchTime -= relaxTime
            self._dataProvider.updateSize(self._DefaultGunMarkerController__curSize, 0.0)
        else:
            self._dataProvider.updateSize(self._DefaultGunMarkerController__curSize, relaxTime)

        if shouldUpdateExtendedReticleSize:
            self._interceptPostUpdate(self._DefaultGunMarkerController__curSize)

    # ugly hack
    # we are dependent on mod internal state, which already was a workaround - yikes!
    def _shouldUpdateExtendedReticleSize(self):
        # if either mod is not present or mod haven't stored timestamps yet, always update reticles
        dataProviderSizeCache = getattr(BigWorld.player(), "_mod_dataProviderSizeCache", None)  # type: dict
        if dataProviderSizeCache is None:
            return True

        # if this data provider doesn't have timestamps, it means it is most likely SPG data provider
        # on which we don't want to skip updates
        lastTime = dataProviderSizeCache.get(id(self._dataProvider), None)
        if lastTime is None:
            return True

        # handle timeDiff the same way Responsive Reticle does
        timeDiff = BigWorld.time() - lastTime
        if timeDiff < constants.SERVER_TICK_LENGTH:
            return False

        return True

    def isClientController(self):
        return not self._isServer

    def isServerController(self):
        return self._isServer

    def _interceptReplayLogic(self, size):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            s = self._replayReader(replayCtrl)()
            if s != -1.0:
                size = s
        elif replayCtrl.isRecording:
            if self._areBothModesEnabled():
                # IMPORTANT
                # when both client-side and server-side reticles are enabled
                # we MUST write only server-side data, because
                # VehicleGunRotator in that state writes server data to replays
                if replayCtrl.isServerAim and self._gunMarkerType == GUN_MARKER_TYPE.SERVER:
                    self._replayWriter(replayCtrl)(size)
            else:
                # update is always done for all reticles,
                # so we can use any reticle to write data to replay
                # but for simplicity, use client and dual acc reticle
                if self._gunMarkerType in (GUN_MARKER_TYPE.CLIENT, GUN_MARKER_TYPE.DUAL_ACC):
                    self._replayWriter(replayCtrl)(size)
        return size

    def _interceptPostUpdate(self, size):
        pass

    def _interceptSize(self, size, pos):
        return size

    def _isAnyModeEnabled(self):
        return self._isClientModeEnabled() or self._isServerModeEnabled()

    def _areBothModesEnabled(self):
        return self._isClientModeEnabled() and self._isServerModeEnabled()

    def _isClientModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED

    def _isServerModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED
