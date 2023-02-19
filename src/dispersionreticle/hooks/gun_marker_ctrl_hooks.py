from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory, _MARKER_TYPE

from dispersionreticle.controllers.gun_marker_decorator import \
    NewGunMarkersDecorator, \
    GUN_MARKER_TYPE_CLIENT_FOCUS, \
    GUN_MARKER_TYPE_SERVER_FOCUS
from dispersionreticle.controllers.gun_marker_default_controller import \
    NewDefaultGunMarkerController, \
    FocusGunMarkerController
from dispersionreticle.controllers.gun_marker_spg_controller import \
    NewSPGGunMarkerController, \
    FocusSPGGunMarkerController
from dispersionreticle.utils import *
from dispersionreticle.utils import version


###########################################################
# Return new decorator that includes new reticle controllers
#
# Basically, creates controllers of each markerType and provides them with proper
# data provider to communicate with crosshair flash component.
#
# Gun marker decorator manages all created controllers and forwards properly all methods
# related with them. Because decorator accepts only 2 controllers (vanilla client
# and server controllers), it is needed to provide custom decorator that handles
# new additional 2 controllers of dispersion reticles.
###########################################################

# gun_marker_ctrl
@overrideIn(gun_marker_ctrl)
def createGunMarker(func, isStrategic):
    factory = _GunMarkersDPFactory()
    if isStrategic:
        clientMarker = NewSPGGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientSPGProvider())
        serverMarker = NewSPGGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerSPGProvider())
        clientMarkerFocus = FocusSPGGunMarkerController(GUN_MARKER_TYPE_CLIENT_FOCUS, factory.getClientSPGFocusProvider())
        serverMarkerFocus = FocusSPGGunMarkerController(GUN_MARKER_TYPE_SERVER_FOCUS, factory.getServerSPGFocusProvider())
    else:
        clientMarker = NewDefaultGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientProvider())
        serverMarker = NewDefaultGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerProvider())
        clientMarkerFocus = FocusGunMarkerController(GUN_MARKER_TYPE_CLIENT_FOCUS, factory.getClientFocusProvider())
        serverMarkerFocus = FocusGunMarkerController(GUN_MARKER_TYPE_SERVER_FOCUS, factory.getServerFocusProvider())
    return NewGunMarkersDecorator(clientMarker, serverMarker, clientMarkerFocus, serverMarkerFocus)


@overrideIn(gun_marker_ctrl)
def useClientGunMarker(func):
    if version.isWithServerReticle():
        return True
    return func()


@overrideIn(gun_marker_ctrl)
def useDefaultGunMarkers(func):
    if version.isWithServerReticle():
        return False
    return func()
