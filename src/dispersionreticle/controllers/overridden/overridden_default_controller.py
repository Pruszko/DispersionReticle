import BigWorld, Math, BattleReplay
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _DefaultGunMarkerController, _makeWorldMatrix, _MARKER_FLAG
from aih_constants import GUN_MARKER_TYPE

from dispersionreticle.settings.config_param import g_configParams


# gun_marker_ctrl
class OverriddenDefaultGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, isServer, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(OverriddenDefaultGunMarkerController, self).__init__(gunMakerType, dataProvider, enabledFlag=enabledFlag)
        self._isServer = isServer

    def update(self, markerType, pos, direction, size, sizeOffset, relaxTime, collData):
        super(_DefaultGunMarkerController, self).update(markerType, pos, direction, size, sizeOffset, relaxTime, collData)

        positionMatrix = Math.Matrix()
        positionMatrix.setTranslate(pos)
        self._updateMatrixProvider(positionMatrix, relaxTime)

        size = self._interceptReplayLogic(size)

        # this have to be here, we don't want to corrupt replays
        sizeMultiplier = g_configParams.reticleSizeMultiplier()

        size = self._interceptSize(size, pos, direction, relaxTime, collData) * sizeMultiplier

        positionMatrixForScale = BigWorld.checkAndRecalculateIfPositionInExtremeProjection(positionMatrix)
        worldMatrix = _makeWorldMatrix(positionMatrixForScale)
        self._DefaultGunMarkerController__currentSize = BigWorld.markerHelperScale(worldMatrix, size) * self._DefaultGunMarkerController__screenRatio
        self._DefaultGunMarkerController__currentSizeOffset = BigWorld.markerHelperScale(worldMatrix, sizeOffset) * self._DefaultGunMarkerController__screenRatio
        self._dataProvider.updateSizes(self._DefaultGunMarkerController__currentSize,
                                       self._DefaultGunMarkerController__currentSizeOffset,
                                       relaxTime,
                                       self._DefaultGunMarkerController__offsetInertness)
        if self._DefaultGunMarkerController__offsetInertness == self._OFFSET_DEFAULT_INERTNESS:
            self._DefaultGunMarkerController__offsetInertness = self._OFFSET_SLOWDOWN_INERTNESS

        self._interceptPostUpdate(self._DefaultGunMarkerController__currentSize)

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

    def _interceptSize(self, size, pos, direction, relaxTime, collData):
        return size

    def _isAnyModeEnabled(self):
        return self._isClientModeEnabled() or self._isServerModeEnabled()

    def _areBothModesEnabled(self):
        return self._isClientModeEnabled() and self._isServerModeEnabled()

    def _isClientModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED

    def _isServerModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED
