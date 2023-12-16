from aih_constants import GUN_MARKER_TYPE
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _GunMarkersFactory

from dispersionreticle.utils import *
from dispersionreticle.utils.reticle_registry import ReticleRegistry


###########################################################
# Adds data providers for each reticle type
#
# This is done by reticles in ReticleRegistry.
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
# - prepare data providers (and their singleton getters) that will be used to write data by controllers,
# - in ReticleRegistry, add descriptor getters of data providers for each registered reticle
#
# Also, make getters of providers return proper data provider for new marker types
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
    else:
        if markerType is GUN_MARKER_TYPE.CLIENT:
            return self._markersInfo.clientMarkerDataProvider
        if markerType is GUN_MARKER_TYPE.DUAL_ACC:
            return self._markersInfo.dualAccMarkerDataProvider

    for reticle in ReticleRegistry.ADDITIONAL_RETICLES:
        if markerType == reticle.getGunMarkerType():
            return reticle.getStandardDataProvider()


# gm_factory
@overrideIn(_GunMarkersFactory)
def _getSPGDataProvider(func, self, markerType):
    if markerType is GUN_MARKER_TYPE.SERVER:
        return self._markersInfo.serverSPGMarkerDataProvider
    else:
        if markerType is GUN_MARKER_TYPE.CLIENT:
            return self._markersInfo.clientSPGMarkerDataProvider

    for reticle in ReticleRegistry.ADDITIONAL_RETICLES:
        if markerType == reticle.getGunMarkerType():
            return reticle.getSpgDataProvider()
