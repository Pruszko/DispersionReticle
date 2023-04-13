import BattleReplay
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory, _MARKER_TYPE
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

from dispersionreticle.controllers.gun_marker_decorator import NewGunMarkersDecorator
from dispersionreticle.controllers.standard.standard_default_controller import OverriddenDefaultGunMarkerController
from dispersionreticle.controllers.standard.standard_spg_controller import OverriddenSPGGunMarkerController
from dispersionreticle.controllers.dispersion.dispersion_default_controller import DispersionDefaultGunMarkerController
from dispersionreticle.controllers.dispersion.dispersion_spg_controller import DispersionSPGGunMarkerController
from dispersionreticle.controllers.latency.latency_default_controller import LatencyDefaultGunMarkerController
from dispersionreticle.controllers.latency.latency_spg_controller import LatencySPGGunMarkerController

from dispersionreticle.settings.config import g_config
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

    dispersionClientReticle = ReticleRegistry.CLIENT_FOCUS
    dispersionServerReticle = ReticleRegistry.SERVER_FOCUS
    latencyClientReticle = ReticleRegistry.CLIENT_LATENCY

    if isStrategic:
        clientMarker = OverriddenSPGGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientSPGProvider())
        serverMarker = OverriddenSPGGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerSPGProvider())

        dispersionClientMarker = DispersionSPGGunMarkerController(dispersionClientReticle)
        dispersionServerMarker = DispersionSPGGunMarkerController(dispersionServerReticle)

        latencyClientMarker = LatencySPGGunMarkerController(latencyClientReticle)
    else:
        clientMarker = OverriddenDefaultGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientProvider())
        serverMarker = OverriddenDefaultGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerProvider())

        dispersionClientMarker = DispersionDefaultGunMarkerController(dispersionClientReticle)
        dispersionServerMarker = DispersionDefaultGunMarkerController(dispersionServerReticle)

        latencyClientMarker = LatencyDefaultGunMarkerController(latencyClientReticle)

    return NewGunMarkersDecorator(clientMarker, serverMarker,
                                  dispersionClientMarker, dispersionServerMarker,
                                  latencyClientMarker)


@overrideIn(gun_marker_ctrl)
def useServerGunMarker(func):
    replayCtrl = BattleReplay.g_replayCtrl
    if replayCtrl.isPlaying:
        return False

    settingsCore = dependency.instance(ISettingsCore)

    if g_config.isServerAimRequired():
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
