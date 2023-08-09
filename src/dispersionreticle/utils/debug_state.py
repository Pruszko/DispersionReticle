import logging

import BigWorld
from AvatarInputHandler import gun_marker_ctrl, aih_global_binding, _BINDING_ID
from aih_constants import GUN_MARKER_FLAG


IS_DEBUGGING = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if IS_DEBUGGING:
    logger.setLevel(logging.DEBUG)


# gun marker server state is scattered around many variables that are not logged anywhere
# here there is collected state of as many variables/calls
# that directly or indirectly changes gun marker server state as I could find
#
# debug logs are only done (or registered) when IS_DEBUGGING is enabled
# and other parts of code checks whenever it should call mark field changes or calls based on this flag

class ValueBroadcast(object):

    ALL = []

    def __init__(self, name, initialValue):
        self.name = name
        self.value = initialValue

        ValueBroadcast.ALL.append(self)

    def get(self):
        return self.value

    def set(self, newValue, cause="assignment"):
        if cause == "sync":
            if self.value != newValue:
                logger.debug("State [%s] synced: [%s] -> [%s]", self.name, self.value, newValue)
        else:
            logger.debug("State [%s] set by %s: [%s] -> [%s]", self.name, cause, self.value, newValue)
        self.value = newValue

    def failToSet(self, newValue, cause="assignment"):
        if cause == "sync":
            if self.value != newValue:
                logger.debug("State [%s] failed to sync: [%s] -> [%s]", self.name, self.value, newValue)
        else:
            logger.debug("State [%s] failed to set by %s: [%s] -> [%s]", self.name, cause, self.value, newValue)

    def broadcast(self):
        logger.debug("State [%s] value: [%s]", self.name, self.value)


class DebugStateCollector(object):

    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)

    def __init__(self):
        self.useClientGunMarker = ValueBroadcast("useClientGunMarker", None)
        self.useDefaultGunMarkers = ValueBroadcast("useDefaultGunMarkers", None)
        self.useServerGunMarker = ValueBroadcast("useServerGunMarker", None)

        self.clientModeFlag = ValueBroadcast("clientModeFlag", None)
        self.serverModeFlag = ValueBroadcast("serverModeFlag", None)

        self.clientMode = ValueBroadcast("clientMode", None)
        self.showServerMarker = ValueBroadcast("showServerMarker", None)

        self.enableServerAim = ValueBroadcast("enableServerAim", None)

        if not IS_DEBUGGING:
            return

        self.subscribeAihGlobalBindings()

    def subscribeAihGlobalBindings(self):
        aih_global_binding.subscribe(_BINDING_ID.GUN_MARKERS_FLAGS, self.__onGunMarkerFlagChange)

    def __onGunMarkerFlagChange(self, _):
        logger.debug("Invoking __onGunMarkerFlagChange")
        self.__markGunMarkersFlags(cause="flag change event")

    def broadcast(self):
        for value in ValueBroadcast.ALL:
            value.broadcast()

    def collectStateAfterConfigReload(self):
        logger.debug("Performing debug state sync after config reload")
        self.__collectState()

    def collectStateBeforeGunMarkersUpdate(self):
        # logger.debug("Performing debug state sync before gun marker update")
        self.__collectState()

    def __collectState(self):
        self.__markUseGunMarkers(cause="sync")
        self.__markGunMarkersFlags(cause="sync")
        self.markClientMode(cause="sync")
        self.markShowServerMarker(cause="sync")

        # self.markEnableServerAim(...)
        #
        # we cannot reliably obtain development features outside direct calls to setter
        # or at least I don't want to call methods not explicitly present in WG code even if such getter exists
        #
        # last time I did so, it ended up in lost few hours of debugging why they don't work properly
        # just to conclude they just completely don't work, lmao

    def __markUseGunMarkers(self, cause=None):
        self.useClientGunMarker.set(gun_marker_ctrl.useClientGunMarker(),
                                    cause)
        self.useDefaultGunMarkers.set(gun_marker_ctrl.useDefaultGunMarkers(),
                                      cause)
        self.useServerGunMarker.set(gun_marker_ctrl.useServerGunMarker(),
                                    cause)

    def __markGunMarkersFlags(self, cause=None):
        self.clientModeFlag.set(self.__gunMarkersFlags & GUN_MARKER_FLAG.CLIENT_MODE_ENABLED > 0, cause)
        self.serverModeFlag.set(self.__gunMarkersFlags & GUN_MARKER_FLAG.SERVER_MODE_ENABLED > 0, cause)

    def markClientMode(self, cause=None):
        if self.__isGunRotatorPresent():
            self.clientMode.set(BigWorld.player().gunRotator.clientMode, cause)

    def markClientModeFail(self, enabled, cause=None):
        if self.__isGunRotatorPresent():
            self.clientMode.failToSet(enabled, cause)

    def markShowServerMarker(self, cause=None):
        if self.__isGunRotatorPresent():
            self.showServerMarker.set(BigWorld.player().gunRotator.showServerMarker, cause)

    def markShowServerMarkerFail(self, enabled, cause=None):
        if self.__isGunRotatorPresent():
            self.showServerMarker.failToSet(enabled, cause)

    def markEnableServerAim(self, enabled, cause=None):
        self.enableServerAim.set(enabled, cause)

    def markEnableServerAimFail(self, enabled, cause=None):
        self.enableServerAim.failToSet(enabled, cause)

    def __isGunRotatorPresent(self):
        return BigWorld.player() is not None and hasattr(BigWorld.player(), "gunRotator")


g_debugStateCollector = DebugStateCollector()
