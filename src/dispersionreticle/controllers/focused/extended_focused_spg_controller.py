from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.focused.focused_spg_controller import FocusedSPGGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class ExtendedFocusedSPGGunMarkerController(FocusedSPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ExtendedFocusedSPGGunMarkerController, self).__init__(reticle, enabledFlag=enabledFlag)

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
