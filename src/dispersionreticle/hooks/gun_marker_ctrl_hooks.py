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

# gun_marker_ctrl
@overrideIn(gun_marker_ctrl)
def createGunMarker(func, isStrategic):
    return createStrategicGunMarkers() if isStrategic else createDefaultGunMarkers()


def createStrategicGunMarkers():
    factory = _GunMarkersDPFactory()

    clientController = OverriddenSPGGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientSPGProvider())
    serverController = OverriddenSPGGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerSPGProvider())

    # this is what WG wrote
    # I hope it won't collapse universe or something
    dualAccController = _EmptyGunMarkerController(_MARKER_TYPE.UNDEFINED, None)

    focusedClientController = FocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_CLIENT)
    focusedServerController = FocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_SERVER)

    hybridClientController = HybridSPGGunMarkerController(ReticleRegistry.HYBRID_CLIENT)
    hybridExtendedClientController = ExtendedHybridSPGGunMarkerController(ReticleRegistry.HYBRID_EXTENDED_CLIENT)

    focusedExtendedClientController = ExtendedFocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_CLIENT)
    focusedExtendedServerController = ExtendedFocusedSPGGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_SERVER)

    serverExtendedServerController = ExtendedServerSPGGunMarkerController(ReticleRegistry.SERVER_EXTENDED_SERVER)

    return DispersionGunMarkersDecorator(clientController, serverController, dualAccController,
                                         focusedClientController, focusedServerController,
                                         hybridClientController, hybridExtendedClientController,
                                         focusedExtendedClientController, focusedExtendedServerController,
                                         serverExtendedServerController)


def createDefaultGunMarkers():
    factory = _GunMarkersDPFactory()

    clientController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientProvider())
    serverController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerProvider())
    dualAccController = OverriddenDualAccGunMarkerController(_MARKER_TYPE.DUAL_ACC, factory.getDualAccuracyProvider())

    focusedClientController = FocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_CLIENT)
    focusedServerController = FocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_SERVER)

    hybridClientController = HybridDefaultGunMarkerController(ReticleRegistry.HYBRID_CLIENT)
    hybridExtendedClientController = ExtendedHybridDefaultGunMarkerController(ReticleRegistry.HYBRID_EXTENDED_CLIENT)

    focusedExtendedClientController = ExtendedFocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_CLIENT)
    focusedExtendedServerController = ExtendedFocusedDefaultGunMarkerController(ReticleRegistry.FOCUSED_EXTENDED_SERVER)

    serverExtendedServerController = ExtendedServerDefaultGunMarkerController(ReticleRegistry.SERVER_EXTENDED_SERVER)

    return DispersionGunMarkersDecorator(clientController, serverController, dualAccController,
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
