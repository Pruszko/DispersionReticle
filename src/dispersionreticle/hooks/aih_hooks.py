import AvatarInputHandler
from AvatarInputHandler import _GUN_MARKER_TYPE

from dispersionreticle.utils import *
from dispersionreticle.utils.gun_marker_type import *


###########################################################
# AvatarInputHandler hooks
# Needed to invoke update method on gun markers of new markerType
#
# Basically, AvatarInputHandler invokes updateGunMarker
# method on currently selected control mode (control_modes.py)
# which then invokes update on gun marker decorator (gun_marker_ctrl.py)
# that manages individual markers.
#
# Without this override, client and server focus gun markers
# wouldn't be updated.
#
# Notes:
# - Every control mode related to gun markers (there are few of them) has their own gun marker decorator.
###########################################################

@overrideIn(AvatarInputHandler.AvatarInputHandler)
def updateGunMarker(func, self, pos, direction, size, relaxTime, collData):
    self._AvatarInputHandler__curCtrl.updateGunMarker(AvatarInputHandler._GUN_MARKER_TYPE.CLIENT,
                                                      pos, direction, size, relaxTime, collData)
    self._AvatarInputHandler__curCtrl.updateGunMarker(GUN_MARKER_TYPE_CLIENT_FOCUS,
                                                      pos, direction, size, relaxTime, collData)
    self._AvatarInputHandler__curCtrl.updateGunMarker(GUN_MARKER_TYPE_CLIENT_LATENCY,
                                                      pos, direction, size, relaxTime, collData)


@overrideIn(AvatarInputHandler.AvatarInputHandler)
def updateGunMarker2(func, self, pos, direction, size, relaxTime, collData):
    self._AvatarInputHandler__curCtrl.updateGunMarker(_GUN_MARKER_TYPE.SERVER,
                                                      pos, direction, size, relaxTime, collData)
    self._AvatarInputHandler__curCtrl.updateGunMarker(GUN_MARKER_TYPE_SERVER_FOCUS,
                                                      pos, direction, size, relaxTime, collData)
