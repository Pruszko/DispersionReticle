from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.server.server_default_controller import ServerDefaultGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


# gun_marker_ctrl
class ExtendedServerDefaultGunMarkerController(ServerDefaultGunMarkerController):

    def __init__(self, reticle, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ExtendedServerDefaultGunMarkerController, self).__init__(reticle,
                                                                       dataProvider,
                                                                       enabledFlag=enabledFlag)

    def _interceptPostUpdate(self, size):
        if self.isServerController():
            DispersionReticleFlash.onReticleUpdate(self._reticle, size)
