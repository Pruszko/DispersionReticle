import logging

from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import GunMarkersInvalidatePlugin

from dispersionreticle.flash import Layer
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash
from dispersionreticle.settings.config import g_config
from dispersionreticle.utils import *

logger = logging.getLogger(__name__)


###########################################################
# Adds hooks to invalidate gun markers presence
# whenever possible.
###########################################################

@addMethodTo(GunMarkersInvalidatePlugin)
def fullyInvalidateGunMarkers(self):
    ctrl = self.sessionProvider.shared.crosshair
    if ctrl is not None:
        markersInfo = ctrl.getGunMarkersSetInfo()
        vehicleInfo = self._GunMarkersInvalidatePlugin__getVehicleInfo()

        # provided by us by crosshair_panel_container_hooks.py
        self._parentObj.fullyInvalidateGunMarkers(markersInfo, vehicleInfo)
    return


g_TopDispersionReticleFlash = None
g_BottomDispersionReticleFlash = None


@overrideIn(GunMarkersInvalidatePlugin)
def start(func, self):
    global g_TopDispersionReticleFlash
    if g_TopDispersionReticleFlash is None:
        g_TopDispersionReticleFlash = DispersionReticleFlash(Layer.TOP)
        g_TopDispersionReticleFlash.active(True)

    global g_BottomDispersionReticleFlash
    if g_BottomDispersionReticleFlash is None:
        g_BottomDispersionReticleFlash = DispersionReticleFlash(Layer.BOTTOM)
        g_BottomDispersionReticleFlash.active(True)

    func(self)
    g_config.onConfigReload += self.fullyInvalidateGunMarkers


@overrideIn(GunMarkersInvalidatePlugin)
def stop(func, self):
    global g_TopDispersionReticleFlash
    if g_TopDispersionReticleFlash is not None:
        g_TopDispersionReticleFlash.close()
        g_TopDispersionReticleFlash = None

    global g_BottomDispersionReticleFlash
    if g_BottomDispersionReticleFlash is not None:
        g_BottomDispersionReticleFlash.close()
        g_BottomDispersionReticleFlash = None

    g_config.onConfigReload -= self.fullyInvalidateGunMarkers
    func(self)
