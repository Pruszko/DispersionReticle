# gun_marker_ctrl
import BigWorld, Math
from AvatarInputHandler import gun_marker_ctrl, aih_global_binding, AimingSystems
from AvatarInputHandler.gun_marker_ctrl import IGunMarkerController, _BINDING_ID, _MARKER_TYPE, _MARKER_FLAG

from dispersionreticle.utils import debug_state
from dispersionreticle.utils.debug_state import g_debugStateCollector
from dispersionreticle.utils.reticle_registry import ReticleRegistry


# gun_marker_ctrl
class NewGunMarkersDecorator(IGunMarkerController):
    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)
    __clientState = aih_global_binding.bindRW(_BINDING_ID.CLIENT_GUN_MARKER_STATE)
    __serverState = aih_global_binding.bindRW(_BINDING_ID.SERVER_GUN_MARKER_STATE)

    def __init__(self,
                 clientController, serverController,
                 dispersionClientController, dispersionServerController,
                 latencyClientController,
                 simpleServerController):
        super(NewGunMarkersDecorator, self).__init__()
        self.__clientController = clientController
        self.__serverController = serverController
        self.__dispersionClientController = dispersionClientController
        self.__dispersionServerController = dispersionServerController

        self.__latencyClientController = latencyClientController

        self.__simpleServerController = simpleServerController

        self._allControllers = [
            clientController, serverController,
            dispersionClientController, dispersionServerController,
            latencyClientController,
            simpleServerController
        ]

        self.__serverSizeDispersion = None
        self.__serverDispersionAngle = None

    def create(self):
        for controller in self._allControllers:
            controller.create()

    def destroy(self):
        for controller in self._allControllers:
            controller.destroy()

    def enable(self):
        self.__clientController.enable()
        self.__clientController.setPosition(self.__clientState[0])
        self.__serverController.enable()
        self.__serverController.setPosition(self.__serverState[0])

        self.__dispersionClientController.enable()
        self.__dispersionClientController.setPosition(self.__clientState[0])
        self.__dispersionServerController.enable()
        self.__dispersionServerController.setPosition(self.__serverState[0])

        self.__latencyClientController.enable()
        self.__latencyClientController.setPosition(self.__clientState[0])

        self.__simpleServerController.enable()
        self.__simpleServerController.setPosition(self.__serverState[0])

    def disable(self):
        for controller in self._allControllers:
            controller.disable()

    def reset(self):
        for controller in self._allControllers:
            controller.reset()

    def onRecreateDevice(self):
        for controller in self._allControllers:
            controller.onRecreateDevice()

    def getPosition(self, markerType=_MARKER_TYPE.CLIENT):
        for controller in self._allControllers:
            if markerType == controller._gunMarkerType:
                return controller.getPosition()
        gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)
        return Math.Vector3()

    def setPosition(self, position, markerType=_MARKER_TYPE.CLIENT):
        for controller in self._allControllers:
            if markerType == controller._gunMarkerType:
                controller.setPosition(position)
                return
        gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def setFlag(self, positive, bit):
        if positive:
            self.__gunMarkersFlags |= bit
            if bit == _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__serverController.setPosition(self.__clientController.getPosition())
                self.__serverController.setSize(self.__clientController.getSize())
                self.__dispersionServerController.setPosition(self.__dispersionClientController.getPosition())
                self.__dispersionServerController.setSize(self.__dispersionClientController.getSize())
                self.__latencyClientController.setPosition(self.__clientController.getPosition())
                self.__latencyClientController.setSize(self.__clientController.getSize())
                self.__simpleServerController.setPosition(self.__clientController.getPosition())
                self.__simpleServerController.setSize(self.__clientController.getSize())
        else:
            self.__gunMarkersFlags &= ~bit

    def update(self, markerType, position, direction, size, relaxTime, collData):
        if debug_state.IS_DEBUGGING:
            g_debugStateCollector.collectStateBeforeGunMarkersUpdate()

        if markerType == _MARKER_TYPE.CLIENT:
            self.__clientState = (
             position, direction, collData)
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__clientController.update(markerType, position, direction, size, relaxTime, collData)
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

                self.__serverController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.CLIENT_DISPERSION.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__dispersionClientController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.SERVER_DISPERSION.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__dispersionServerController.update(markerType, position, direction, size, relaxTime, collData)
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

                    self.__latencyClientController.setServerDispersionAngle(self.__serverDispersionAngle)
                    self.__latencyClientController.update(markerType, position, direction, serverSize, relaxTime, collData)
                else:
                    self.__latencyClientController.setServerDispersionAngle(None)
                    self.__latencyClientController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.SERVER_SIMPLE.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__simpleServerController.update(markerType, position, direction, size, relaxTime, collData)
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
