import logging

from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import ShotResultIndicatorPlugin

from dispersionreticle.settings.config import g_config
from dispersionreticle.utils import *

logger = logging.getLogger(__name__)


###########################################################
# Adds hooks to invalidate gun marker pen indicators.
#
# Because we're invalidating entire gun marker set, old pen results
# are still in cache, so until different pen results arrives from gun marker decorator, they
# won't be applied to newly spawned vanilla gun marker pen indicators (which are red by default)
# until you move reticle out of tank armor (so pen results changes -> it will be applied to flash reticle component).
#
# This will clear internal cache when gun marker set changes, so next gun marker decorator update
# will immediately apply pen results to newly spawned reticles once even if it was the same previously.
###########################################################

@addMethodTo(ShotResultIndicatorPlugin)
def invalidateColorsCache(self, _=None):
    self._ShotResultIndicatorPlugin__cache.clear()


@overrideIn(ShotResultIndicatorPlugin)
def start(func, self):
    func(self)

    g_config.onConfigReload += self.invalidateColorsCache

    ctrl = self.sessionProvider.shared.crosshair
    if ctrl is not None:
        ctrl.onGunMarkersSetChanged += self.invalidateColorsCache


@overrideIn(ShotResultIndicatorPlugin)
def stop(func, self):
    ctrl = self.sessionProvider.shared.crosshair
    if ctrl is not None:
        ctrl.onGunMarkersSetChanged -= self.invalidateColorsCache

    g_config.onConfigReload -= self.invalidateColorsCache

    func(self)
