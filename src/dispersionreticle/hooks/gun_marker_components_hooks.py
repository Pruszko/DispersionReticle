from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_components import GunMarkersComponents
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from dispersionreticle.utils import overrideIn
from dispersionreticle.utils.reticle_registry import ReticleRegistry

###########################################################
# Gun markers are displayed literally in pseudo-random order
# due to being stored in dict which does not have defined
# order of itervalues() method.
#
# Here we defined order of gun markers with first being
# the most important (rendered last, so displayed on all others).
###########################################################

GUN_MARKERS_PRIORITY = [
    _CONSTANTS.ARCADE_GUN_MARKER_NAME,
    _CONSTANTS.SNIPER_GUN_MARKER_NAME,
    _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME,
    _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME,
    _CONSTANTS.SPG_GUN_MARKER_NAME
]

GUN_MARKERS_PRIORITY += ReticleRegistry.CLIENT_FOCUS.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.SERVER_FOCUS.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.CLIENT_LATENCY.getMarkerNames()

GUN_MARKERS_PRIORITY += [
    _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME,
    _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME,
    _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME,
    _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME,
    _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME
]


def positionInPriorityList(viewSetting):
    name = viewSetting.name
    if name in GUN_MARKERS_PRIORITY:
        return GUN_MARKERS_PRIORITY.index(name)
    return 9999


###########################################################
# Returned list of ViewSettings normally does not have any defined order
# so different reticles can sometimes cover other reticles.
#
# This override is needed to return list with exact order of gun markers.
###########################################################
@overrideIn(GunMarkersComponents)
def getViewSettings(func, self):
    viewSettings = func(self)
    viewSettings.sort(key=positionInPriorityList, reverse=True)
    return viewSettings
