from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.focused.standard_focused_spg_controller import StandardFocusedSPGGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class CustomFocusedSPGGunMarkerController(StandardFocusedSPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(CustomFocusedSPGGunMarkerController, self).__init__(reticle, enabledFlag=enabledFlag)

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
