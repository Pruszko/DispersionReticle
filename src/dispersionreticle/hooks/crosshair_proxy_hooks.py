from aih_constants import GUN_MARKER_TYPE
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy

from dispersionreticle.utils import *
from dispersionreticle.utils.reticle_registry import ReticleRegistry


###########################################################
# CrosshairDataProxy hooks
# Responsible for changing penetration indicator (that mark on the
# middle of the reticle) to proper color (red, orange, green) on new markerType.
#
# Without this override, new gun markers would
# always be red and because most of the time they are displayed in front of vanilla reticles, color of
# vanilla reticle penetration indicator wouldn't be visible.
###########################################################

# crosshair_proxy
@overrideIn(CrosshairDataProxy)
def __setGunMarkerState(func, self, markerType, value):
    func(self, markerType, value)

    # I don't really know how to react here to DUAL_ACC
    #
    # let's just stay with client/server behavior
    # not to update client reticles too often
    if markerType == GUN_MARKER_TYPE.DUAL_ACC:
        return

    isServerMarkerStateUpdate = markerType == GUN_MARKER_TYPE.SERVER

    for reticle in ReticleRegistry.ADDITIONAL_RETICLES:
        if reticle.isServerReticle() == isServerMarkerStateUpdate:
            self.onGunMarkerStateChanged(reticle.gunMarkerType, *value)
