from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.overridden.overridden_spg_controller import OverriddenSPGGunMarkerController


# gun_marker_ctrl
class ServerSPGGunMarkerController(OverriddenSPGGunMarkerController):

    def __init__(self, reticle, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ServerSPGGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                           dataProvider,
                                                           reticle.isServerReticle(),
                                                           enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptReplayLogic(self, dispersionAngle):
        return dispersionAngle
