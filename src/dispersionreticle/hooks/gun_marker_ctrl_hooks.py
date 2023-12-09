import BattleReplay
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory, _MARKER_TYPE, _EmptyGunMarkerController
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

from dispersionreticle.controllers.gun_marker_decorator import NewGunMarkersDecorator
from dispersionreticle.controllers.simple.as3_default_controller import AS3DefaultGunMarkerController
from dispersionreticle.controllers.simple.as3_spg_controller import AS3SPGGunMarkerController
from dispersionreticle.controllers.standard.standard_default_controller import OverriddenDefaultGunMarkerController
from dispersionreticle.controllers.standard.standard_dual_acc_controller import OverriddenDualAccGunMarkerController
from dispersionreticle.controllers.standard.standard_spg_controller import OverriddenSPGGunMarkerController
from dispersionreticle.controllers.dispersion.dispersion_default_controller import DispersionDefaultGunMarkerController
from dispersionreticle.controllers.dispersion.dispersion_spg_controller import DispersionSPGGunMarkerController
from dispersionreticle.controllers.latency.latency_default_controller import LatencyDefaultGunMarkerController
from dispersionreticle.controllers.latency.latency_spg_controller import LatencySPGGunMarkerController

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
    factory = _GunMarkersDPFactory()

    dispersionClientReticle = ReticleRegistry.CLIENT_DISPERSION
    dispersionServerReticle = ReticleRegistry.SERVER_DISPERSION

    latencyClientReticle = ReticleRegistry.CLIENT_LATENCY

    simpleServerReticle = ReticleRegistry.SERVER_SIMPLE

    if isStrategic:
        clientController = OverriddenSPGGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientSPGProvider())
        serverController = OverriddenSPGGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerSPGProvider())
        # this is what WG wrote
        # I hope it won't collapse universe or something
        dualAccController = _EmptyGunMarkerController(_MARKER_TYPE.UNDEFINED, None)

        dispersionClientController = DispersionSPGGunMarkerController(dispersionClientReticle)
        dispersionServerController = DispersionSPGGunMarkerController(dispersionServerReticle)

        latencyClientController = LatencySPGGunMarkerController(latencyClientReticle)

        simpleServerController = AS3SPGGunMarkerController(simpleServerReticle)
    else:
        clientController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientProvider())
        serverController = OverriddenDefaultGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerProvider())
        dualAccController = OverriddenDualAccGunMarkerController(_MARKER_TYPE.DUAL_ACC, factory.getDualAccuracyProvider())

        dispersionClientController = DispersionDefaultGunMarkerController(dispersionClientReticle)
        dispersionServerController = DispersionDefaultGunMarkerController(dispersionServerReticle)

        latencyClientController = LatencyDefaultGunMarkerController(latencyClientReticle)

        simpleServerController = AS3DefaultGunMarkerController(simpleServerReticle)

    return NewGunMarkersDecorator(clientController, serverController, dualAccController,
                                  dispersionClientController, dispersionServerController,
                                  latencyClientController,
                                  simpleServerController)


@overrideIn(gun_marker_ctrl)
def useServerGunMarker(func):
    replayCtrl = BattleReplay.g_replayCtrl
    if replayCtrl.isPlaying:
        return False

    settingsCore = dependency.instance(ISettingsCore)

    if g_configParams.latencyReticleEnabled() or \
            g_configParams.serverReticleEnabled() or \
            g_configParams.simpleServerReticleEnabled():
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
