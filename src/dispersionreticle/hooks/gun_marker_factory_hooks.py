from aih_constants import GUN_MARKER_TYPE
from gui.battle_control.battle_constants import CROSSHAIR_VIEW_ID as _VIEW_ID
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import \
    _ControlMarkersFactory,\
    _OptionalMarkersFactory,\
    _EquipmentMarkersFactory

from dispersionreticle.hooks.gun_marker_components_hooks import ExtendedGunMarkerComponent
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

        result = ()

        if self.areBothMarkersEnabled():
            if g_configParams.serverReticleExtendedEnabled():
                result += ReticleRegistry.SERVER_EXTENDED_SERVER.createDefaultMarkers(self, markerType)
            if g_configParams.hybridReticleExtendedEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createDefaultMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createDefaultMarkers(self, markerType)

            if g_configParams.serverReticleEnabled():
                result += ReticleRegistry.DEBUG_SERVER.createDefaultMarkers(self, markerType)

            if g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_CLIENT.createDefaultMarkers(self, markerType)

            if g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_CLIENT.createDefaultMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createDefaultMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleEnabled():
                result += toFocusedReticle(markerType).createDefaultMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += toFocusedReticleExtended(markerType).createDefaultMarkers(self, markerType)

            result += toVanillaReticle(markerType).createDefaultMarkers(self, markerType)

        return result

    def _createSPGMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothMarkersEnabled():
            # IMPORTANT
            # account for spg NOT TO create additional SPG marker when both reticles
            # of some type are enabled

            # server reticles
            if g_configParams.serverReticleExtendedEnabled() and g_configParams.serverReticleEnabled():
                result += ReticleRegistry.SERVER_EXTENDED_SERVER.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.DEBUG_SERVER.createSPGMarkers(self, markerType)
            else:
                if g_configParams.serverReticleExtendedEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createSPGMarkers(self, markerType)
                if g_configParams.serverReticleEnabled():
                    result += ReticleRegistry.DEBUG_SERVER.createSPGMarkers(self, markerType)

            # hybrid reticles
            if g_configParams.hybridReticleExtendedEnabled() and g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.HYBRID_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.hybridReticleExtendedEnabled():
                    result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.hybridReticleEnabled():
                    result += ReticleRegistry.HYBRID_CLIENT.createSPGMarkers(self, markerType)

            # focused reticles
            if g_configParams.focusedReticleExtendedEnabled() and g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.FOCUSED_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.focusedReticleExtendedEnabled():
                    result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.focusedReticleEnabled():
                    result += ReticleRegistry.FOCUSED_CLIENT.createSPGMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createSPGMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleEnabled():
                result += toFocusedReticle(markerType).createSPGMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += toFocusedReticleExtended(markerType).createSPGMarkers(self, markerType)

            result += toVanillaReticle(markerType).createSPGMarkers(self, markerType)

        return result

    # Lesta specific
    # on WG client it simply won't be called, because call to it doesn't exist
    # should be same as for SPGs
    def _createFlamethrowerMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothMarkersEnabled():
            # IMPORTANT
            # account for spg NOT TO create additional SPG marker when
            # both reticles of some type are enabled

            # server reticles
            if g_configParams.serverReticleExtendedEnabled() and g_configParams.serverReticleEnabled():
                result += ReticleRegistry.SERVER_EXTENDED_SERVER.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.DEBUG_SERVER.createSPGMarkers(self, markerType)
            else:
                if g_configParams.serverReticleExtendedEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createSPGMarkers(self, markerType)
                if g_configParams.serverReticleEnabled():
                    result += ReticleRegistry.DEBUG_SERVER.createSPGMarkers(self, markerType)

            # hybrid reticles
            if g_configParams.hybridReticleExtendedEnabled() and g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.HYBRID_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.hybridReticleExtendedEnabled():
                    result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.hybridReticleEnabled():
                    result += ReticleRegistry.HYBRID_CLIENT.createSPGMarkers(self, markerType)

            # focused reticles
            if g_configParams.focusedReticleExtendedEnabled() and g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.FOCUSED_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.focusedReticleExtendedEnabled():
                    result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.focusedReticleEnabled():
                    result += ReticleRegistry.FOCUSED_CLIENT.createSPGMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createSPGMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleEnabled():
                result += toFocusedReticle(markerType).createSPGMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += toFocusedReticleExtended(markerType).createSPGMarkers(self, markerType)

            result += toVanillaReticle(markerType).createSPGMarkers(self, markerType)

        return result

    def _createDualGunMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothMarkersEnabled():
            if g_configParams.serverReticleExtendedEnabled():
                result += ReticleRegistry.SERVER_EXTENDED_SERVER.createDualGunMarkers(self, markerType)
            if g_configParams.hybridReticleExtendedEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createDualGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createDualGunMarkers(self, markerType)

            if g_configParams.serverReticleEnabled():
                result += ReticleRegistry.DEBUG_SERVER.createDualGunMarkers(self, markerType)

            if g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_CLIENT.createDualGunMarkers(self, markerType)

            if g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_CLIENT.createDualGunMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createDualGunMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleEnabled():
                result += toFocusedReticle(markerType).createDualGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += toFocusedReticleExtended(markerType).createDualGunMarkers(self, markerType)

            result += toVanillaReticle(markerType).createDualGunMarkers(self, markerType)

        return result

    def areBothMarkersEnabled(self):
        return self._markersInfo.isClientMarkerActivated and self._markersInfo.isServerMarkerActivated

    def _createExtendedArcadeMarker(self, markerType, name):
        dataProvider = self._getMarkerDataProvider(markerType)
        return self._createMarker(ExtendedGunMarkerComponent, _VIEW_ID.ARCADE, markerType, dataProvider, name)

    def _createExtendedSniperMarker(self, markerType, name):
        dataProvider = self._getMarkerDataProvider(markerType)
        return self._createMarker(ExtendedGunMarkerComponent, _VIEW_ID.SNIPER, markerType, dataProvider, name)


def selectProperType(markerType, currentType):
    if currentType != GUN_MARKER_TYPE.UNDEFINED:
        return markerType
    return GUN_MARKER_TYPE.UNDEFINED


def selectReticle(markerType, clientReticle, serverReticle):
    if markerType == GUN_MARKER_TYPE.SERVER:
        return serverReticle
    return clientReticle


def toVanillaReticle(markerType):
    return selectReticle(markerType, ReticleRegistry.VANILLA_CLIENT, ReticleRegistry.VANILLA_SERVER)


def toFocusedReticle(markerType):
    return selectReticle(markerType, ReticleRegistry.FOCUSED_CLIENT, ReticleRegistry.FOCUSED_SERVER)


def toFocusedReticleExtended(markerType):
    return selectReticle(markerType, ReticleRegistry.FOCUSED_EXTENDED_CLIENT, ReticleRegistry.FOCUSED_EXTENDED_SERVER)


def shouldHideStandardReticle():
    return g_configParams.hybridReticleEnabled() and g_configParams.hybridReticleHideStandardReticle()


# It is needed to be overridden manually.
# Especially, first one in tuple is responsible for marker's instantiation.
gm_factory._FACTORIES_COLLECTION = (_NewControlMarkersFactory, _OptionalMarkersFactory, _EquipmentMarkersFactory)
