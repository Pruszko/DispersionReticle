from dispersionreticle.controllers.hybrid.hybrid_spg_controller import HybridSPGGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


class ExtendedHybridSPGGunMarkerController(HybridSPGGunMarkerController):

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)
