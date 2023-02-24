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
    resolveShowServerMarker(self)

    # clientMode becomes False when auto aiming
    # when in auto-aim, don't change client reticles presence
    # it will be properly internally done by AvatarInputHandler using gun_marker_ctrl.useDefaultGunMarkers()
    if self.clientMode:
        self._avatar.inputHandler.showGunMarker(gun_marker_ctrl.useClientGunMarker())


@overrideIn(VehicleGunRotator)
def applySettings(func, self, diff):
    if 'useServerAim' in diff:
        g_config.onConfigReload()


@overrideIn(VehicleGunRotator)
def start(func, self):
    func(self)
    g_config.onConfigReload += self.refreshGunRotatorState

    resolveShowServerMarker(self)


def resolveShowServerMarker(vehicleGunRotator):
    vehicleGunRotator.showServerMarker = gun_marker_ctrl.useServerGunMarker()


@overrideIn(VehicleGunRotator)
def stop(func, self):
    g_config.onConfigReload -= self.refreshGunRotatorState
    func(self)


