import logging

import BigWorld, Math
from VehicleGunRotator import GunMarkerInfo
from aih_constants import GunMarkerState
from AvatarInputHandler import gun_marker_ctrl, aih_global_binding, AimingSystems
from AvatarInputHandler.gun_marker_ctrl import IGunMarkerController, _BINDING_ID, _MARKER_TYPE, _MARKER_FLAG

from dispersionreticle.controllers import AihUpdateType
from dispersionreticle.utils import debug_state
from dispersionreticle.utils.debug_state import g_debugStateCollector
from dispersionreticle.utils.reticle_registry import ReticleRegistry


logger = logging.getLogger(__name__)


# gun_marker_ctrl
class WgDispersionGunMarkersDecorator(IGunMarkerController):
    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)
    __clientState = aih_global_binding.bindRW(_BINDING_ID.CLIENT_GUN_MARKER_STATE)
    __serverState = aih_global_binding.bindRW(_BINDING_ID.SERVER_GUN_MARKER_STATE)
    __dualAccState = aih_global_binding.bindRW(_BINDING_ID.DUAL_ACC_GUN_MARKER_STATE)

    # very dirty hack
    #
    # when update method is being invoked by our aih_hooks, we are not guaranteed that control mode = update type
    # this is due to both aih_hooks.updateClientGunMarker and aih_hooks.updateServerGunMarker being invoked
    # when ONLY server mode is enabled, which in result will call ALL reticles TWICE with DIFFERENT source data
    # resulting in jagged reticle movement
    #
    # we MUST somehow pass this information from aih_hooks to update method to properly delegate update calls
    # ... and this dirty hack is the easiest way, because game logic is single threaded
    currentUpdateType = AihUpdateType.CLIENT

    def __init__(self,
                 clientController, serverController, dualAccController,
                 debugClientController, debugServerController,
                 focusedClientController, focusedServerController,
                 hybridClientController, hybridExtendedClientController,
                 focusedExtendedClientController, focusedExtendedServerController,
                 serverExtendedClientController, serverExtendedServerController):
        super(WgDispersionGunMarkersDecorator, self).__init__()
        self.__clientController = clientController
        self.__serverController = serverController
        self.__dualAccController = dualAccController

        self.__debugClientController = debugClientController
        self.__debugServerController = debugServerController

        self.__focusedClientController = focusedClientController
        self.__focusedServerController = focusedServerController

        self.__hybridClientController = hybridClientController
        self.__hybridExtendedClientController = hybridExtendedClientController

        self.__focusedExtendedClientController = focusedExtendedClientController
        self.__focusedExtendedServerController = focusedExtendedServerController

        self.__serverExtendedClientController = serverExtendedClientController
        self.__serverExtendedServerController = serverExtendedServerController

        self._allAdditionalControllers = [
            debugClientController, debugServerController,
            focusedClientController, focusedServerController,
            hybridClientController, hybridExtendedClientController,
            focusedExtendedClientController, focusedExtendedServerController,
            serverExtendedClientController, serverExtendedServerController
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
        self.__clientController.setPosition(self.__clientState[0].position)
        self.__serverController.enable()
        self.__serverController.setPosition(self.__serverState[0].position)
        self.__dualAccController.enable()
        self.__dualAccController.setPosition(self.__dualAccState[0].position)

        for controller in self._allAdditionalControllers:
            controller.enable()

            if controller.isServerController():
                controller.setPosition(self.__serverState[0].position)
            else:
                controller.setPosition(self.__clientState[0].position)

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
                self.__serverController.setSizes(self.__clientController.getSizes())

                for controller in self._allAdditionalControllers:
                    if not controller.isServerController():
                        continue

                    controller.setPosition(self.__clientController.getPosition())
                    controller.setSizes(self.__clientController.getSizes())
        else:
            self.__gunMarkersFlags &= ~bit

    def update(self, markerType, gunMarkerInfo, supportMarkersInfo, relaxTime):
        if debug_state.IS_DEBUGGING:
            g_debugStateCollector.collectStateBeforeGunMarkersUpdate()

        # normally, I would replicate here the exact vanilla WoT client gun marker logic,
        # but then, it would have annoying bug that exist *even in non-modded WoT client*:
        # - when "Use server aim" is checked in game settings and user starts auto-aiming,
        #     then server reticle temporarily becomes client reticle
        #     but this would cause data provider switching from server one to client one
        #     while still using same gun marker
        #     and because client data provider was not getting updates, reticle
        #     would "flick" into any previous position stored in client data provider before auto-aiming
        #     then in next update tick it would "flick" back into correct position
        #
        # to fix it ourselves, we have to update "this" reticle data provider with data
        # from "another" reticle, if "this" reticle was not getting updates from its expected source
        #
        # for example, when only serverMode is enabled and we are updating server-side Focused Reticle
        # then we also update client-side Focused Reticle to update its data provider
        # so when auto-aiming occurs and data provider is switched to client-side one, no "flick" would happen
        # because data stored in it would be fresh
        #
        # extended reticles must be aware of this trick in _interceptPostUpdate method
        # not to update gun markers twice as much
        #
        # this vanilla WoT client bug is especially visible on server reticles in this mod
        # when both client and server reticles are enabled
        # so here I fixed this for myself, because it was annoying for me
        # lmao
        if not self._areBothModesEnabled():
            self.__serverSizeDispersion = None
            self.__serverDispersionAngle = None

        if markerType == _MARKER_TYPE.CLIENT:
            size = gunMarkerInfo.size
            if self._shouldUpdateController():
                self.__clientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
                size = self.__clientController.getSizes()[0]
            if self.currentUpdateType == AihUpdateType.CLIENT:
                self.__clientState = (GunMarkerState.fromGunMarkerInfo(gunMarkerInfo, size), supportMarkersInfo)
        elif markerType == _MARKER_TYPE.SERVER:
            size = gunMarkerInfo.size
            if self._shouldUpdateController():
                self.__serverController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
                size = self.__serverController.getSizes()[0]
            if self.currentUpdateType == AihUpdateType.SERVER:
                self.__serverState = (GunMarkerState.fromGunMarkerInfo(gunMarkerInfo, size), supportMarkersInfo)
        elif markerType == _MARKER_TYPE.DUAL_ACC:
            self.__dualAccState = (GunMarkerState.fromGunMarkerInfo(gunMarkerInfo), supportMarkersInfo)
            # don't touch mode here - vanilla code handles it normally
            if self._isClientModeEnabled():
                self.__dualAccController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.DEBUG_CLIENT.gunMarkerType:
            if self._shouldUpdateController():
                self.__debugClientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.DEBUG_SERVER.gunMarkerType:
            if self._shouldUpdateController():
                self.__debugServerController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)

            # collect server size dispersion for hybrid reticle
            # this will be called even, if server reticle is not instantiated
            self.__serverSizeDispersion = gunMarkerInfo.size
            if BigWorld.player() and BigWorld.player().gunRotator:
                self.__serverDispersionAngle = BigWorld.player().gunRotator.dispersionAngle

            # scale it down to dispersion per 1m unit
            distance = getDistanceFromSniperViewport(gunMarkerInfo.position)
            if distance > 0.0:
                self.__serverSizeDispersion = gunMarkerInfo.size / distance
        elif markerType == ReticleRegistry.FOCUSED_CLIENT.gunMarkerType:
            if self._shouldUpdateController():
                self.__focusedClientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.FOCUSED_SERVER.gunMarkerType:
            if self._shouldUpdateController():
                self.__focusedServerController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        # those 2x elif has to be done outside controllers because we have to collect server reticle size
        # also, we will have delayed access to server size, so we need to wait
        # until GunMarkerComponent will provide server data
        elif markerType == ReticleRegistry.HYBRID_CLIENT.gunMarkerType:
            if self._shouldUpdateController():
                self._updateHybridReticle(self.__hybridClientController,
                                          markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.HYBRID_EXTENDED_CLIENT.gunMarkerType:
            if self._shouldUpdateController():
                self._updateHybridReticle(self.__hybridExtendedClientController,
                                          markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.FOCUSED_EXTENDED_CLIENT.gunMarkerType:
            if self._shouldUpdateController():
                self.__focusedExtendedClientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.FOCUSED_EXTENDED_SERVER.gunMarkerType:
            if self._shouldUpdateController():
                self.__focusedExtendedServerController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.SERVER_EXTENDED_CLIENT.gunMarkerType:
            if self._shouldUpdateController():
                self.__serverExtendedClientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.SERVER_EXTENDED_SERVER.gunMarkerType:
            if self._shouldUpdateController():
                self.__serverExtendedServerController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        else:
            gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def _updateHybridReticle(self, controller, markerType, gunMarkerInfo, supportMarkersInfo, relaxTime):
        gunMarkerInfo = gunMarkerInfo  # type: GunMarkerInfo

        # when auto-aiming, use client-side data
        #
        # also, first calls won't have ready server data yet
        # just display client size whenever it is not known
        if self._areBothModesEnabled() \
                and self.__serverSizeDispersion is not None \
                and self.__serverDispersionAngle is not None:
            # scale server size dispersion by distance for hybrid reticle
            distance = getDistanceFromSniperViewport(gunMarkerInfo.position)
            serverSize = self.__serverSizeDispersion * distance

            controller.setServerDispersionAngle(self.__serverDispersionAngle)
            gunMarkerInfo = gunMarkerInfo._replace(size=serverSize)

            controller.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        else:
            controller.setServerDispersionAngle(None)
            controller.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)

    def _shouldUpdateController(self):
        return self._areBothModesEnabled() \
            or (self._isClientModeEnabled() and self.currentUpdateType == AihUpdateType.CLIENT) \
            or (self._isServerModeEnabled() and self.currentUpdateType == AihUpdateType.SERVER)

    def _areBothModesEnabled(self):
        return self._isClientModeEnabled() and self._isServerModeEnabled()

    def _isAnyModeEnabled(self):
        return self._isClientModeEnabled() or self._isServerModeEnabled()

    def _isClientModeEnabled(self):
        return self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED

    def _isServerModeEnabled(self):
        return self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED

    def setVisible(self, flag):
        pass

    def getSizes(self):
        return (0.0, 0.0)

    def setSizes(self, newSizes):
        pass


def getDistanceFromSniperViewport(position):
    sniperViewportPos = getSniperViewportPosition()
    shotDir = position - sniperViewportPos
    return shotDir.length


def getSniperViewportPosition():
    gunRotator = BigWorld.player().gunRotator
    gunMatrix = AimingSystems.getPlayerGunMat(gunRotator.turretYaw, gunRotator.gunPitch)
    return gunMatrix.translation
