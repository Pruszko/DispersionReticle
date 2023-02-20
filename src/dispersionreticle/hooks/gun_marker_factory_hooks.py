from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import \
    _ControlMarkersFactory,\
    _OptionalMarkersFactory,\
    _EquipmentMarkersFactory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _GUN_MARKER_LINKAGES
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from dispersionreticle.config import g_config
from dispersionreticle.utils.gun_marker_type import *


###########################################################
# Adds linkage for new reticles so they'll use default reticle
# This is needed due to components having unique name restriction.
#
# Linkages to certain gun markers (to their properties like color)
# can be reused, so it is only needed to make new unique names
# for new marker types for certain aiming mode (arcade, sniper, SPG,
# arcade dual, sniper dual)
#
# Linkages are selected same like vanilla markers (arcade focus -> arcade linkage etc).
#
# Without adding unique names, factories in gm_factory.py would mess up
# in providing proper data provider for certain markerType.
#
# Also, GunMarkerComponents (gm_components.py) would raise exception due to
# components not having unique names (it would mess up some of its methods
# without this restrictions since components are stored in dictionary by name).
###########################################################

ARCADE_FOCUS_GUN_MARKER_NAME = 'arcadeFocusGunMarker'
SNIPER_FOCUS_GUN_MARKER_NAME = 'sniperFocusGunMarker'
DUAL_FOCUS_GUN_ARCADE_MARKER_NAME = 'arcadeDualFocusGunMarker'
DUAL_FOCUS_GUN_SNIPER_MARKER_NAME = 'sniperDualFocusGunMarker'
SPG_FOCUS_GUN_MARKER_NAME = 'spgFocusGunMarker'

ARCADE_LATENCY_GUN_MARKER_NAME = 'arcadeLatencyGunMarker'
SNIPER_LATENCY_GUN_MARKER_NAME = 'sniperLatencyGunMarker'
DUAL_LATENCY_GUN_ARCADE_MARKER_NAME = 'arcadeDualLatencyGunMarker'
DUAL_LATENCY_GUN_SNIPER_MARKER_NAME = 'sniperDualLatencyGunMarker'
SPG_LATENCY_GUN_MARKER_NAME = 'spgLatencyGunMarker'

# gm_factory
_GUN_MARKER_LINKAGES.update({
    ARCADE_FOCUS_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    SNIPER_FOCUS_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    DUAL_FOCUS_GUN_ARCADE_MARKER_NAME: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
    DUAL_FOCUS_GUN_SNIPER_MARKER_NAME: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE,
    SPG_FOCUS_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_SPG_LINKAGE,

    ARCADE_LATENCY_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    SNIPER_LATENCY_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    DUAL_LATENCY_GUN_ARCADE_MARKER_NAME: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
    DUAL_LATENCY_GUN_SNIPER_MARKER_NAME: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE,
    SPG_LATENCY_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_SPG_LINKAGE
})


###########################################################
# Use new marker factory to create gun markers
#
# Standard _ControlMarkersFactory (gm_factory) either instantiates or overrides
# crosshair flash component for each vehicle types (for ex. normal tanks needs
# only arcade and sniper reticle).
#
# So, for new gun markers, it is needed to instantiate crosshair flash component as well.
# Creation of markers internally uses linkages retrieved
# from _GUN_MARKER_LINKAGES (gm_factory) by marker name.
###########################################################


# gm_factory
class _NewControlMarkersFactory(_ControlMarkersFactory):

    def _createDefaultMarkers(self):
        markerType = self._getMarkerType()

        if g_config.isServerReticleEnabled() or g_config.isLatencyReticleEnabled():
            clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)
            clientFocusType = selectProperType(GUN_MARKER_TYPE_CLIENT_FOCUS, markerType)
            clientLatencyType = selectProperType(GUN_MARKER_TYPE_CLIENT_LATENCY, markerType)

            if g_config.isDispersionReticleEnabled():
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createArcadeMarker(clientFocusType, ARCADE_FOCUS_GUN_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.SNIPER_GUN_MARKER_NAME),
                    self._createSniperMarker(clientFocusType, SNIPER_FOCUS_GUN_MARKER_NAME))
            else:
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.SNIPER_GUN_MARKER_NAME))

            if markerType == GUN_MARKER_TYPE.SERVER:
                if g_config.isServerReticleEnabled():
                    result += (
                        self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                        self._createSniperMarker(serverType, _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME))
                if g_config.isLatencyReticleEnabled():
                    result += (
                        self._createArcadeMarker(clientLatencyType, ARCADE_LATENCY_GUN_MARKER_NAME),
                        self._createSniperMarker(clientLatencyType, SNIPER_LATENCY_GUN_MARKER_NAME))

            return result

        if g_config.isDispersionReticleEnabled():
            focusMarkerType = toFocusGunMarkerType(markerType)
            return (
                self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                self._createArcadeMarker(focusMarkerType, ARCADE_FOCUS_GUN_MARKER_NAME),
                self._createSniperMarker(markerType, _CONSTANTS.SNIPER_GUN_MARKER_NAME),
                self._createSniperMarker(focusMarkerType, SNIPER_FOCUS_GUN_MARKER_NAME))

        return (
            self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
            self._createSniperMarker(markerType, _CONSTANTS.SNIPER_GUN_MARKER_NAME))

    def _createSPGMarkers(self):
        markerType = self._getMarkerType()

        if g_config.isServerReticleEnabled() or g_config.isLatencyReticleEnabled():
            clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)
            clientFocusType = selectProperType(GUN_MARKER_TYPE_CLIENT_FOCUS, markerType)
            clientLatencyType = selectProperType(GUN_MARKER_TYPE_CLIENT_LATENCY, markerType)

            if g_config.isDispersionReticleEnabled():
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createArcadeMarker(clientFocusType, ARCADE_FOCUS_GUN_MARKER_NAME),
                    self._createSPGMarker(clientType, _CONSTANTS.SPG_GUN_MARKER_NAME),
                    self._createSPGMarker(clientFocusType, SPG_FOCUS_GUN_MARKER_NAME))
            else:
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createSPGMarker(clientType, _CONSTANTS.SPG_GUN_MARKER_NAME))

            if markerType == GUN_MARKER_TYPE.SERVER:
                if g_config.isServerReticleEnabled():
                    result += (
                        self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                        self._createSPGMarker(serverType, _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME))
                if g_config.isLatencyReticleEnabled():
                    result += (
                        self._createArcadeMarker(clientLatencyType, ARCADE_LATENCY_GUN_MARKER_NAME),
                        self._createSPGMarker(clientLatencyType, SPG_LATENCY_GUN_MARKER_NAME))

            return result

        if g_config.isDispersionReticleEnabled():
            focusMarkerType = toFocusGunMarkerType(markerType)
            return (
                self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                self._createArcadeMarker(focusMarkerType, ARCADE_FOCUS_GUN_MARKER_NAME),
                self._createSPGMarker(markerType, _CONSTANTS.SPG_GUN_MARKER_NAME),
                self._createSPGMarker(focusMarkerType, SPG_FOCUS_GUN_MARKER_NAME))

        return (
            self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
            self._createSPGMarker(markerType, _CONSTANTS.SPG_GUN_MARKER_NAME))

    def _createDualGunMarkers(self):
        markerType = self._getMarkerType()

        if g_config.isServerReticleEnabled() or g_config.isLatencyReticleEnabled():
            clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)
            clientFocusType = selectProperType(GUN_MARKER_TYPE_CLIENT_FOCUS, markerType)
            clientLatencyType = selectProperType(GUN_MARKER_TYPE_CLIENT_LATENCY, markerType)

            if g_config.isDispersionReticleEnabled():
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                    self._createArcadeMarker(clientFocusType, DUAL_FOCUS_GUN_ARCADE_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME),
                    self._createSniperMarker(clientFocusType, DUAL_FOCUS_GUN_SNIPER_MARKER_NAME))
            else:
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME))

            if markerType == GUN_MARKER_TYPE.SERVER:
                if g_config.isServerReticleEnabled():
                    result += (
                        self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME),
                        self._createSniperMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME))
                if g_config.isLatencyReticleEnabled():
                    result += (
                        self._createArcadeMarker(clientLatencyType, DUAL_LATENCY_GUN_ARCADE_MARKER_NAME),
                        self._createSniperMarker(clientLatencyType, DUAL_LATENCY_GUN_SNIPER_MARKER_NAME))

            return result

        if g_config.isDispersionReticleEnabled():
            focusMarkerType = toFocusGunMarkerType(markerType)
            return (
                self._createArcadeMarker(markerType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                self._createArcadeMarker(focusMarkerType, DUAL_FOCUS_GUN_ARCADE_MARKER_NAME),
                self._createSniperMarker(markerType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME),
                self._createSniperMarker(focusMarkerType, DUAL_FOCUS_GUN_SNIPER_MARKER_NAME))

        return (
            self._createArcadeMarker(markerType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
            self._createSniperMarker(markerType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME))


def selectProperType(markerType, currentType):
    if currentType != GUN_MARKER_TYPE.UNDEFINED:
        return markerType
    return GUN_MARKER_TYPE.UNDEFINED


def toFocusGunMarkerType(markerType):
    if markerType != GUN_MARKER_TYPE.UNDEFINED:
        return markerType + FOCUS_MARKER_TYPE_OFFSET
    return GUN_MARKER_TYPE.UNDEFINED


# It is needed to be overridden manually.
# Especially, first one in tuple is responsible for marker's instantiation.
gm_factory._FACTORIES_COLLECTION = (_NewControlMarkersFactory, _OptionalMarkersFactory, _EquipmentMarkersFactory)
