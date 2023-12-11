from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.hybrid.standard_hybrid_default_controller import \
    StandardHybridDefaultGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class CustomHybridDefaultGunMarkerController(StandardHybridDefaultGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(CustomHybridDefaultGunMarkerController, self).__init__(reticle, enabledFlag=enabledFlag)

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
