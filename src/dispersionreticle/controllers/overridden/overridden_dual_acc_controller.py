from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController


# gun_marker_ctrl
class OverriddenDualAccGunMarkerController(OverriddenDefaultGunMarkerController):

    # WG specific
    # it won't be called on Lesta client
    def _getMarkerSize(self, gunMarkerInfo):
        return gunMarkerInfo.dualAccSize

    def _replayReader(self, replayCtrl):
        return replayCtrl.getDualAccMarkerSize

    def _replayWriter(self, replayCtrl):
        return replayCtrl.setDualAccMarkerSize
