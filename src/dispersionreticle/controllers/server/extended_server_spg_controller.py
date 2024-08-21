from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.server.server_spg_controller import ServerSPGGunMarkerController
from dispersionreticle.flash.dispersion_reticle_flash import DispersionReticleFlash


# gun_marker_ctrl
class ExtendedServerSPGGunMarkerController(ServerSPGGunMarkerController):

    def __init__(self, reticle, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ExtendedServerSPGGunMarkerController, self).__init__(reticle,
                                                                   dataProvider,
                                                                   enabledFlag=enabledFlag)

    def _interceptPostUpdate(self, size):
        if self.isServerController():
            DispersionReticleFlash.onReticleUpdate(self._reticle, size)

    def _interceptReplayLogic(self, dispersionAngle):
        return dispersionAngle
