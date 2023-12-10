# gun_marker_ctrl
import BigWorld, Math
from AvatarInputHandler import gun_marker_ctrl, aih_global_binding, AimingSystems
from AvatarInputHandler.gun_marker_ctrl import IGunMarkerController, _BINDING_ID, _MARKER_TYPE, _MARKER_FLAG

from dispersionreticle.utils import debug_state
from dispersionreticle.utils.debug_state import g_debugStateCollector
from dispersionreticle.utils.reticle_registry import ReticleRegistry


# gun_marker_ctrl
class DispersionGunMarkersDecorator(IGunMarkerController):
    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)
    __clientState = aih_global_binding.bindRW(_BINDING_ID.CLIENT_GUN_MARKER_STATE)
    __serverState = aih_global_binding.bindRW(_BINDING_ID.SERVER_GUN_MARKER_STATE)
    __dualAccState = aih_global_binding.bindRW(_BINDING_ID.DUAL_ACC_GUN_MARKER_STATE)

    def __init__(self,
                 clientController, serverController, dualAccController,
                 standardFocusedClientController, standardFocusedServerController,
                 standardHybridClientController,
                 customServerServerController):
        super(DispersionGunMarkersDecorator, self).__init__()
        self.__clientController = clientController
        self.__serverController = serverController
        self.__dualAccController = dualAccController
        self.__standardFocusedClientController = standardFocusedClientController
        self.__standardFocusedServerController = standardFocusedServerController

        self.__standardHybridClientController = standardHybridClientController

        self.__customServerServerController = customServerServerController

        self._allControllers = [
            clientController, serverController, dualAccController,
            standardFocusedClientController, standardFocusedServerController,
            standardHybridClientController,
            customServerServerController
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
        self.__dualAccController.enable()
        self.__dualAccController.setPosition(self.__dualAccState[0])

        self.__standardFocusedClientController.enable()
        self.__standardFocusedClientController.setPosition(self.__clientState[0])
        self.__standardFocusedServerController.enable()
        self.__standardFocusedServerController.setPosition(self.__serverState[0])

        self.__standardHybridClientController.enable()
        self.__standardHybridClientController.setPosition(self.__clientState[0])

        self.__customServerServerController.enable()
        self.__customServerServerController.setPosition(self.__serverState[0])

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
                self.__standardFocusedServerController.setPosition(self.__standardFocusedClientController.getPosition())
                self.__standardFocusedServerController.setSize(self.__standardFocusedClientController.getSize())
                self.__standardHybridClientController.setPosition(self.__clientController.getPosition())
                self.__standardHybridClientController.setSize(self.__clientController.getSize())
                self.__customServerServerController.setPosition(self.__clientController.getPosition())
                self.__customServerServerController.setSize(self.__clientController.getSize())
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
                # collect server size dispersion for hybrid reticle
                self.__serverSizeDispersion = size
                if BigWorld.player() and BigWorld.player().gunRotator:
                    self.__serverDispersionAngle = BigWorld.player().gunRotator.dispersionAngle

                # scale it down to dispersion per 1m unit
                distance = getDistanceFromSniperViewport(position)
                if distance > 0.0:
                    self.__serverSizeDispersion = tuple(i / distance for i in size)

                self.__serverController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == _MARKER_TYPE.DUAL_ACC:
            self.__dualAccState = (
                position, direction, collData)
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__dualAccController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.STANDARD_FOCUSED_CLIENT.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__standardFocusedClientController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.STANDARD_FOCUSED_SERVER.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__standardFocusedServerController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.STANDARD_HYBRID_CLIENT.gunMarkerType:
            # this has to be done outside controllers because we have to collect server reticle size
            # also, we will have delayed access to server size, so we need to wait
            # until GunMarkerComponent will provide server data
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                # first calls won't have ready server data yet
                # just display client size whenever it is not known
                if self.__serverSizeDispersion is not None and self.__serverDispersionAngle is not None:
                    # scale server size dispersion by distance for hybrid reticle
                    distance = getDistanceFromSniperViewport(position)
                    serverSize = tuple(i * distance for i in self.__serverSizeDispersion)

                    self.__standardHybridClientController.setServerDispersionAngle(self.__serverDispersionAngle)
                    self.__standardHybridClientController.update(markerType, position, direction, serverSize, relaxTime, collData)
                else:
                    self.__standardHybridClientController.setServerDispersionAngle(None)
                    self.__standardHybridClientController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.CUSTOM_SERVER_SERVER.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__customServerServerController.update(markerType, position, direction, size, relaxTime, collData)
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
