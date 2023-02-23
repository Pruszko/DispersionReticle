from AvatarInputHandler import gun_marker_ctrl
from aih_constants import GUN_MARKER_TYPE
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import \
    _ControlMarkersFactory,\
    _OptionalMarkersFactory,\
    _EquipmentMarkersFactory
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from dispersionreticle.config import g_config
from dispersionreticle.utils.reticle_registry import ReticleRegistry


###########################################################
# Add linkages for new reticles so they'll use defined settings.
# This is needed due to components having unique name restriction.
#
# It is done by reticles in ReticleRegistry.
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
#
# So, create new marker factory to create gun markers.
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
        markerType = self._getBaseMarkerType()

        result = (self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                  self._createSniperMarker(markerType, _CONSTANTS.SNIPER_GUN_MARKER_NAME))

        if g_config.isDispersionReticleEnabled():
            result += toFocusReticle(markerType).createDefaultMarkers(self, markerType)

        if gun_marker_ctrl.useClientGunMarker() and gun_marker_ctrl.useServerGunMarker():
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

            if g_config.isServerReticleEnabled():
                result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                           self._createSniperMarker(serverType, _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME))
            if g_config.isLatencyReticleEnabled():
                result += ReticleRegistry.CLIENT_LATENCY.createDefaultMarkers(self, markerType)

        return result

    def _createSPGMarkers(self):
        markerType = self._getBaseMarkerType()

        result = (self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                  self._createSPGMarker(markerType, _CONSTANTS.SPG_GUN_MARKER_NAME))

        if g_config.isDispersionReticleEnabled():
            result += toFocusReticle(markerType).createSPGMarkers(self, markerType)

        if gun_marker_ctrl.useClientGunMarker() and gun_marker_ctrl.useServerGunMarker():
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

            if g_config.isServerReticleEnabled():
                result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                           self._createSPGMarker(serverType, _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME))
            if g_config.isLatencyReticleEnabled():
                result += ReticleRegistry.CLIENT_LATENCY.createSPGMarkers(self, markerType)

        return result

    def _createDualGunMarkers(self):
        markerType = self._getBaseMarkerType()

        result = (self._createArcadeMarker(markerType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                  self._createSniperMarker(markerType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME))

        if g_config.isDispersionReticleEnabled():
            result += toFocusReticle(markerType).createDualGunMarkers(self, markerType)

        if gun_marker_ctrl.useClientGunMarker() and gun_marker_ctrl.useServerGunMarker():
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

            if g_config.isServerReticleEnabled():
                result += (self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME),
                           self._createSniperMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME))
            if g_config.isLatencyReticleEnabled():
                result += ReticleRegistry.CLIENT_LATENCY.createDualGunMarkers(self, markerType)

        return result

    def _getBaseMarkerType(self):
        markerType = GUN_MARKER_TYPE.CLIENT

        if g_config.isServerAimEnabled():
            markerType = GUN_MARKER_TYPE.SERVER

        return selectProperType(markerType, self._getMarkerType())


def selectProperType(markerType, currentType):
    if currentType != GUN_MARKER_TYPE.UNDEFINED:
        return markerType
    return GUN_MARKER_TYPE.UNDEFINED


def toFocusReticle(markerType):
    if markerType != GUN_MARKER_TYPE.UNDEFINED:
        if markerType == GUN_MARKER_TYPE.CLIENT:
            return ReticleRegistry.CLIENT_FOCUS
        return ReticleRegistry.SERVER_FOCUS

    return ReticleRegistry.CLIENT_FOCUS


# It is needed to be overridden manually.
# Especially, first one in tuple is responsible for marker's instantiation.
gm_factory._FACTORIES_COLLECTION = (_NewControlMarkersFactory, _OptionalMarkersFactory, _EquipmentMarkersFactory)
