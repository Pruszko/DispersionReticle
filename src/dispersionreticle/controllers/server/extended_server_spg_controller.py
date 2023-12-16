from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.overridden.overridden_spg_controller import OverriddenSPGGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


# gun_marker_ctrl
class ExtendedServerSPGGunMarkerController(OverriddenSPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ExtendedServerSPGGunMarkerController, self).__init__(reticle.getGunMarkerType(),
                                                                   reticle.getSpgDataProvider(),
                                                                   reticle.isServerReticle(),
                                                                   enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)

    def _interceptReplayLogic(self, dispersionAngle):
        return dispersionAngle
