import logging

import BigWorld
import Math
import AvatarInputHandler
from AvatarInputHandler import gun_marker_ctrl, aih_global_binding, AimingSystems
from aih_constants import GUN_MARKER_FLAG
from constants import ARENA_PERIOD

from dispersionreticle.utils import *
from dispersionreticle.utils import debug_state


logger = logging.getLogger(__name__)

if debug_state.IS_DEBUGGING:
    logger.setLevel(logging.DEBUG)


class _OneTickCache(object):
    gunMarkersFlags = aih_global_binding.bindRO(AvatarInputHandler._BINDING_ID.GUN_MARKERS_FLAGS)
    clientState = aih_global_binding.bindRW(AvatarInputHandler._BINDING_ID.CLIENT_GUN_MARKER_STATE)
    serverState = aih_global_binding.bindRW(AvatarInputHandler._BINDING_ID.SERVER_GUN_MARKER_STATE)

    def __init__(self):
        self.isClientModeEnabled = False
        self.isServerModeEnabled = False
        self.areBothModesEnabled = False
        self.sniperViewportPosition = Math.Vector3()
        self.dualAccuracy = None

    def updateCache(self):
        gunMarkersFlag = self.gunMarkersFlags

        self.isClientModeEnabled = gunMarkersFlag & GUN_MARKER_FLAG.CLIENT_MODE_ENABLED
        self.isServerModeEnabled = gunMarkersFlag & GUN_MARKER_FLAG.SERVER_MODE_ENABLED
        self.areBothModesEnabled = self.isClientModeEnabled and self.isServerModeEnabled

        self.sniperViewportPosition = getSniperViewportPosition()
        self.dualAccuracy = getDualAccuracy()


def getDualAccuracy():
    # WG specific
    # different way of getting dual accuracy component in WoT 2.1.0.0
    if isClientWG():
        from DualAccuracy import DualAccuracy
        from items.vehicle_mechanics_types import VehicleMechanicKeys
        from vehicles.mechanics.mechanic_helpers import getPlayerVehicleMechanicComponent

        return getPlayerVehicleMechanicComponent(VehicleMechanicKeys.DUAL_ACCURACY)  # type: DualAccuracy
    else:
        from DualAccuracyBase import DualAccuracyBase, getPlayerVehicleDualAccuracy

        return getPlayerVehicleDualAccuracy()  # type: DualAccuracyBase


def getSniperViewportPosition():
    gunRotator = BigWorld.player().gunRotator
    gunMatrix = AimingSystems.getPlayerGunMat(gunRotator.turretYaw, gunRotator.gunPitch)
    return gunMatrix.translation


g_oneTickCache = _OneTickCache()


@overrideIn(AvatarInputHandler.AvatarInputHandler, condition=isClientWG)
def __onArenaStarted(func, self, period, *args):
    common_onArenaStarted(func, self, period, *args)


# Lesta specific
# changed method name
@overrideIn(AvatarInputHandler.AvatarInputHandler, condition=isClientLesta)
def _onArenaStarted(func, self, period, *args):
    common_onArenaStarted(func, self, period, *args)


def common_onArenaStarted(func, self, period, *args):
    func(self, period, *args)

    # this event handler is called multiple times
    # we only want to react to it when battle start finishes countdown
    if period != ARENA_PERIOD.BATTLE:
        return

    # TODO fix it in a more sophisticated way than "this"
    #
    # in Onslaught game mode something weird happens to server gun markers
    # when selecting different than initial vehicle before countdown finishes
    #
    # by this code, we will invalidate BigWorld internal state to reboot GunMarkerComponent
    # as soon as the game starts
    #
    # generally I want to analyze server marker state more precisely with DebugStateCollector
    # however, when I got some free time, Onslaught event has already finished
    # so I cannot find real root cause now
    #
    # previously I've fixed it with blind guess quickly restarting showServerMarker flag and it worked
    # but rebooting is not the finest way to workaround bugs
    #
    # not only that, but after first version of this fix was implemented, it fixed
    # upper mentioned DETERMINISTIC bug in Onslaught
    # HOWEVER, new NON-DETERMINISTIC bug has appeared when certain conditions were met in ANY MATCH:
    # - user was using enabled "Use server aim" from in-game menu
    # - user were not using any server-related reticles from this mod config
    #
    # this bug happens quite rarely and randomly (around 5%-10% chance to appear), but often enough to bother users
    # after roughly 30 matches (I have bad luck as you see) I've managed to reproduce it
    # and introspect all server reticle related variables when it occurred
    # everything was fine with all of them
    # most importantly, Avatar#enableServerAim was eventually called with True when it needed to be True
    #
    # my guess is that
    # changing "server_marker" developer feature flag too fast may cause
    # some consecutive calls to be completely ignored, in result, we may end up with DISABLED server aim
    # despite calling it with True
    #
    # in other words, it looks like setting developer feature flags on Avatar base
    # may be NON-BLOCKING ASYNCHRONOUS operation (or something really is messed up that I haven't noticed yet)
    #
    # or it might be related to __onArenaStarted being called by BigWorld
    # and bug is some race condition that messes up "server_marker" flag
    #
    # either way, to workaround this, we will delay calls a little bit to be (most likely) sure BigWorld caught up
    # to accept consecutive call (probably 1 ms would be fine, but let's throw 40 ms to be sure, why the heck not)
    #
    # this is overall bad, but for now it is what it is

    logger.debug("Onslaught server marker fix start")

    def negateGunMarkerComponentState():
        logger.debug("Onslaught server marker fix negate begin")
        BigWorld.player().gunRotator.showServerMarker = not gun_marker_ctrl.useServerGunMarker()
        logger.debug("Onslaught server marker fix negate finished")

        # 2: schedule restore
        BigWorld.callback(0.04, restoreGunMarkerComponentState)

    def restoreGunMarkerComponentState():
        logger.debug("Onslaught server marker fix restore begin")
        BigWorld.player().gunRotator.showServerMarker = gun_marker_ctrl.useServerGunMarker()
        logger.debug("Onslaught server marker fix restore finished")

    # 1: schedule negation
    BigWorld.callback(0.04, negateGunMarkerComponentState)
