from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_components
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_components import GunMarkersComponents, GunMarkerComponent
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash
from dispersionreticle.utils import overrideIn
from dispersionreticle.utils.reticle_registry import ReticleRegistry


_logger = gm_components._logger


###########################################################
# The general contract between CrosshairPanelContainer, GunMarkerComponents
# and GUI.WGCrosshairFlash (and its spg variant) is following:
# - CrosshairPanelContainer spawns gun markers in its app
# - panel then notifies GunMarkerComponents to create view like GUI.WGCrosshairFlash that manages it
# - for now, despite markers being in display list, they're not rendered because during countdown
#   they aren't getting assigned data provider and when it is not present, markers are invisible
# - when countdown is finished, markers are invalidated and get assigned data provider
#   that makes them possible to render
# - so basically, data provider presence determines marker presence on screen, but it doesn't control
#   their presence in display list
# - markers are removed from display list when CrosshairPanelContainer requests it
# - then panel notifies GunMarkerComponents to clear data provider and removes GUI.WGCrosshairFlash
#   from panel's GUI child list
#
# Because using custom AS3GunMarkerComponent we have control over how we will spawn our markers, we will
# attempt to interpose that logic in the most "vanilla way" possible
#
# Instead of returning GUI.WGCrosshairFlash, we will use a "proxy" to control marker visibility
# that imitates methods that WG marker had to alter data provider presence
# Also, for every marker except SPG one, we will alter as_createMarker and as_destroy marker
# in CrosshairPanelContainer to interpose marker instantiation to our app
#
# Fun fact
# There is one small difference between this approach and vanilla one
# Our markers are not exactly controlled by GUI.Flash-like component like WG does it, but just DisplayObject instances
# in one app
#
# If we used entire flash app as one marker (like vanilla game does it), then there would be more overhead caused
# by flash app create/destroy (GUI.WGCrosshairFlash itself is NOT an swf app, but something like "a part" of it, but
# it still prints create/destroy in logs due to GUI.addChild and GUI.delChild calls)
# Can't explain precisely what it is doing internally because code is not accessible
#
# Also, we can successfully add our flash component as a child to CrosshairPanelContainer, but can't remove it
# the same way it is done with GUI.WGCrosshairFlash
# For some reason it simply won't be removed and WILL cause crash when closing main battleCrosshairFlash app
#
# Maybe GUI.WGCrosshairFlash has "something hidden" that makes GUI.delChild(...) able
# to recognize it in GUI child list?
###########################################################

# gm_components
class _AS3GunMarkerProxy(object):

    def __init__(self, gunMarkerComponent):
        self.markerName = gunMarkerComponent.getName()

    def setDataProvider(self, dataProvider):
        DispersionReticleFlash.onMarkerDataProviderAttach(self.markerName, dataProvider)

    def clearDataProvider(self):
        DispersionReticleFlash.onMarkerDataProviderDetach(self.markerName)


# gm_components
class AS3GunMarkerComponent(GunMarkerComponent):

    def _createView(self, container):
        # imitate GUI.WGCrosshairFlash data provider methods
        return _AS3GunMarkerProxy(self)

    # because we can't add our markers to CrosshairPanelContainer GUI, we need
    # to skip those steps when adding/removing it from GunMarkerComponents
    #
    # the rest of the logic should stay the same to interpose into WG code as "normally" as possible

    def addView(self, container):
        if self._view is not None:
            _logger.error('GunMarkerComponent "%s" is already created.', self._name)
        else:
            self._view = self._createView(container)
            _logger.debug('GunMarkerComponent "%s" is created', self._name)
            if self._isActive:
                self._setupDataProvider()

    def removeView(self, container):
        if self._view is None:
            _logger.error('GunMarkerComponent "%s" is already removed.', self._name)
        else:
            self._clearDataProvider()
            self._view = None


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

GUN_MARKERS_PRIORITY += ReticleRegistry.CLIENT_DISPERSION.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.SERVER_DISPERSION.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.CLIENT_LATENCY.getMarkerNames()

GUN_MARKERS_PRIORITY += [
    _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME,
    _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME,
    _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME,
    _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME,
    _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME
]

GUN_MARKERS_PRIORITY += ReticleRegistry.SERVER_SIMPLE.getMarkerNames()


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
