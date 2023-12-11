from aih_constants import GUN_MARKER_TYPE
from gui.battle_control.battle_constants import CROSSHAIR_VIEW_ID as _VIEW_ID
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import \
    _ControlMarkersFactory,\
    _OptionalMarkersFactory,\
    _EquipmentMarkersFactory
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from dispersionreticle.hooks.gun_marker_components_hooks import CustomGunMarkerComponent
from dispersionreticle.settings.config import g_configParams
from dispersionreticle.utils.reticle_registry import ReticleRegistry


###########################################################
# Linkages to certain gun markers (to their properties like color)
# can be reused, so it is only needed to make new names
# for new marker types.
#
# Linkages are selected same like vanilla markers (arcade focus -> arcade linkage etc.).
#
# Standard _ControlMarkersFactory (gm_factory) either instantiates or overrides
# crosshair flash component for each vehicle types (for ex. normal tanks needs
# only arcade and sniper reticle).
#
# For new gun markers, it is needed to instantiate crosshair flash component as well.
# Creation of markers internally uses linkages retrieved
# from _GUN_MARKER_LINKAGES (gm_factory) by marker name.
#
# Generally, this class is heavily if'ed up due to being heavily configurable, however I don't
# really have any idea how to write it better for now.
###########################################################

# gm_factory
class _NewControlMarkersFactory(_ControlMarkersFactory):

    def _createDefaultMarkers(self):
        markerType = self._getMarkerType()
        clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
        serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

        result = ()

        if self.areBothMarkersEnabled():
            if g_configParams.customServerReticleEnabled():
                result += ReticleRegistry.CUSTOM_SERVER_SERVER.createDefaultMarkers(self, markerType)
            if g_configParams.customHybridReticleEnabled():
                result += ReticleRegistry.CUSTOM_HYBRID_CLIENT.createDefaultMarkers(self, markerType)
            if g_configParams.customFocusedReticleEnabled():
                result += ReticleRegistry.CUSTOM_FOCUSED_CLIENT.createDefaultMarkers(self, markerType)

            if g_configParams.standardServerReticleEnabled():
                result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                           self._createSniperMarker(serverType, _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME))

            if g_configParams.standardHybridReticleEnabled():
                result += ReticleRegistry.STANDARD_HYBRID_CLIENT.createDefaultMarkers(self, markerType)

            if g_configParams.standardFocusedReticleEnabled():
                result += ReticleRegistry.STANDARD_FOCUSED_CLIENT.createDefaultMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += (self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                           self._createSniperMarker(clientType, _CONSTANTS.SNIPER_GUN_MARKER_NAME))
        else:
            if g_configParams.standardFocusedReticleEnabled():
                result += toFocusedReticle(markerType).createDefaultMarkers(self, markerType)
            if g_configParams.customFocusedReticleEnabled():
                result += toCustomFocusedReticle(markerType).createDefaultMarkers(self, markerType)

            result += (self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                       self._createSniperMarker(markerType, _CONSTANTS.SNIPER_GUN_MARKER_NAME))

        return result

    def _createSPGMarkers(self):
        markerType = self._getMarkerType()
        clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
        serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

        result = ()

        if self.areBothMarkersEnabled():
            # IMPORTANT
            # account for spg NOT TO create additional SPG marker when both reticles
            # of some type are enabled

            # server reticles
            if g_configParams.customServerReticleEnabled() and g_configParams.standardServerReticleEnabled():
                result += ReticleRegistry.CUSTOM_SERVER_SERVER.createArcadeOnlySPGMarkers(self, markerType)
                result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                           self._createSPGMarker(serverType, _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME))
            else:
                if g_configParams.customServerReticleEnabled():
                    result += ReticleRegistry.CUSTOM_SERVER_SERVER.createSPGMarkers(self, markerType)
                if g_configParams.standardServerReticleEnabled():
                    result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                               self._createSPGMarker(serverType, _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME))

            # hybrid reticles
            if g_configParams.customHybridReticleEnabled() and g_configParams.standardHybridReticleEnabled():
                result += ReticleRegistry.CUSTOM_HYBRID_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.STANDARD_HYBRID_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.customHybridReticleEnabled():
                    result += ReticleRegistry.CUSTOM_HYBRID_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.standardHybridReticleEnabled():
                    result += ReticleRegistry.STANDARD_HYBRID_CLIENT.createSPGMarkers(self, markerType)

            # focused reticles
            if g_configParams.customFocusedReticleEnabled() and g_configParams.standardFocusedReticleEnabled():
                result += ReticleRegistry.CUSTOM_FOCUSED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.STANDARD_FOCUSED_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.customFocusedReticleEnabled():
                    result += ReticleRegistry.CUSTOM_FOCUSED_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.standardFocusedReticleEnabled():
                    result += ReticleRegistry.STANDARD_FOCUSED_CLIENT.createSPGMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += (self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                           self._createSPGMarker(clientType, _CONSTANTS.SPG_GUN_MARKER_NAME))
        else:
            if g_configParams.standardFocusedReticleEnabled():
                result += toFocusedReticle(markerType).createSPGMarkers(self, markerType)
            if g_configParams.customFocusedReticleEnabled():
                result += toCustomFocusedReticle(markerType).createSPGMarkers(self, markerType)

            result += (self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                       self._createSPGMarker(markerType, _CONSTANTS.SPG_GUN_MARKER_NAME))

        return result

    # Lesta specific
    # on WG client it simply won't be called, because call to it doesn't exist
    # should be same as for SPGs
    def _createFlamethrowerMarkers(self):
        markerType = self._getMarkerType()
        clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
        serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

        result = ()

        if self.areBothMarkersEnabled():
            # IMPORTANT
            # account for spg NOT TO create additional SPG marker when
            # both reticles of some type are enabled

            # server reticles
            if g_configParams.customServerReticleEnabled() and g_configParams.standardServerReticleEnabled():
                result += ReticleRegistry.CUSTOM_SERVER_SERVER.createArcadeOnlySPGMarkers(self, markerType)
                result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                           self._createSPGMarker(serverType, _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME))
            else:
                if g_configParams.customServerReticleEnabled():
                    result += ReticleRegistry.CUSTOM_SERVER_SERVER.createSPGMarkers(self, markerType)
                if g_configParams.standardServerReticleEnabled():
                    result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                               self._createSPGMarker(serverType, _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME))

            # hybrid reticles
            if g_configParams.customHybridReticleEnabled() and g_configParams.standardHybridReticleEnabled():
                result += ReticleRegistry.CUSTOM_HYBRID_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.STANDARD_HYBRID_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.customHybridReticleEnabled():
                    result += ReticleRegistry.CUSTOM_HYBRID_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.standardHybridReticleEnabled():
                    result += ReticleRegistry.STANDARD_HYBRID_CLIENT.createSPGMarkers(self, markerType)

            # focused reticles
            if g_configParams.customFocusedReticleEnabled() and g_configParams.standardFocusedReticleEnabled():
                result += ReticleRegistry.CUSTOM_FOCUSED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.STANDARD_FOCUSED_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.customFocusedReticleEnabled():
                    result += ReticleRegistry.CUSTOM_FOCUSED_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.standardFocusedReticleEnabled():
                    result += ReticleRegistry.STANDARD_FOCUSED_CLIENT.createSPGMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += (self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                           self._createSPGMarker(clientType, _CONSTANTS.SPG_GUN_MARKER_NAME))
        else:
            if g_configParams.standardFocusedReticleEnabled():
                result += toFocusedReticle(markerType).createSPGMarkers(self, markerType)
            if g_configParams.customFocusedReticleEnabled():
                result += toCustomFocusedReticle(markerType).createSPGMarkers(self, markerType)

            result += (self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                       self._createSPGMarker(markerType, _CONSTANTS.SPG_GUN_MARKER_NAME))

        return result

    def _createDualGunMarkers(self):
        markerType = self._getMarkerType()
        clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
        serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

        result = ()

        if self.areBothMarkersEnabled():
            if g_configParams.customServerReticleEnabled():
                result += ReticleRegistry.CUSTOM_SERVER_SERVER.createDualGunMarkers(self, markerType)
            if g_configParams.customHybridReticleEnabled():
                result += ReticleRegistry.CUSTOM_HYBRID_CLIENT.createDualGunMarkers(self, markerType)
            if g_configParams.customFocusedReticleEnabled():
                result += ReticleRegistry.CUSTOM_FOCUSED_CLIENT.createDualGunMarkers(self, markerType)

            if g_configParams.standardServerReticleEnabled():
                result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME),
                           self._createSniperMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME))

            if g_configParams.standardHybridReticleEnabled():
                result += ReticleRegistry.STANDARD_HYBRID_CLIENT.createDualGunMarkers(self, markerType)

            if g_configParams.standardFocusedReticleEnabled():
                result += ReticleRegistry.STANDARD_FOCUSED_CLIENT.createDualGunMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += (self._createArcadeMarker(clientType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                           self._createSniperMarker(clientType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME))
        else:
            if g_configParams.standardFocusedReticleEnabled():
                result += toFocusedReticle(markerType).createDualGunMarkers(self, markerType)
            if g_configParams.customFocusedReticleEnabled():
                result += toCustomFocusedReticle(markerType).createDualGunMarkers(self, markerType)

            result += (self._createArcadeMarker(markerType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                       self._createSniperMarker(markerType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME))

        return result

    def areBothMarkersEnabled(self):
        return self._markersInfo.isClientMarkerActivated and self._markersInfo.isServerMarkerActivated

    def _createCustomArcadeMarker(self, markerType, name):
        dataProvider = self._getMarkerDataProvider(markerType)
        return self._createMarker(CustomGunMarkerComponent, _VIEW_ID.ARCADE, markerType, dataProvider, name)

    def _createCustomSniperMarker(self, markerType, name):
        dataProvider = self._getMarkerDataProvider(markerType)
        return self._createMarker(CustomGunMarkerComponent, _VIEW_ID.SNIPER, markerType, dataProvider, name)


def selectProperType(markerType, currentType):
    if currentType != GUN_MARKER_TYPE.UNDEFINED:
        return markerType
    return GUN_MARKER_TYPE.UNDEFINED


def toFocusedReticle(markerType):
    if markerType != GUN_MARKER_TYPE.UNDEFINED:
        if markerType == GUN_MARKER_TYPE.CLIENT:
            return ReticleRegistry.STANDARD_FOCUSED_CLIENT
        return ReticleRegistry.STANDARD_FOCUSED_SERVER

    return ReticleRegistry.STANDARD_FOCUSED_CLIENT


def toCustomFocusedReticle(markerType):
    if markerType != GUN_MARKER_TYPE.UNDEFINED:
        if markerType == GUN_MARKER_TYPE.CLIENT:
            return ReticleRegistry.CUSTOM_FOCUSED_CLIENT
        return ReticleRegistry.CUSTOM_FOCUSED_SERVER

    return ReticleRegistry.CUSTOM_FOCUSED_CLIENT


def shouldHideStandardReticle():
    return g_configParams.standardHybridReticleEnabled() and g_configParams.standardHybridReticleHideStandardReticle()


# It is needed to be overridden manually.
# Especially, first one in tuple is responsible for marker's instantiation.
gm_factory._FACTORIES_COLLECTION = (_NewControlMarkersFactory, _OptionalMarkersFactory, _EquipmentMarkersFactory)
