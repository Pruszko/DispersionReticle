from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.focused import getFocusedDispersionSize
from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController


# gun_marker_ctrl
class StandardFocusedDefaultGunMarkerController(OverriddenDefaultGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(StandardFocusedDefaultGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                                        reticle.getStandardDataProvider(),
                                                                        enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptSize(self, size, pos, direction, relaxTime, collData):
        return getFocusedDispersionSize(pos)

    def _interceptReplayLogic(self, size):
        return size
