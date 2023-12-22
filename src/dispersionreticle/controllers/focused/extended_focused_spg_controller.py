from dispersionreticle.controllers.focused.focused_spg_controller import FocusedSPGGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class ExtendedFocusedSPGGunMarkerController(FocusedSPGGunMarkerController):

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
