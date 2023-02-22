import logging

from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import GunMarkersInvalidatePlugin

from dispersionreticle.config import g_config
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


@overrideIn(GunMarkersInvalidatePlugin)
def start(func, self):
    func(self)
    g_config.onConfigReload += self.invalidateGunMarkers


@overrideIn(GunMarkersInvalidatePlugin)
def stop(func, self):
    g_config.onConfigReload -= self.invalidateGunMarkers
    func(self)
