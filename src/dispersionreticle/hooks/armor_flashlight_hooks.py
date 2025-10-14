import AvatarInputHandler
from AvatarInputHandler import aih_global_binding
from aih_constants import GUN_MARKER_TYPE, GUN_MARKER_FLAG

from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.utils import overrideIn, isClientWG


class _Descriptors(object):
    gunMarkersFlags = aih_global_binding.bindRO(AvatarInputHandler._BINDING_ID.GUN_MARKERS_FLAGS)


_descriptors = _Descriptors()


def _areBothModesEnabled():
    return _isClientModeEnabled() and _isServerModeEnabled()


def _isClientModeEnabled():
    return _descriptors.gunMarkersFlags & GUN_MARKER_FLAG.CLIENT_MODE_ENABLED


def _isServerModeEnabled():
    return _descriptors.gunMarkersFlags & GUN_MARKER_FLAG.SERVER_MODE_ENABLED


if isClientWG():
    from gui.armor_flashlight.battle_controller import ArmorFlashlightBattleController
    from aih_constants import GunMarkerState

    # make sure to invoke armor flashlight state update only for vanilla client/server reticle
    # and only for server reticle, when both client and server reticles are displayed
    # otherwise, when "Use server aim" is checked (and in some condition even with unchecked),
    # armor flashlight starts flickering
    #
    # reproducible scenarios, when hook is not present:
    # - "Use server aim" is checked and at most focused reticle is enabled -> armor flashlight starts flickering
    # - "Use server aim" is unchecked and at most focused reticle is enabled -> armor flashlight is normal
    # - "Use server aim" is unchecked and some server reticle is enabled -> armor flashlight starts flickering
    #    but only during aim focusing - after aim focused, it stops flickering

    @overrideIn(ArmorFlashlightBattleController)
    def _updateVisibilityState(func, self, markerType, gunMarkerState, *args, **kwargs):
        # revert gunAimingCircleSize to original form, before being altered in gun marker decorator
        # by reticleSizeMultiplier, so armor flashlight stays independent of it
        reticleSizeMultiplier = g_configParams.reticleSizeMultiplier()
        if reticleSizeMultiplier >= 0.001:
            gunMarkerState = gunMarkerState  # type: GunMarkerState

            initialSize = gunMarkerState.size / reticleSizeMultiplier
            gunMarkerState = gunMarkerState._replace(size=initialSize)

        if _areBothModesEnabled():
            if markerType == GUN_MARKER_TYPE.SERVER:
                func(self, markerType, gunMarkerState, *args, **kwargs)
        else:
            if markerType == GUN_MARKER_TYPE.CLIENT or markerType == GUN_MARKER_TYPE.SERVER:
                func(self, markerType, gunMarkerState, *args, **kwargs)
