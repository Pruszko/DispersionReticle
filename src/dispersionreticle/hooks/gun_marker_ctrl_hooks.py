import BattleReplay
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory, _MARKER_TYPE, _EmptyGunMarkerController
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

from dispersionreticle.controllers.focused.extended_focused_default_controller import \
    ExtendedFocusedDefaultGunMarkerController
from dispersionreticle.controllers.focused.extended_focused_spg_controller import ExtendedFocusedSPGGunMarkerController
from dispersionreticle.controllers.gun_marker_decorator import DispersionGunMarkersDecorator
from dispersionreticle.controllers.hybrid.extended_hybrid_default_controller import ExtendedHybridDefaultGunMarkerController
from dispersionreticle.controllers.hybrid.extended_hybrid_spg_controller import ExtendedHybridSPGGunMarkerController
from dispersionreticle.controllers.server.extended_server_default_controller import ExtendedServerDefaultGunMarkerController
from dispersionreticle.controllers.server.extended_server_spg_controller import ExtendedServerSPGGunMarkerController
from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController
from dispersionreticle.controllers.overridden.overridden_dual_acc_controller import OverriddenDualAccGunMarkerController
from dispersionreticle.controllers.overridden.overridden_spg_controller import OverriddenSPGGunMarkerController
from dispersionreticle.controllers.focused.focused_default_controller import FocusedDefaultGunMarkerController
from dispersionreticle.controllers.focused.focused_spg_controller import FocusedSPGGunMarkerController
from dispersionreticle.controllers.hybrid.hybrid_default_controller import HybridDefaultGunMarkerController
from dispersionreticle.controllers.hybrid.hybrid_spg_controller import HybridSPGGunMarkerController

from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.utils import *
from dispersionreticle.utils.reticle_registry import ReticleRegistry


###########################################################
# Return new decorator that includes new reticle controllers
#
# Basically, creates controllers of each markerType and provides them with proper
# data provider to communicate with crosshair flash component.
#
# Gun marker decorator manages all created controllers and forwards properly all methods
# related with them. Because decorator accepts only 2 controllers (vanilla client
# and server controllers), it is needed to provide custom decorator that handles
# additional controllers for new reticles.
###########################################################

@overrideIn(gun_marker_ctrl, condition=isClientWG)
def createGunMarker(func, isStrategic):
    return createStrategicGunMarker() if isStrategic else createDefaultGunMarker()


# Lesta specific
#
# on WG client it will only be called as standard "helper" method
# on Lesta client it will become an override
@overrideIn(gun_marker_ctrl, condition=isClientLesta)
def createStrategicGunMarker(func=None):
    factory = _GunMarkersDPFactory()

    clientController = OverriddenSPGGunMarkerController(_MARKER_TYPE.CLIENT,
                                                        factory.getClientSPGProvider(),
                                                        False)
    serverController = OverriddenSPGGunMarkerController(_MARKER_TYPE.SERVER,
                                                        factory.getServerSPGProvider(),
                                                        True)

    # this is what WG wrote
    # I hope it won't collapse universe or something
    dualAccController = _EmptyGunMarkerController(_MARKER_TYPE.UNDEFINED, None)

    debugServerController = OverriddenSPGGunMarkerController(ReticleRegistry.DEBUG_SERVER.getGunMarkerType(),
                                                             ReticleRegistry.DEBUG_SERVER.getSpgDataProvider(),
                                                             True)

    focusedClientController = FocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_CLIENT,
                                                            ReticleRegistry.FOCUSED_CLIENT.getSpgDataProvider())
    focusedServerController = FocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_SERVER,
                                                            ReticleRegistry.FOCUSED_SERVER.getSpgDataProvider())

    hybridClientController = HybridSPGGunMarkerController(ReticleRegistry.HYBRID_CLIENT,
                                                          ReticleRegistry.HYBRID_CLIENT.getSpgDataProvider())
    hybridExtendedClientController = ExtendedHybridSPGGunMarkerController(ReticleRegistry.HYBRID_EXTENDED_CLIENT,
                                                                          ReticleRegistry.HYBRID_EXTENDED_CLIENT.getSpgDataProvider())

    focusedExtendedClientController = ExtendedFocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_CLIENT,
                                                                            ReticleRegistry.FOCUSED_EXTENDED_CLIENT.getSpgDataProvider())
    focusedExtendedServerController = ExtendedFocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_SERVER,
                                                                            ReticleRegistry.FOCUSED_EXTENDED_SERVER.getSpgDataProvider())

    serverExtendedServerController = ExtendedServerSPGGunMarkerController(ReticleRegistry.SERVER_EXTENDED_SERVER,
                                                                          ReticleRegistry.SERVER_EXTENDED_SERVER.getSpgDataProvider())

    return DispersionGunMarkersDecorator(clientController, serverController, dualAccController,
                                         debugServerController,
                                         focusedClientController, focusedServerController,
                                         hybridClientController, hybridExtendedClientController,
                                         focusedExtendedClientController, focusedExtendedServerController,
                                         serverExtendedServerController)


# Lesta specific
#
# on WG client it will only be called as standard "helper" method
# on Lesta client it will become an override
@overrideIn(gun_marker_ctrl, condition=isClientLesta)
def createDefaultGunMarker(func=None):
    factory = _GunMarkersDPFactory()

    clientController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.CLIENT,
                                                            factory.getClientProvider(),
                                                            False)
    serverController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.SERVER,
                                                            factory.getServerProvider(),
                                                            True)

    # mark DUAL_ACC as client-side reticle
    # this is awkward, but this value for this reticle in decorator is not used anyway
    dualAccController = OverriddenDualAccGunMarkerController(_MARKER_TYPE.DUAL_ACC,
                                                             factory.getDualAccuracyProvider(),
                                                             False)

    debugServerController = OverriddenDefaultGunMarkerController(ReticleRegistry.DEBUG_SERVER.getGunMarkerType(),
                                                                 ReticleRegistry.DEBUG_SERVER.getStandardDataProvider(),
                                                                 True)

    focusedClientController = FocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_CLIENT,
                                                                ReticleRegistry.FOCUSED_CLIENT.getStandardDataProvider())
    focusedServerController = FocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_SERVER,
                                                                ReticleRegistry.FOCUSED_SERVER.getStandardDataProvider())

    hybridClientController = HybridDefaultGunMarkerController(ReticleRegistry.HYBRID_CLIENT,
                                                              ReticleRegistry.HYBRID_CLIENT.getStandardDataProvider())
    hybridExtendedClientController = ExtendedHybridDefaultGunMarkerController(ReticleRegistry.HYBRID_EXTENDED_CLIENT,
                                                                              ReticleRegistry.HYBRID_EXTENDED_CLIENT.getStandardDataProvider())

    focusedExtendedClientController = ExtendedFocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_CLIENT,
                                                                                ReticleRegistry.FOCUSED_EXTENDED_CLIENT.getStandardDataProvider())
    focusedExtendedServerController = ExtendedFocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_SERVER,
                                                                                ReticleRegistry.FOCUSED_EXTENDED_SERVER.getStandardDataProvider())

    serverExtendedServerController = ExtendedServerDefaultGunMarkerController(ReticleRegistry.SERVER_EXTENDED_SERVER,
                                                                              ReticleRegistry.SERVER_EXTENDED_SERVER.getStandardDataProvider())

    return DispersionGunMarkersDecorator(clientController, serverController, dualAccController,
                                         debugServerController,
                                         focusedClientController, focusedServerController,
                                         hybridClientController, hybridExtendedClientController,
                                         focusedExtendedClientController, focusedExtendedServerController,
                                         serverExtendedServerController)


# Lesta specific
#
# on WG client it doesn't exist and won't be called
# on Lesta client it should be very similar to createStrategicGunMarker(), except
# it should use different data providers
@overrideIn(gun_marker_ctrl, condition=isClientLesta)
def createAssaultSpgGunMarker(func=None):
    factory = _GunMarkersDPFactory()

    clientController = OverriddenSPGGunMarkerController(_MARKER_TYPE.CLIENT,
                                                        factory.getClientAssaultSPGProvider(),
                                                        False)
    serverController = OverriddenSPGGunMarkerController(_MARKER_TYPE.SERVER,
                                                        factory.getServerAssaultSPGProvider(),
                                                        True)

    # this is what WG wrote
    # I hope it won't collapse universe or something
    dualAccController = _EmptyGunMarkerController(_MARKER_TYPE.UNDEFINED, None)

    debugServerController = OverriddenSPGGunMarkerController(ReticleRegistry.DEBUG_SERVER.getGunMarkerType(),
                                                             ReticleRegistry.DEBUG_SERVER.getAssaultSpgDataProvider(),
                                                             True)

    focusedClientController = FocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_CLIENT,
                                                            ReticleRegistry.FOCUSED_CLIENT.getAssaultSpgDataProvider())
    focusedServerController = FocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_SERVER,
                                                            ReticleRegistry.FOCUSED_SERVER.getAssaultSpgDataProvider())

    hybridClientController = HybridSPGGunMarkerController(ReticleRegistry.HYBRID_CLIENT,
                                                          ReticleRegistry.HYBRID_CLIENT.getAssaultSpgDataProvider())
    hybridExtendedClientController = ExtendedHybridSPGGunMarkerController(ReticleRegistry.HYBRID_EXTENDED_CLIENT,
                                                                          ReticleRegistry.HYBRID_EXTENDED_CLIENT.getAssaultSpgDataProvider())

    focusedExtendedClientController = ExtendedFocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_CLIENT,
                                                                            ReticleRegistry.FOCUSED_EXTENDED_CLIENT.getAssaultSpgDataProvider())
    focusedExtendedServerController = ExtendedFocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_SERVER,
                                                                            ReticleRegistry.FOCUSED_EXTENDED_SERVER.getAssaultSpgDataProvider())

    serverExtendedServerController = ExtendedServerSPGGunMarkerController(ReticleRegistry.SERVER_EXTENDED_SERVER,
                                                                          ReticleRegistry.SERVER_EXTENDED_SERVER.getAssaultSpgDataProvider())

    return DispersionGunMarkersDecorator(clientController, serverController, dualAccController,
                                         debugServerController,
                                         focusedClientController, focusedServerController,
                                         hybridClientController, hybridExtendedClientController,
                                         focusedExtendedClientController, focusedExtendedServerController,
                                         serverExtendedServerController)


@overrideIn(gun_marker_ctrl)
def useServerGunMarker(func):
    replayCtrl = BattleReplay.g_replayCtrl
    if replayCtrl.isPlaying:
        return False

    settingsCore = dependency.instance(ISettingsCore)

    if g_configParams.hybridReticleEnabled() or \
            g_configParams.hybridReticleExtendedEnabled() or \
            g_configParams.serverReticleEnabled() or \
            g_configParams.serverReticleExtendedEnabled():
        return True

    return settingsCore.getSetting('useServerAim')


@overrideIn(gun_marker_ctrl)
def useClientGunMarker(func):
    replayCtrl = BattleReplay.g_replayCtrl
    if replayCtrl.isPlaying:
        return True

    settingsCore = dependency.instance(ISettingsCore)

    return not settingsCore.getSetting('useServerAim')


@overrideIn(gun_marker_ctrl)
def useDefaultGunMarkers(func):
    # make VehicleGunRotator not hide client reticle when both reticle types are enabled
    if gun_marker_ctrl.useClientGunMarker() and gun_marker_ctrl.useServerGunMarker():
        return False
    return func()
