from dispersionreticle.controllers.focused.focused_default_controller import FocusedDefaultGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class ExtendedFocusedDefaultGunMarkerController(FocusedDefaultGunMarkerController):

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
