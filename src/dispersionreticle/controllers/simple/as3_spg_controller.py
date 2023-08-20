import BigWorld, BattleReplay
from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG, _SPGGunMarkerController


# gun_marker_ctrl
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash
from dispersionreticle.settings.config import g_config


class AS3SPGGunMarkerController(_SPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(AS3SPGGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                        reticle.getSpgDataProvider(),
                                                        enabledFlag=enabledFlag)
        self.__reticle = reticle

    def _update(self):
        pos3d, vel3d, gravity3d = self._getCurrentShotInfo()
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            self._SPGGunMarkerController__updateRelaxTime()
        self._updateDispersionData()

        newSize = self._size * g_config.reticleSizeMultiplier

        self._dataProvider.update(pos3d, vel3d, gravity3d, newSize)

        DispersionReticleFlash.onReticleUpdate(self.__reticle, newSize)

    def _updateDispersionData(self):
        dispersionAngle = self._gunRotator.dispersionAngle

        # here we avoid replay-specific code, it is handled by vanilla controllers
        # even if their markers may not be present

        self._dataProvider.setupConicDispersion(dispersionAngle)
