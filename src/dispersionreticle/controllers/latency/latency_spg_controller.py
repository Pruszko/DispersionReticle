import BigWorld, BattleReplay
from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from dispersionreticle.controllers.standard.standard_spg_controller import OverriddenSPGGunMarkerController


# gun_marker_ctrl
class LatencySPGGunMarkerController(OverriddenSPGGunMarkerController):

    def __init__(self, reticle, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(LatencySPGGunMarkerController, self).__init__(reticle.gunMarkerType,
                                                            reticle.getSpgDataProvider(),
                                                            enabledFlag=enabledFlag)
        self.__serverDispersionAngle = None

    def _updateDispersionData(self):
        dispersionAngle = self._gunRotator.dispersionAngle
        if self.__serverDispersionAngle is not None:
            dispersionAngle = self.__serverDispersionAngle

        # here we avoid replay-specific code, it is handled by vanilla controllers
        # even if their markers may not be present

        self._dataProvider.setupConicDispersion(dispersionAngle)

    def setServerDispersionAngle(self, serverDispersionAngle):
        self.__serverDispersionAngle = serverDispersionAngle
