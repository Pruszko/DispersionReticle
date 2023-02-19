from AvatarInputHandler import aih_global_binding
from AvatarInputHandler.aih_global_binding import BINDING_ID, _DEFAULT_VALUES, _Observable
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _GunMarkersFactory
from gui.battle_control.controllers.crosshair_proxy import _GUN_MARKERS_SET_IDS, GunMarkersSetInfo

from dispersionreticle.utils import *
from dispersionreticle.utils.gun_marker_type import *

###########################################################
# Adds data providers for each reticle type
#
# Each reticle MUST have their own data provider.
# Otherwise, GUI.WGCrosshairFlash will complain with failing
# to assign data provider by raising an exception.
#
# Basically, gun marker controllers and factories uses them.
#
# Controllers provides data (positionMatrix, startSize, maybe something more)
# and factories assigns providers of them to GUI.WGCrosshairFlash object
# that uses them to update it's position and size.
#
# Can't tell exactly why crosshair flash components can't share
# certain data provider (exception message isn't precise
# and code of GUI modules isn't accessible), however
# an easy workaround is just providing unique data provider
# for each reticle type and just mimic data of vanilla data providers
# to the new ones.
#
# To do this:
# - register IDs of new data providers
#   in global AvatarInputHandler bindings and provide same default values
#   for them as vanilla data providers,
# - in _GunMarkersDPFactory (gun_marker_ctrl), add read-write access to
#   new providers that will be used to write data by controllers,
# - also, add singleton getters for each new data provider like for
#   vanilla ones,
# - in GunMarkersSetInfo (crosshair_proxy), add read-only access to
#   new providers that will be used by crosshair flash objects.
###########################################################

CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER = 6114
CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER = 6115
SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER = 6116
SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER = 6117

# aih_global_binding
BINDING_ID.RANGE += (
    CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER,
    CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER
)

# aih_global_binding
_DEFAULT_VALUES.update({
    CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None),
    CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None),
    SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None),
    SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None)
})

# crosshair_proxy
_GUN_MARKERS_SET_IDS += (
    CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER,
    CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER
)

# gun_marker_ctrl
_GunMarkersDPFactory._clientFocusDataProvider = aih_global_binding.bindRW(CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER)
_GunMarkersDPFactory._serverFocusDataProvider = aih_global_binding.bindRW(SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER)
_GunMarkersDPFactory._clientSPGFocusDataProvider = aih_global_binding.bindRW(CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)
_GunMarkersDPFactory._serverSPGFocusDataProvider = aih_global_binding.bindRW(SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)

# crosshair_proxy
GunMarkersSetInfo.clientMarkerFocusDataProvider = aih_global_binding.bindRO(CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER)
GunMarkersSetInfo.clientSPGMarkerFocusDataProvider = aih_global_binding.bindRO(CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)
GunMarkersSetInfo.serverMarkerFocusDataProvider = aih_global_binding.bindRO(SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER)
GunMarkersSetInfo.serverSPGMarkerFocusDataProvider = aih_global_binding.bindRO(SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getClientFocusProvider(self):
    if self._clientFocusDataProvider is None:
        self._clientFocusDataProvider = self._makeDefaultProvider()
    return self._clientFocusDataProvider


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getServerFocusProvider(self):
    if self._serverFocusDataProvider is None:
        self._serverFocusDataProvider = self._makeDefaultProvider()
    return self._serverFocusDataProvider


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getClientSPGFocusProvider(self):
    if self._clientSPGFocusDataProvider is None:
        self._clientSPGFocusDataProvider = self._makeSPGProvider()
    return self._clientSPGFocusDataProvider


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getServerSPGFocusProvider(self):
    if self._serverSPGFocusDataProvider is None:
        self._serverSPGFocusDataProvider = self._makeSPGProvider()
    return self._serverSPGFocusDataProvider


###########################################################
# Make getters of providers return proper data provider for new marker types
#
# It is needed, so an internal getter won't return None for new marker types.
# By this override, those methods can be reused without changing other methods
# that relies on it.
###########################################################

# gm_factory
@overrideIn(_GunMarkersFactory)
def _getMarkerDataProvider(func, self, markerType):
    if markerType is GUN_MARKER_TYPE.SERVER:
        return self._markersInfo.serverMarkerDataProvider
    if markerType is GUN_MARKER_TYPE_SERVER_FOCUS:
        return self._markersInfo.serverMarkerFocusDataProvider
    else:
        if markerType is GUN_MARKER_TYPE.CLIENT:
            return self._markersInfo.clientMarkerDataProvider
        if markerType is GUN_MARKER_TYPE_CLIENT_FOCUS:
            return self._markersInfo.clientMarkerFocusDataProvider
        return


# gm_factory
@overrideIn(_GunMarkersFactory)
def _getSPGDataProvider(func, self, markerType):
    if markerType is GUN_MARKER_TYPE.SERVER:
        return self._markersInfo.serverSPGMarkerDataProvider
    if markerType is GUN_MARKER_TYPE_SERVER_FOCUS:
        return self._markersInfo.serverSPGMarkerFocusDataProvider
    else:
        if markerType is GUN_MARKER_TYPE.CLIENT:
            return self._markersInfo.clientSPGMarkerDataProvider
        if markerType is GUN_MARKER_TYPE_CLIENT_FOCUS:
            return self._markersInfo.clientSPGMarkerFocusDataProvider
        return
