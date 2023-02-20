from aih_constants import GUN_MARKER_TYPE
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy

from dispersionreticle.utils import *
from dispersionreticle.utils.gun_marker_type import FOCUS_MARKER_TYPE_OFFSET, GUN_MARKER_TYPE_CLIENT_LATENCY


###########################################################
# CrosshairDataProxy hooks
# Responsible for changing penetration indicator (that mark on the
# middle of the reticle) to proper color (red, orange, green) on new markerType.
#
# Without this override, client and server focus gun markers would
# always be red and since focus markers are displayed in front of vanilla reticles, color of
# vanilla reticle penetration indicator wouldn't be visible.
###########################################################

# crosshair_proxy
@overrideIn(CrosshairDataProxy)
def __setGunMarkerState(func, self, markerType, value):
    position, direction, collision = value
    self.onGunMarkerStateChanged(markerType, position, direction, collision)
    self.onGunMarkerStateChanged(markerType + FOCUS_MARKER_TYPE_OFFSET, position, direction, collision)
    if markerType == GUN_MARKER_TYPE.CLIENT:
        self.onGunMarkerStateChanged(GUN_MARKER_TYPE_CLIENT_LATENCY, position, direction, collision)

