import logging

import BattleReplay
from AvatarInputHandler import gun_marker_ctrl
from VehicleGunRotator import VehicleGunRotator

from dispersionreticle.settings.config import g_config
from dispersionreticle.utils import *
from dispersionreticle.utils.debug_state import g_debugStateCollector

logger = logging.getLogger(__name__)


###########################################################
# Adds hooks to invalidate gun markers presence
# whenever possible.
###########################################################

@addMethodTo(VehicleGunRotator)
def refreshGunRotatorState(self):
    logger.info("Invalidating gun markers rotator")
    self.showServerMarker = gun_marker_ctrl.useServerGunMarker()

    # clientMode becomes False when auto aiming
    # when in auto-aim, don't change client reticles presence
    # it will be properly internally done by AvatarInputHandler using gun_marker_ctrl.useDefaultGunMarkers()
    if self.clientMode:
        self._avatar.inputHandler.showClientGunMarkers(gun_marker_ctrl.useClientGunMarker())


@overrideIn(VehicleGunRotator)
def applySettings(func, self, diff):
    if 'useServerAim' in diff:
        g_config.refreshGameState()


# code like this from Avatar makes me wonder, how am I supposed to react to this?
# stop() and start() changes server state quite fast and on top of that enableServerAim is called on top of it
# this looks like a bugfix that no one will know what it actually fixes
#
# self.gunRotator.stop()
# self.gunRotator.start()
# self.gunRotator.reset()
# self.enableServerAim(self.gunRotator.showServerMarker)

@overrideIn(VehicleGunRotator)
def start(func, self):
    func(self)
    g_config.onConfigReload += self.refreshGunRotatorState

    # this line is necessary to restore proper showServerMarker
    # due to start method setting showServerMarker to that from the game settings
    self.showServerMarker = gun_marker_ctrl.useServerGunMarker()

    if debug_state.IS_DEBUGGING:
        g_debugStateCollector.markClientMode(cause="gunRotator.start")
        g_debugStateCollector.markShowServerMarker(cause="gunRotator.start")


@overrideIn(VehicleGunRotator)
def stop(func, self):
    g_config.onConfigReload -= self.refreshGunRotatorState
    func(self)

    # mimic logic that changes showServerMarker for debugging purposes
    # necessary to collect properly showServerMarker because WG simply accessed __showServerMarker directly
    # when invoking stop() method, so we wouldn't have got update by property setter
    if not debug_state.IS_DEBUGGING:
        return

    if not self._VehicleGunRotator__isStarted:
        return
    else:
        if self._avatar.inputHandler is None:
            return
        if self.clientMode and self.showServerMarker:
            g_debugStateCollector.markShowServerMarker(cause="gunRotator.stop")


# VehicleGunRotator hooks purely for debugging purposes

@overrideIn(VehicleGunRotator, onlyWhenDebugging=True)
def __set_showServerMarker(func, self, value):
    prevValue = self.showServerMarker

    func(self, value)

    replayCtrl = BattleReplay.g_replayCtrl
    if replayCtrl.isPlaying:
        g_debugStateCollector.markShowServerMarkerFail(value, cause="assignment (replay is playing)")
        return

    if prevValue == value:
        g_debugStateCollector.markShowServerMarkerFail(value, cause="assignment (same value)")
        return

    g_debugStateCollector.markShowServerMarker(cause="assignment")


if debug_state.IS_DEBUGGING:
    VehicleGunRotator.showServerMarker = property(lambda self: self._VehicleGunRotator__showServerMarker,
                                                  __set_showServerMarker)


@overrideIn(VehicleGunRotator, onlyWhenDebugging=True)
def __set_clientMode(func, self, value):
    prevValue = self.clientMode

    func(self, value)

    if prevValue == value:
        g_debugStateCollector.markClientModeFail(value, cause="assignment (same value)")
        return

    g_debugStateCollector.markClientMode(cause="assignment")


if debug_state.IS_DEBUGGING:
    VehicleGunRotator.clientMode = property(lambda self: self._VehicleGunRotator__clientMode,
                                            __set_clientMode)
