import BigWorld
from Avatar import Avatar

from dispersionreticle.utils import overrideIn
from dispersionreticle.utils.debug_state import g_debugStateCollector


###########################################################
# Avatar hooks purely for debugging purposes
###########################################################

@overrideIn(Avatar, onlyWhenDebugging=True)
def enableServerAim(func, self, enable):
    func(self, enable)

    g_debugStateCollector.markEnableServerAim(enable, cause="avatar.enableServerAim")


@overrideIn(Avatar, onlyWhenDebugging=True)
def __controlAnotherVehicleAfteraction(func, self, vehicleID, callback):
    func(self, vehicleID, callback)

    # development feature "server_marker" is enabled when entity vehicle is found
    vehicle = BigWorld.entity(vehicleID)
    if vehicle is None:
        g_debugStateCollector.markEnableServerAimFail(True, cause="avatar.controlAnotherVehicle none vehicle")
        return

    g_debugStateCollector.markEnableServerAim(True, cause="avatar.controlAnotherVehicle")
