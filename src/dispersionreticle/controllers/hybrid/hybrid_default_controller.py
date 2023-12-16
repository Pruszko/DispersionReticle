from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController


# gun_marker_ctrl
class HybridDefaultGunMarkerController(OverriddenDefaultGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(HybridDefaultGunMarkerController, self).__init__(reticle.getGunMarkerType(),
                                                               reticle.getStandardDataProvider(),
                                                               reticle.isServerReticle(),
                                                               enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptReplayLogic(self, size):
        return size

    def setServerDispersionAngle(self, serverDispersionAngle):
        pass
