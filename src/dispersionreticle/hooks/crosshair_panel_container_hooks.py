from gui.Scaleform.daapi.view.battle.shared.crosshair import CrosshairPanelContainer, gm_factory
from debug_utils import LOG_WARNING
from gui.Scaleform.daapi.view.meta.CrosshairPanelContainerMeta import CrosshairPanelContainerMeta

from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash
from dispersionreticle.utils import overrideIn
from dispersionreticle.utils.reticle_registry import ReticleRegistry


###########################################################
# This is needed to maintain exact order of gun markers displayed
# in CrosshairPanelContainer.
#
# Normally, CrosshairPanelContainer would only clear those gun markers
# that are not present in new GunMarkersComponents, in effect, we wouldn't have
# control over order of gun marker rendering.
#
# This override will instead clear all current gun markers and recreate
# all of them in our order by getViewSettings().
###########################################################

@overrideIn(CrosshairPanelContainer)
def invalidateGunMarkers(func, self, markersInfo, vehicleInfo):
    if self._CrosshairPanelContainer__gunMarkers is None:
        LOG_WARNING('Set of gun markers is not created')
        return
    else:
        self._CrosshairPanelContainer__clearGunMarkers()

        newSet = gm_factory.createComponents(markersInfo, vehicleInfo)
        self._CrosshairPanelContainer__setGunMarkers(newSet)


###########################################################
# This is needed to redirect marker instantiation to our swf app instead
# of CrosshairPanelContainer when spawning simple markers.
#
# For more explanation, check gun_marker_components_hooks.py
###########################################################

@overrideIn(CrosshairPanelContainerMeta)
def as_createGunMarkerS(func, self, viewID, linkage, name):
    flashReticle = ReticleRegistry.getReticleByFlashMarkerName(name)
    if flashReticle:
        DispersionReticleFlash.onMarkerCreate(name, flashReticle)
        return True

    return func(self, viewID, linkage, name)


@overrideIn(CrosshairPanelContainerMeta)
def as_destroyGunMarkerS(func, self, name):
    flashReticle = ReticleRegistry.getReticleByFlashMarkerName(name)
    if flashReticle:
        DispersionReticleFlash.onMarkerDestroy(name, flashReticle)
        return True

    return func(self, name)
