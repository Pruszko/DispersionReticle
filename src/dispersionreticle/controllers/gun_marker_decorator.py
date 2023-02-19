# gun_marker_ctrl
import Math
from AvatarInputHandler import gun_marker_ctrl, aih_global_binding
from AvatarInputHandler.gun_marker_ctrl import IGunMarkerController, _BINDING_ID, _MARKER_TYPE, _MARKER_FLAG
from dispersionreticle.utils.gun_marker_type import *


# gun_marker_ctrl
class NewGunMarkersDecorator(IGunMarkerController):
    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)
    __clientState = aih_global_binding.bindRW(_BINDING_ID.CLIENT_GUN_MARKER_STATE)
    __serverState = aih_global_binding.bindRW(_BINDING_ID.SERVER_GUN_MARKER_STATE)

    def __init__(self, clientMarker, serverMarker, clientMarkerFocus, serverMarkerFocus):
        super(NewGunMarkersDecorator, self).__init__()
        self.__clientMarker = clientMarker
        self.__serverMarker = serverMarker
        self.__clientMarkerFocus = clientMarkerFocus
        self.__serverMarkerFocus = serverMarkerFocus

    def create(self):
        self.__clientMarker.create()
        self.__serverMarker.create()
        self.__clientMarkerFocus.create()
        self.__serverMarkerFocus.create()

    def destroy(self):
        self.__clientMarker.destroy()
        self.__serverMarker.destroy()
        self.__clientMarkerFocus.destroy()
        self.__serverMarkerFocus.destroy()

    def enable(self):
        self.__clientMarker.enable()
        self.__clientMarker.setPosition(self.__clientState[0])
        self.__serverMarker.enable()
        self.__serverMarker.setPosition(self.__serverState[0])
        self.__clientMarkerFocus.enable()
        self.__clientMarkerFocus.setPosition(self.__clientState[0])
        self.__serverMarkerFocus.enable()
        self.__serverMarkerFocus.setPosition(self.__serverState[0])

    def disable(self):
        self.__clientMarker.disable()
        self.__serverMarker.disable()
        self.__clientMarkerFocus.disable()
        self.__serverMarkerFocus.disable()

    def reset(self):
        self.__clientMarker.reset()
        self.__serverMarker.reset()
        self.__clientMarkerFocus.reset()
        self.__serverMarkerFocus.reset()

    def onRecreateDevice(self):
        self.__clientMarker.onRecreateDevice()
        self.__serverMarker.onRecreateDevice()
        self.__clientMarkerFocus.onRecreateDevice()
        self.__serverMarkerFocus.onRecreateDevice()

    def getPosition(self, markerType=_MARKER_TYPE.CLIENT):
        if markerType == _MARKER_TYPE.CLIENT:
            return self.__clientMarker.getPosition()
        if markerType == GUN_MARKER_TYPE_CLIENT_FOCUS:
            return self.__clientMarkerFocus.getPosition()
        if markerType == _MARKER_TYPE.SERVER:
            return self.__serverMarker.getPosition()
        if markerType == GUN_MARKER_TYPE_SERVER_FOCUS:
            return self.__serverMarkerFocus.getPosition()
        gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)
        return Math.Vector3()

    def setPosition(self, position, markerType=_MARKER_TYPE.CLIENT):
        if markerType == _MARKER_TYPE.CLIENT:
            self.__clientMarker.setPosition(position)
        elif markerType == GUN_MARKER_TYPE_CLIENT_FOCUS:
            self.__clientMarkerFocus.setPosition(position)
        elif markerType == _MARKER_TYPE.SERVER:
            self.__serverMarker.setPosition(position)
        elif markerType == GUN_MARKER_TYPE_SERVER_FOCUS:
            self.__serverMarkerFocus.setPosition(position)
        else:
            gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def setFlag(self, positive, bit):
        if positive:
            self.__gunMarkersFlags |= bit
            if bit == _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__serverMarker.setPosition(self.__clientMarker.getPosition())
                self.__serverMarker.setSize(self.__clientMarker.getSize())
                self.__serverMarkerFocus.setPosition(self.__clientMarkerFocus.getPosition())
                self.__serverMarkerFocus.setSize(self.__clientMarkerFocus.getSize())
        else:
            self.__gunMarkersFlags &= ~bit

    def update(self, markerType, position, direction, size, relaxTime, collData):
        if markerType == _MARKER_TYPE.CLIENT:
            self.__clientState = (
             position, direction, collData)
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__clientMarker.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == _MARKER_TYPE.SERVER:
            self.__serverState = (
             position, direction, collData)
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__serverMarker.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == GUN_MARKER_TYPE_CLIENT_FOCUS:
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__clientMarkerFocus.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == GUN_MARKER_TYPE_SERVER_FOCUS:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__serverMarkerFocus.update(markerType, position, direction, size, relaxTime, collData)
        else:
            gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def setVisible(self, flag):
        pass

    def getSize(self):
        return 0.0

    def setSize(self, newSize):
        pass
