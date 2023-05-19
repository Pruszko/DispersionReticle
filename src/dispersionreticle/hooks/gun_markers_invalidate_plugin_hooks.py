import logging

from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import GunMarkersInvalidatePlugin

from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash
from dispersionreticle.settings.config import g_config
from dispersionreticle.utils import *

logger = logging.getLogger(__name__)


###########################################################
# Adds hooks to invalidate gun markers presence
# whenever possible.
###########################################################

@addMethodTo(GunMarkersInvalidatePlugin)
def invalidateGunMarkers(self):
    ctrl = self.sessionProvider.shared.crosshair
    if ctrl is not None:
        markersInfo = ctrl.getGunMarkersSetInfo()
        vehicleInfo = self._GunMarkersInvalidatePlugin__getVehicleInfo()

        logger.info("Invalidating gun markers plugin")
        self._parentObj.invalidateGunMarkers(markersInfo, vehicleInfo)
    return


g_dispersionReticleFlash = None


@overrideIn(GunMarkersInvalidatePlugin)
def start(func, self):
    global g_dispersionReticleFlash
    if g_dispersionReticleFlash is None:
        g_dispersionReticleFlash = DispersionReticleFlash()
        g_dispersionReticleFlash.active(True)

    func(self)
    g_config.onConfigReload += self.invalidateGunMarkers


@overrideIn(GunMarkersInvalidatePlugin)
def stop(func, self):
    global g_dispersionReticleFlash
    if g_dispersionReticleFlash is not None:
        g_dispersionReticleFlash.close()
        g_dispersionReticleFlash = None

    g_config.onConfigReload -= self.invalidateGunMarkers
    func(self)
