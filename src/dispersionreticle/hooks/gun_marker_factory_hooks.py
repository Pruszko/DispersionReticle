import BattleReplay
from AvatarInputHandler import gun_marker_ctrl
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
#
# IMPORTANT
# When both client-side and server-side reticles are enabled, then
# controllers MUST only write server-side data.
# Otherwise, reticles in replays would be "jumpy".
###########################################################

# gm_factory
class _DispersionControlMarkersFactory(_ControlMarkersFactory):

    def _hasDualAccuracyMarkers(self):
        isClientMarkers = self._getMarkerType() == GUN_MARKER_TYPE.CLIENT
        shouldWriteDualAccToReplay = (not BattleReplay.g_replayCtrl.isServerAim)

        # when both client and server markers are enabled, then
        # - self._getMarkerType() returns GUN_MARKER_TYPE.SERVER
        # - BattleReplay.g_replayCtrl.isServerAim return True
        #
        # what normally prevents DUAL_ACC marker from displaying
        # even through client markers are visible and could display them (by WG logic)
        #
        # by this we will additionally allow
        # to display DUAL_ACC when both client and server markers are enabled
        #
        # controllers MUST NOT write DUAL_ACC data in such case even, if they are visible, because
        # - VehicleGunRotator in that state writes server data to replays,
        # - DUAL_ACC is client-side reticle (mixing client-side data with server-side data is bad)
        # and we don't want to change that logic
        #
        # this in result means, that replays would not display DUAL_ACC in replays,
        # and IT CAN'T, because standard reticle is server-side and DUAL_ACC is client-side
        # it would be messed up
        if self.areBothClientAndServerAimEnabled():
            isClientMarkers = True
            shouldWriteDualAccToReplay = True

        isClientMarkers = isClientMarkers and shouldWriteDualAccToReplay
        return isClientMarkers and self._vehicleInfo.isPlayerVehicle() and self._vehicleInfo.hasDualAccuracy()

    def _createDefaultMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothClientAndServerAimEnabled():
            if g_configParams.serverReticleExtendedEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createDefaultMarkers(self, markerType)
                else:
                    result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createDefaultMarkers(self, markerType)
            if g_configParams.hybridReticleExtendedEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createDefaultMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createDefaultMarkers(self, markerType)

            if g_configParams.serverReticleEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.DEBUG_SERVER.createDefaultMarkers(self, markerType)
                else:
                    result += ReticleRegistry.DEBUG_CLIENT.createDefaultMarkers(self, markerType)

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

        if self.areBothClientAndServerAimEnabled():
            # IMPORTANT
            # account for spg NOT TO create additional SPG marker when both reticles
            # of some type are enabled

            # server reticles
            if g_configParams.serverReticleExtendedEnabled() and g_configParams.serverReticleEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createArcadeOnlySPGMarkers(self, markerType)
                    result += ReticleRegistry.DEBUG_SERVER.createSPGMarkers(self, markerType)
                else:
                    result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                    result += ReticleRegistry.DEBUG_CLIENT.createSPGMarkers(self, markerType)
            else:
                if g_configParams.serverReticleExtendedEnabled():
                    if self.areBothFlagsEnabled():
                        result += ReticleRegistry.SERVER_EXTENDED_SERVER.createSPGMarkers(self, markerType)
                    else:
                        result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createSPGMarkers(self, markerType)
                if g_configParams.serverReticleEnabled():
                    if self.areBothFlagsEnabled():
                        result += ReticleRegistry.DEBUG_SERVER.createSPGMarkers(self, markerType)
                    else:
                        result += ReticleRegistry.DEBUG_CLIENT.createSPGMarkers(self, markerType)

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
            if g_configParams.focusedReticleExtendedEnabled() and g_configParams.focusedReticleEnabled():
                result += toFocusedReticleExtended(markerType).createArcadeOnlySPGMarkers(self, markerType)
                result += toFocusedReticle(markerType).createSPGMarkers(self, markerType)
            else:
                if g_configParams.focusedReticleExtendedEnabled():
                    result += toFocusedReticleExtended(markerType).createSPGMarkers(self, markerType)
                if g_configParams.focusedReticleEnabled():
                    result += toFocusedReticle(markerType).createSPGMarkers(self, markerType)

            result += toVanillaReticle(markerType).createSPGMarkers(self, markerType)

        return result

    def _createDualGunMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothClientAndServerAimEnabled():
            if g_configParams.serverReticleExtendedEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createDualGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createDualGunMarkers(self, markerType)
            if g_configParams.hybridReticleExtendedEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createDualGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createDualGunMarkers(self, markerType)

            if g_configParams.serverReticleEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.DEBUG_SERVER.createDualGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.DEBUG_CLIENT.createDualGunMarkers(self, markerType)

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

    # WG specific
    # it won't be called on Lesta client
    # should be very similar to dual gun markers
    def _createTwinGunMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothClientAndServerAimEnabled():
            if g_configParams.serverReticleExtendedEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createTwinGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createTwinGunMarkers(self, markerType)
            if g_configParams.hybridReticleExtendedEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createTwinGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createTwinGunMarkers(self, markerType)

            if g_configParams.serverReticleEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.DEBUG_SERVER.createTwinGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.DEBUG_CLIENT.createTwinGunMarkers(self, markerType)

            if g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_CLIENT.createTwinGunMarkers(self, markerType)

            if g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_CLIENT.createTwinGunMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createTwinGunMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleEnabled():
                result += toFocusedReticle(markerType).createTwinGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += toFocusedReticleExtended(markerType).createTwinGunMarkers(self, markerType)

            result += toVanillaReticle(markerType).createTwinGunMarkers(self, markerType)

        return result

    # WG specific
    # it won't be called on Lesta client
    # should be very similar to dual gun markers
    def _createAccuracyGunMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothClientAndServerAimEnabled():
            if g_configParams.serverReticleExtendedEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createAccuracyGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createAccuracyGunMarkers(self, markerType)
            if g_configParams.hybridReticleExtendedEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createAccuracyGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createAccuracyGunMarkers(self, markerType)

            if g_configParams.serverReticleEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.DEBUG_SERVER.createAccuracyGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.DEBUG_CLIENT.createAccuracyGunMarkers(self, markerType)

            if g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_CLIENT.createAccuracyGunMarkers(self, markerType)

            if g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_CLIENT.createAccuracyGunMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createAccuracyGunMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleEnabled():
                result += toFocusedReticle(markerType).createAccuracyGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += toFocusedReticleExtended(markerType).createAccuracyGunMarkers(self, markerType)

            result += toVanillaReticle(markerType).createAccuracyGunMarkers(self, markerType)

        return result

    # WG specific
    # it won't be called on Lesta client
    # should be very similar to dual gun markers
    def _createChargeGunMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothClientAndServerAimEnabled():
            if g_configParams.serverReticleExtendedEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createChargeGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createChargeGunMarkers(self, markerType)
            if g_configParams.hybridReticleExtendedEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createChargeGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createChargeGunMarkers(self, markerType)

            if g_configParams.serverReticleEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.DEBUG_SERVER.createChargeGunMarkers(self, markerType)
                else:
                    result += ReticleRegistry.DEBUG_CLIENT.createChargeGunMarkers(self, markerType)

            if g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_CLIENT.createChargeGunMarkers(self, markerType)

            if g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_CLIENT.createChargeGunMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createChargeGunMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleEnabled():
                result += toFocusedReticle(markerType).createChargeGunMarkers(self, markerType)
            if g_configParams.focusedReticleExtendedEnabled():
                result += toFocusedReticleExtended(markerType).createChargeGunMarkers(self, markerType)

            result += toVanillaReticle(markerType).createChargeGunMarkers(self, markerType)

        return result

    # Lesta specific
    # _createFlamethrowerMarkers() calls our methods, so here we don't have to do anything

    # Lesta specific
    # it won't be called on WG client
    # should be very similar to SPG markers, but must use different spg marker factory method
    def _createAssaultSPGMarkers(self):
        markerType = self._getMarkerType()

        result = ()

        if self.areBothClientAndServerAimEnabled():
            # IMPORTANT
            # account for spg NOT TO create additional SPG marker when both reticles
            # of some type are enabled

            # server reticles
            if g_configParams.serverReticleExtendedEnabled() and g_configParams.serverReticleEnabled():
                if self.areBothFlagsEnabled():
                    result += ReticleRegistry.SERVER_EXTENDED_SERVER.createArcadeOnlySPGMarkers(self, markerType)
                    result += ReticleRegistry.DEBUG_SERVER.createAssaultSPGMarkers(self, markerType)
                else:
                    result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                    result += ReticleRegistry.DEBUG_CLIENT.createAssaultSPGMarkers(self, markerType)
            else:
                if g_configParams.serverReticleExtendedEnabled():
                    if self.areBothFlagsEnabled():
                        result += ReticleRegistry.SERVER_EXTENDED_SERVER.createAssaultSPGMarkers(self, markerType)
                    else:
                        result += ReticleRegistry.SERVER_EXTENDED_CLIENT.createAssaultSPGMarkers(self, markerType)
                if g_configParams.serverReticleEnabled():
                    if self.areBothFlagsEnabled():
                        result += ReticleRegistry.DEBUG_SERVER.createAssaultSPGMarkers(self, markerType)
                    else:
                        result += ReticleRegistry.DEBUG_CLIENT.createAssaultSPGMarkers(self, markerType)

            # hybrid reticles
            if g_configParams.hybridReticleExtendedEnabled() and g_configParams.hybridReticleEnabled():
                result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.HYBRID_CLIENT.createAssaultSPGMarkers(self, markerType)
            else:
                if g_configParams.hybridReticleExtendedEnabled():
                    result += ReticleRegistry.HYBRID_EXTENDED_CLIENT.createAssaultSPGMarkers(self, markerType)
                if g_configParams.hybridReticleEnabled():
                    result += ReticleRegistry.HYBRID_CLIENT.createAssaultSPGMarkers(self, markerType)

            # focused reticles
            if g_configParams.focusedReticleExtendedEnabled() and g_configParams.focusedReticleEnabled():
                result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createArcadeOnlySPGMarkers(self, markerType)
                result += ReticleRegistry.FOCUSED_CLIENT.createAssaultSPGMarkers(self, markerType)
            else:
                if g_configParams.focusedReticleExtendedEnabled():
                    result += ReticleRegistry.FOCUSED_EXTENDED_CLIENT.createAssaultSPGMarkers(self, markerType)
                if g_configParams.focusedReticleEnabled():
                    result += ReticleRegistry.FOCUSED_CLIENT.createAssaultSPGMarkers(self, markerType)

            if not shouldHideStandardReticle():
                result += ReticleRegistry.VANILLA_CLIENT.createAssaultSPGMarkers(self, markerType)
        else:
            if g_configParams.focusedReticleExtendedEnabled() and g_configParams.focusedReticleEnabled():
                result += toFocusedReticleExtended(markerType).createArcadeOnlySPGMarkers(self, markerType)
                result += toFocusedReticle(markerType).createAssaultSPGMarkers(self, markerType)
            else:
                if g_configParams.focusedReticleExtendedEnabled():
                    result += toFocusedReticleExtended(markerType).createAssaultSPGMarkers(self, markerType)
                if g_configParams.focusedReticleEnabled():
                    result += toFocusedReticle(markerType).createAssaultSPGMarkers(self, markerType)

            result += toVanillaReticle(markerType).createAssaultSPGMarkers(self, markerType)

        return result

    @staticmethod
    def areBothClientAndServerAimEnabled():
        return gun_marker_ctrl.useClientGunMarker() and gun_marker_ctrl.useServerGunMarker()

    def areBothFlagsEnabled(self):
        return self._markersInfo.isClientMarkerActivated and self._markersInfo.isServerMarkerActivated

    def _createExtendedArcadeMarker(self, markerType, name):
        dataProvider = self._getMarkerDataProvider(markerType)
        return self._createMarker(ExtendedGunMarkerComponent, _VIEW_ID.ARCADE, markerType, dataProvider, name)

    def _createExtendedSniperMarker(self, markerType, name):
        dataProvider = self._getMarkerDataProvider(markerType)
        return self._createMarker(ExtendedGunMarkerComponent, _VIEW_ID.SNIPER, markerType, dataProvider, name)


# this will be a very late comment, but
# those methods below resolves quite an interesting "feature" of vanilla marker visibility handling
#
# it initially took me over 2 weeks of reverse engineering it to understand what's going on
# around 3 years ago since making this comment, when this mod was just 1-2 weeks old
#
# we cannot just display CLIENT markers, SERVER markers or any other type of reticle
# because if we did so, reticles would have been temporarily "displayed frozen" in the middle of the map
# during battle start countdown (they should be invisible during that period)
#
# why? maybe some methods for hiding/showing are not called?
# no, they for example do "that" (GunMarkerDecorator):
#
#     def setVisible(self, flag):
#         pass
#
# maybe you have to manually control gm_components.GunMarkerComponent
# and call setActive(...) or destroy()/create() ?
# no, that wouldn't be "vanilla behavior" way to handle that properly
#
# plus, GunMarkerComponent is almost completely isolated from gun marker controllers
# so that would need extremely tricky overrides even to do so
#
# so ... we have to create ALL markers with GUN_MARKER_TYPE.UNDEFINED
#
# yup
#
# all reticles during battle start countdown must be UNDEFINED
# and this is vanilla reticle behavior
#
# generally self._gunMarkerType() returns GUN_MARKER_TYPE.UNDEFINED during that period
# because both client and server flag in gunMarkerFlags are turned off
# and rest of vanilla code somehow doesn't collapse and handle this properly
#
# and we MUST follow this pattern to properly handle battle start countdown for our custom reticles

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
gm_factory._FACTORIES_COLLECTION = (_DispersionControlMarkersFactory, _OptionalMarkersFactory, _EquipmentMarkersFactory)
