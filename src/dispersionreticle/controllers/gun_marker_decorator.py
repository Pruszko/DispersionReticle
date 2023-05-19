# gun_marker_ctrl
import BigWorld, Math
from AvatarInputHandler import gun_marker_ctrl, aih_global_binding, AimingSystems
from AvatarInputHandler.gun_marker_ctrl import IGunMarkerController, _BINDING_ID, _MARKER_TYPE, _MARKER_FLAG

from dispersionreticle.utils.reticle_registry import ReticleRegistry


# gun_marker_ctrl
class NewGunMarkersDecorator(IGunMarkerController):
    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)
    __clientState = aih_global_binding.bindRW(_BINDING_ID.CLIENT_GUN_MARKER_STATE)
    __serverState = aih_global_binding.bindRW(_BINDING_ID.SERVER_GUN_MARKER_STATE)

    def __init__(self,
                 clientMarker, serverMarker,
                 dispersionClientMarker, dispersionServerMarker,
                 latencyClientMarker,
                 pentagonServerMarker):
        super(NewGunMarkersDecorator, self).__init__()
        self.__clientMarker = clientMarker
        self.__serverMarker = serverMarker
        self.__dispersionClientMarker = dispersionClientMarker
        self.__dispersionServerMarker = dispersionServerMarker

        self.__latencyClientMarker = latencyClientMarker

        self.__simpleServerMarker = pentagonServerMarker

        self._allMarkers = [
            clientMarker, serverMarker,
            dispersionClientMarker, dispersionServerMarker,
            latencyClientMarker,
            pentagonServerMarker
        ]

        self.__serverSizeDispersion = None
        self.__serverDispersionAngle = None

    def create(self):
        for marker in self._allMarkers:
            marker.create()

    def destroy(self):
        for marker in self._allMarkers:
            marker.destroy()

    def enable(self):
        self.__clientMarker.enable()
        self.__clientMarker.setPosition(self.__clientState[0])
        self.__serverMarker.enable()
        self.__serverMarker.setPosition(self.__serverState[0])
        self.__dispersionClientMarker.enable()
        self.__dispersionClientMarker.setPosition(self.__clientState[0])
        self.__dispersionServerMarker.enable()
        self.__dispersionServerMarker.setPosition(self.__serverState[0])
        self.__latencyClientMarker.enable()
        self.__latencyClientMarker.setPosition(self.__clientState[0])
        self.__simpleServerMarker.enable()
        self.__simpleServerMarker.setPosition(self.__clientState[0])

    def disable(self):
        for marker in self._allMarkers:
            marker.disable()

    def reset(self):
        for marker in self._allMarkers:
            marker.reset()

    def onRecreateDevice(self):
        for marker in self._allMarkers:
            marker.onRecreateDevice()

    def getPosition(self, markerType=_MARKER_TYPE.CLIENT):
        for marker in self._allMarkers:
            if markerType == marker._gunMarkerType:
                return marker.getPosition()
        gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)
        return Math.Vector3()

    def setPosition(self, position, markerType=_MARKER_TYPE.CLIENT):
        for marker in self._allMarkers:
            if markerType == marker._gunMarkerType:
                marker.setPosition(position)
                return
        gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def setFlag(self, positive, bit):
        if positive:
            self.__gunMarkersFlags |= bit
            if bit == _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__serverMarker.setPosition(self.__clientMarker.getPosition())
                self.__serverMarker.setSize(self.__clientMarker.getSize())
                self.__dispersionServerMarker.setPosition(self.__dispersionClientMarker.getPosition())
                self.__dispersionServerMarker.setSize(self.__dispersionClientMarker.getSize())
                self.__latencyClientMarker.setPosition(self.__clientMarker.getPosition())
                self.__latencyClientMarker.setSize(self.__clientMarker.getSize())
                self.__simpleServerMarker.setPosition(self.__clientMarker.getPosition())
                self.__simpleServerMarker.setSize(self.__clientMarker.getSize())
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
                # collect server size dispersion for latency reticle
                self.__serverSizeDispersion = size
                if BigWorld.player() and BigWorld.player().gunRotator:
                    self.__serverDispersionAngle = BigWorld.player().gunRotator.dispersionAngle

                # scale it down to dispersion per 1m unit
                distance = getDistanceFromSniperViewport(position)
                if distance > 0.0:
                    self.__serverSizeDispersion = tuple(i / distance for i in size)

                self.__serverMarker.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.CLIENT_DISPERSION.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__dispersionClientMarker.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.SERVER_DISPERSION.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__dispersionServerMarker.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.CLIENT_LATENCY.gunMarkerType:
            # this has to be done outside controllers because we have to collect server reticle size
            # also, we will have delayed access to server size, so we need to wait
            # until GunMarkerComponent will provide server data
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                # first calls won't have ready server data yet
                # just display client size whenever it is not known
                # it also works well when rendering in replays because there server marker is not called
                if self.__serverSizeDispersion is not None and self.__serverDispersionAngle is not None:
                    # scale server size dispersion by distance for latency reticle
                    distance = getDistanceFromSniperViewport(position)
                    serverSize = tuple(i * distance for i in self.__serverSizeDispersion)

                    self.__latencyClientMarker.setServerDispersionAngle(self.__serverDispersionAngle)
                    self.__latencyClientMarker.update(markerType, position, direction, serverSize, relaxTime, collData)
                else:
                    self.__latencyClientMarker.setServerDispersionAngle(None)
                    self.__latencyClientMarker.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.SERVER_SIMPLE.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__simpleServerMarker.update(markerType, position, direction, size, relaxTime, collData)
        else:
            gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def setVisible(self, flag):
        pass

    def getSize(self):
        return 0.0

    def setSize(self, newSize):
        pass


def getDistanceFromSniperViewport(position):
    sniperViewportPos = getSniperViewportPosition()
    shotDir = position - sniperViewportPos
    return shotDir.length


def getSniperViewportPosition():
    gunRotator = BigWorld.player().gunRotator
    gunMatrix = AimingSystems.getPlayerGunMat(gunRotator.turretYaw, gunRotator.gunPitch)
    return gunMatrix.translation
