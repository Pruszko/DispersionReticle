from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.overridden.overridden_spg_controller import OverriddenSPGGunMarkerController


# gun_marker_ctrl
class HybridSPGGunMarkerController(OverriddenSPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(HybridSPGGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                           reticle.getSpgDataProvider(),
                                                           enabledFlag=enabledFlag)
        self._reticle = reticle
        self.__serverDispersionAngle = None

    def _interceptAngle(self, dispersionAngle):
        if self.__serverDispersionAngle is None:
            return dispersionAngle

        return self.__serverDispersionAngle

    def _interceptReplayLogic(self, dispersionAngle):
        return dispersionAngle

    def setServerDispersionAngle(self, serverDispersionAngle):
        self.__serverDispersionAngle = serverDispersionAngle
