from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.focused.standard_focused_default_controller import \
    StandardFocusedDefaultGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class CustomFocusedDefaultGunMarkerController(StandardFocusedDefaultGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(CustomFocusedDefaultGunMarkerController, self).__init__(reticle, enabledFlag=enabledFlag)

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
