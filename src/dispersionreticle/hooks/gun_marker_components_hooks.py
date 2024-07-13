from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_components
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_components import GunMarkersComponents, GunMarkerComponent, \
    DefaultGunMarkerComponent
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash
from dispersionreticle.utils import *
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
# Because using custom ExtendedGunMarkerComponent we have control over how we will spawn our markers, we will
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
class _ExtendedGunMarkerProxy(object):

    def __init__(self, gunMarkerComponent):
        self._gunMarkerComponent = gunMarkerComponent

    def setDataProvider(self, dataProvider):
        DispersionReticleFlash.onMarkerDataProviderAttach(self._gunMarkerComponent.getName(), dataProvider)

    def clearDataProvider(self):
        DispersionReticleFlash.onMarkerDataProviderDetach(self._gunMarkerComponent.getName())


# gm_components
class ExtendedGunMarkerComponent(GunMarkerComponent):

    def _createView(self, container):
        # imitate GUI.WGCrosshairFlash data provider methods
        return _ExtendedGunMarkerProxy(self)

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

GUN_MARKERS_PRIORITY = []
GUN_MARKERS_PRIORITY += ReticleRegistry.VANILLA_CLIENT.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.VANILLA_SERVER.getMarkerNames()
GUN_MARKERS_PRIORITY += [
    _CONSTANTS.ARCADE_DUAL_ACC_GUN_MARKER_NAME,
    _CONSTANTS.SNIPER_DUAL_ACC_GUN_MARKER_NAME
]

GUN_MARKERS_PRIORITY += ReticleRegistry.HYBRID_CLIENT.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.FOCUSED_CLIENT.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.FOCUSED_SERVER.getMarkerNames()

GUN_MARKERS_PRIORITY += ReticleRegistry.DEBUG_SERVER.getMarkerNames()

GUN_MARKERS_PRIORITY += ReticleRegistry.HYBRID_EXTENDED_CLIENT.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.FOCUSED_EXTENDED_SERVER.getMarkerNames()
GUN_MARKERS_PRIORITY += ReticleRegistry.SERVER_EXTENDED_SERVER.getMarkerNames()


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


# WG specific
# AimDamageUI is not present on Lesta -> avoid fixing it there
@overrideIn(DefaultGunMarkerComponent, condition=isClientWG)
def _createView(func, self, container):
    wgCrosshairFlash = func(self, container)

    # EU WoT 1.25.1.0 added AimDamageUI object to GunMarker (and variants)
    # which holds ZoomingAimDamageUI with alpha == 1.0
    # which fades from 1.0 to 0.0 in around 0.5 second
    # (fading is probably done in invisible code in GUI.WGCrosshairFlash, because that logic is nowhere)
    #
    # this causes displaying a "yellow cross marker" of this object for that 0.5 second
    # immediately after gun marker is instantiated
    # and because markers are destroyed/created on auto-aiming in this mod, this yellow cross marker
    # would always be displayed on auto-aim clicking (which it shouldn't)
    #
    # in vanilla WoT it doesn't happen, because gun markers
    # are created ONLY ONCE and ONLY at the start of 30 sec battle countdown
    # and during that period they are invisible anyway, so bug is not displayed as well
    #
    # by this hacky override, we will forcefully set alpha = 0.0 to this object python-side
    # to immediately stop it from displaying after gun marker instantiation
    immediatelyFadeOutZoomingAimDamageUI(self._name, wgCrosshairFlash)

    return wgCrosshairFlash


def immediatelyFadeOutZoomingAimDamageUI(gunMarkerName, anyCrosshairFlash):
    # all paths taken from CROSSHAIR_ROOT_PATH and CROSSHAIR_ITEM_PATH_FORMAT
    # and battleCrosshairsApp.swf itself
    battleCrosshairsApp = anyCrosshairFlash.movie._level0.root

    # I don't believe that I would ever feel obligated
    # to explain 4 lines of code WITH 40 LINES of comments
    # because of how abnormal crosshairs app is
    #
    # those below commented lines of code at first might look like they work on gun markers
    # HOWEVER, nothing changes, it's like they exist there, changes are applied,
    # but "something" other is actually displayed, but not our changes
    #
    # I don't know why, I don't want to know why, and I don't want to know what is actually happening
    # but it initially took me like 3 days to partially find out
    # probably GUI.WGCrosshairFlash internally messes "main" prop
    # and magically CrosshairPanelContainer IS ACTUALLY there with ALL MARKERS
    # but in some fucking superposition or something
    # for some reason it is not the same as actual child of BattleCrosshairsApp (???)
    #
    # also, interesting fact, there are probably MANY CrosshairPanelContainer
    # however, in app's children, there exists only one
    # I don't know where the heck are the other panels and where they actually are in hierarchy, but
    # one of them (who knows which) is in "main" prop of BattleCrosshairsApp
    # with NOT SHOWING dispersion reticles BUT SOMEHOW displaying crosshair interface of the other panel (?????)
    # and the proper one holding dispersion reticles is in app's children probably with invisible panel (???????)
    #
    # what? why? or how? what happened?
    # the answer is - I don't know
    # I accidentally noticed that as "a little bit more transparent" crosshair interface
    # than it was before replay rewind when I was doing coloring tests with like 300 attempts of finding issue
    # those "redundant" panels are probably invisible or something
    # or visible?, I don't know what's happening to them

    # NOT WORKING SAMPLE CODE (changes are not applied, but gun markers and all its objects are magically present)
    # crosshairPanelContainer = battleCrosshairsApp.main
    #
    # gunMarker = getattr(crosshairPanelContainer, gunMarkerName)
    # gunMarker.aimDamage.zoomingAim.alpha = 0.0

    # A WORKAROUND WORKING CODE
    # instead of using "main" prop, we will access CrosshairPanelContainer
    # by simple loop of BattleCrosshairsApp children
    # again I don't know why and I don't want to know why this works
    # because "battleCrosshairsApp.numChildren" actually equals 1
    # "it just works"
    for childrenIndex in range(0, battleCrosshairsApp.numChildren):
        childCrosshairPanelContainer = battleCrosshairsApp.getChildAt(childrenIndex)

        # interesting DAAPI feature
        # you can access named DisplayObject added to containers by "prop request" call
        # GUI.WGCrosshairFlash uses it to access GunMarker instances in CrosshairPanelContainer
        # took me a longer time to actually notice that nuance
        gunMarker = getattr(childCrosshairPanelContainer, gunMarkerName)

        gunMarker.aimDamage.zoomingAim.alpha = 0.0
