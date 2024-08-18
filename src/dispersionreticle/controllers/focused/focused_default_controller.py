from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.focused import getFocusedDispersionSize
from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController


# gun_marker_ctrl
class FocusedDefaultGunMarkerController(OverriddenDefaultGunMarkerController):

    def __init__(self, reticle, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(FocusedDefaultGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                                dataProvider,
                                                                reticle.isServerReticle(),
                                                                enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptSize(self, size, pos, direction, relaxTime, collData):
        return getFocusedDispersionSize(pos)

    def _interceptReplayLogic(self, size):
        return size
