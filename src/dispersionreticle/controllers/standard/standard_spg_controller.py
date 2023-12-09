import BigWorld, BattleReplay
from AvatarInputHandler.gun_marker_ctrl import _SPGGunMarkerController, _MARKER_FLAG

from dispersionreticle.settings.config_param import g_configParams


# gun_marker_ctrl
class OverriddenSPGGunMarkerController(_SPGGunMarkerController):

    def __init__(self, gunMakerType, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(OverriddenSPGGunMarkerController, self).__init__(gunMakerType, dataProvider, enabledFlag=enabledFlag)

    def _update(self):
        pos3d, vel3d, gravity3d = self._getCurrentShotInfo()
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            self._SPGGunMarkerController__updateRelaxTime()
        self._updateDispersionData()

        newSize = self._size * g_configParams.reticleSizeMultiplier()

        self._dataProvider.update(pos3d, vel3d, gravity3d, newSize)
