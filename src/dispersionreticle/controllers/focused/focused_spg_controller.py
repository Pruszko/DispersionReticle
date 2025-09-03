from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.focused import getFocusedDispersionAngle, getFocusedDispersionSize
from dispersionreticle.controllers.overridden.overridden_spg_controller import OverriddenSPGGunMarkerController


# gun_marker_ctrl
class FocusedSPGGunMarkerController(OverriddenSPGGunMarkerController):

    def __init__(self, reticle, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(FocusedSPGGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                            dataProvider,
                                                            reticle.isServerReticle(),
                                                            enabledFlag=enabledFlag)
        self._reticle = reticle

    def _interceptSize(self, size, pos):
        return getFocusedDispersionSize(pos)

    def _interceptAngle(self, dispersionAngle):
        return getFocusedDispersionAngle()

    def _interceptReplayLogic(self, dispersionAngle):
        return dispersionAngle
