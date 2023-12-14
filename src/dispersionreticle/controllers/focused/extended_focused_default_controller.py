from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.focused.focused_default_controller import \
    FocusedDefaultGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class ExtendedFocusedDefaultGunMarkerController(FocusedDefaultGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ExtendedFocusedDefaultGunMarkerController, self).__init__(reticle, enabledFlag=enabledFlag)

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
