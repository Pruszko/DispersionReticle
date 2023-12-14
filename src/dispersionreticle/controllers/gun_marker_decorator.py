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
                 focusedClientController, focusedServerController,
                 hybridClientController, hybridExtendedClientController,
                 focusedExtendedClientController, focusedExtendedServerController,
                 serverExtendedServerController):
        super(DispersionGunMarkersDecorator, self).__init__()
        self.__clientController = clientController
        self.__serverController = serverController
        self.__dualAccController = dualAccController
        self.__focusedClientController = focusedClientController
        self.__focusedServerController = focusedServerController

        self.__hybridClientController = hybridClientController
        self.__hybridExtendedClientController = hybridExtendedClientController

        self.__focusedExtendedClientController = focusedExtendedClientController
        self.__focusedExtendedServerController = focusedExtendedServerController

        self.__serverExtendedServerController = serverExtendedServerController

        self._allAdditionalControllers = [
            focusedClientController, focusedServerController,
            hybridClientController, hybridExtendedClientController,
            focusedExtendedClientController, focusedExtendedServerController,
            serverExtendedServerController
        ]

        self._allControllers = [clientController, serverController, dualAccController] + self._allAdditionalControllers

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

        for controller in self._allAdditionalControllers:
            controller.enable()

            if controller._reticle.isServerReticle():
                controller.setPosition(self.__serverState[0])
            else:
                controller.setPosition(self.__clientState[0])

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

                for controller in self._allAdditionalControllers:
                    if not controller._reticle.isServerReticle():
                        continue

                    controller.setPosition(self.__clientController.getPosition())
                    controller.setSize(self.__clientController.getSize())
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
        elif markerType == ReticleRegistry.FOCUSED_CLIENT.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__focusedClientController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.FOCUSED_SERVER.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__focusedServerController.update(markerType, position, direction, size, relaxTime, collData)
        # those 2x elif has to be done outside controllers because we have to collect server reticle size
        # also, we will have delayed access to server size, so we need to wait
        # until GunMarkerComponent will provide server data
        elif markerType == ReticleRegistry.HYBRID_CLIENT.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.updateHybridReticle(self.__hybridClientController,
                                         collData, direction, markerType, position, relaxTime, size)
        elif markerType == ReticleRegistry.HYBRID_EXTENDED_CLIENT.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.updateHybridReticle(self.__hybridExtendedClientController,
                                         collData, direction, markerType, position, relaxTime, size)
        elif markerType == ReticleRegistry.FOCUSED_EXTENDED_CLIENT.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED:
                self.__focusedExtendedClientController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.FOCUSED_EXTENDED_SERVER.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__focusedExtendedServerController.update(markerType, position, direction, size, relaxTime, collData)
        elif markerType == ReticleRegistry.SERVER_EXTENDED_SERVER.gunMarkerType:
            if self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__serverExtendedServerController.update(markerType, position, direction, size, relaxTime, collData)
        else:
            gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def updateHybridReticle(self, controller, collData, direction, markerType, position, relaxTime, size):
        # first calls won't have ready server data yet
        # just display client size whenever it is not known
        if self.__serverSizeDispersion is not None and self.__serverDispersionAngle is not None:
            # scale server size dispersion by distance for hybrid reticle
            distance = getDistanceFromSniperViewport(position)
            serverSize = tuple(i * distance for i in self.__serverSizeDispersion)

            controller.setServerDispersionAngle(self.__serverDispersionAngle)
            controller.update(markerType, position, direction, serverSize, relaxTime, collData)
        else:
            controller.setServerDispersionAngle(None)
            controller.update(markerType, position, direction, size, relaxTime, collData)

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
