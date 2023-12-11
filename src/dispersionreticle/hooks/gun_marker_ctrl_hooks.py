import BattleReplay
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory, _MARKER_TYPE, _EmptyGunMarkerController
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

from dispersionreticle.controllers.focused.custom_focused_default_controller import \
    CustomFocusedDefaultGunMarkerController
from dispersionreticle.controllers.focused.custom_focused_spg_controller import CustomFocusedSPGGunMarkerController
from dispersionreticle.controllers.gun_marker_decorator import DispersionGunMarkersDecorator
from dispersionreticle.controllers.hybrid.custom_hybrid_default_controller import CustomHybridDefaultGunMarkerController
from dispersionreticle.controllers.hybrid.custom_hybrid_spg_controller import CustomHybridSPGGunMarkerController
from dispersionreticle.controllers.server.custom_server_default_controller import CustomServerDefaultGunMarkerController
from dispersionreticle.controllers.server.custom_server_spg_controller import CustomServerSPGGunMarkerController
from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController
from dispersionreticle.controllers.overridden.overridden_dual_acc_controller import OverriddenDualAccGunMarkerController
from dispersionreticle.controllers.overridden.overridden_spg_controller import OverriddenSPGGunMarkerController
from dispersionreticle.controllers.focused.standard_focused_default_controller import StandardFocusedDefaultGunMarkerController
from dispersionreticle.controllers.focused.standard_focused_spg_controller import StandardFocusedSPGGunMarkerController
from dispersionreticle.controllers.hybrid.standard_hybrid_default_controller import StandardHybridDefaultGunMarkerController
from dispersionreticle.controllers.hybrid.standard_hybrid_spg_controller import StandardHybridSPGGunMarkerController

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

    standardFocusedClientController = StandardFocusedSPGGunMarkerController(ReticleRegistry.STANDARD_FOCUSED_CLIENT)
    standardFocusedServerController = StandardFocusedSPGGunMarkerController(ReticleRegistry.STANDARD_FOCUSED_SERVER)

    standardHybridClientController = StandardHybridSPGGunMarkerController(ReticleRegistry.STANDARD_HYBRID_CLIENT)
    customHybridClientController = CustomHybridSPGGunMarkerController(ReticleRegistry.CUSTOM_HYBRID_CLIENT)

    customFocusedClientController = CustomFocusedSPGGunMarkerController(ReticleRegistry.CUSTOM_FOCUSED_CLIENT)
    customFocusedServerController = CustomFocusedSPGGunMarkerController(ReticleRegistry.CUSTOM_FOCUSED_SERVER)

    customServerServerController = CustomServerSPGGunMarkerController(ReticleRegistry.CUSTOM_SERVER_SERVER)

    return DispersionGunMarkersDecorator(clientController, serverController, dualAccController,
                                         standardFocusedClientController, standardFocusedServerController,
                                         standardHybridClientController, customHybridClientController,
                                         customFocusedClientController, customFocusedServerController,
                                         customServerServerController)


def createDefaultGunMarkers():
    factory = _GunMarkersDPFactory()

    clientController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientProvider())
    serverController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerProvider())
    dualAccController = OverriddenDualAccGunMarkerController(_MARKER_TYPE.DUAL_ACC, factory.getDualAccuracyProvider())

    standardFocusedClientController = StandardFocusedDefaultGunMarkerController(ReticleRegistry.STANDARD_FOCUSED_CLIENT)
    standardFocusedServerController = StandardFocusedDefaultGunMarkerController(ReticleRegistry.STANDARD_FOCUSED_SERVER)

    standardHybridClientController = StandardHybridDefaultGunMarkerController(ReticleRegistry.STANDARD_HYBRID_CLIENT)
    customHybridClientController = CustomHybridDefaultGunMarkerController(ReticleRegistry.CUSTOM_HYBRID_CLIENT)

    customFocusedClientController = CustomFocusedDefaultGunMarkerController(ReticleRegistry.CUSTOM_FOCUSED_CLIENT)
    customFocusedServerController = CustomFocusedDefaultGunMarkerController(ReticleRegistry.CUSTOM_FOCUSED_SERVER)

    customServerServerController = CustomServerDefaultGunMarkerController(ReticleRegistry.CUSTOM_SERVER_SERVER)

    return DispersionGunMarkersDecorator(clientController, serverController, dualAccController,
                                         standardFocusedClientController, standardFocusedServerController,
                                         standardHybridClientController, customHybridClientController,
                                         customFocusedClientController, customFocusedServerController,
                                         customServerServerController)


@overrideIn(gun_marker_ctrl)
def useServerGunMarker(func):
    replayCtrl = BattleReplay.g_replayCtrl
    if replayCtrl.isPlaying:
        return False

    settingsCore = dependency.instance(ISettingsCore)

    if g_configParams.standardHybridReticleEnabled() or \
            g_configParams.customHybridReticleEnabled() or \
            g_configParams.standardServerReticleEnabled() or \
            g_configParams.customServerReticleEnabled():
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
