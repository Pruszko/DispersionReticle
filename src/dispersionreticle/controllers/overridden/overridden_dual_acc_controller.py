from dispersionreticle.controllers.overridden.overridden_default_controller import OverriddenDefaultGunMarkerController


# gun_marker_ctrl
class OverriddenDualAccGunMarkerController(OverriddenDefaultGunMarkerController):

    def _replayReader(self, replayCtrl):
        return replayCtrl.getDualAccMarkerSize

    def _replayWriter(self, replayCtrl):
        return replayCtrl.setDualAccMarkerSize
