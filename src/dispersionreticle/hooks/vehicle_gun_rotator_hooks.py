import logging

from AvatarInputHandler import gun_marker_ctrl
from VehicleGunRotator import VehicleGunRotator

from dispersionreticle.config import g_config
from dispersionreticle.utils import *

logger = logging.getLogger(__name__)


###########################################################
# Adds hooks to invalidate gun markers presence
# whenever possible.
###########################################################

@addMethodTo(VehicleGunRotator)
def refreshGunRotatorState(self):
    logger.info("Invalidating gun markers rotator")
    self._avatar.inputHandler.showGunMarker2(gun_marker_ctrl.useServerGunMarker())
    self._avatar.inputHandler.showGunMarker(gun_marker_ctrl.useClientGunMarker())


@overrideIn(VehicleGunRotator)
def start(func, self):
    func(self)
    g_config.onConfigReload += self.refreshGunRotatorState


@overrideIn(VehicleGunRotator)
def stop(func, self):
    g_config.onConfigReload -= self.refreshGunRotatorState
    func(self)


