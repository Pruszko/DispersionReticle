from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


# gun_marker_ctrl
class ExtendedServerDefaultGunMarkerController(OverriddenDefaultGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ExtendedServerDefaultGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                                       reticle.getStandardDataProvider(),
                                                                       enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptPostUpdate(self, size):
        DispersionReticleFlash.onReticleUpdate(self._reticle, size)

    def _interceptReplayLogic(self, size):
        return size
