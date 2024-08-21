from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController


# gun_marker_ctrl
class ServerDefaultGunMarkerController(OverriddenDefaultGunMarkerController):

    def __init__(self, reticle, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(ServerDefaultGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                               dataProvider,
                                                               reticle.isServerReticle(),
                                                               enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptReplayLogic(self, size):
        return size
