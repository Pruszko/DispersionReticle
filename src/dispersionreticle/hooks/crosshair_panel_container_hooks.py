from gui.Scaleform.daapi.view.battle.shared.crosshair import CrosshairPanelContainer, gm_factory
from debug_utils import LOG_WARNING

from dispersionreticle.utils import overrideIn


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
