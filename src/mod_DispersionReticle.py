import BigWorld, Math
import AvatarInputHandler
from aih_constants import GUN_MARKER_TYPE
from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler import aih_global_binding
from AvatarInputHandler import _GUN_MARKER_TYPE
from AvatarInputHandler.aih_global_binding import BINDING_ID, _DEFAULT_VALUES, _Observable
from AvatarInputHandler.gun_marker_ctrl import IGunMarkerController
from AvatarInputHandler.gun_marker_ctrl import _DefaultGunMarkerController, _SPGGunMarkerController
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory, _makeWorldMatrix, _calcScale
from AvatarInputHandler.gun_marker_ctrl import _BINDING_ID, _MARKER_TYPE, _MARKER_FLAG
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _GunMarkersFactory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _ControlMarkersFactory,\
    _OptionalMarkersFactory, _EquipmentMarkersFactory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _GUN_MARKER_LINKAGES
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS
from gui.battle_control.controllers.crosshair_proxy import GunMarkersSetInfo
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy
from gui.battle_control.controllers.crosshair_proxy import _GUN_MARKERS_SET_IDS


# A switch to compile two versions of this mod.
# One is normal, the second is with both client and server reticle.
# Because there are no very much changes between
# them, they're merged into one file.
MOD_VERSION_DISP = 0
MOD_VERSION_DISP_CLIENT_SERVER = 1
MOD_VERSION_CLIENT_SERVER = 2

MOD_VERSION_CURRENT = MOD_VERSION_CLIENT_SERVER


def is_version_disp():
    return MOD_VERSION_CURRENT == MOD_VERSION_DISP or MOD_VERSION_CURRENT == MOD_VERSION_DISP_CLIENT_SERVER


def is_version_server():
    return MOD_VERSION_CURRENT == MOD_VERSION_CLIENT_SERVER or MOD_VERSION_CURRENT == MOD_VERSION_DISP_CLIENT_SERVER


# Utility decorator to override function in certain class/module
def overrideIn(cls):
    def _overrideMethod(func):
        old = getattr(cls, func.__name__)

        def wrapper(*args, **kwargs):
            return func(old, *args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        return wrapper
    return _overrideMethod


# Utility decorator to add new function in certain class/module
def addMethodTo(cls):
    def _overrideMethod(func):
        setattr(cls, func.__name__, func)
        return func
    return _overrideMethod


# Helper fields for new gun marker types
FOCUS_MARKER_TYPE_OFFSET = 2
GUN_MARKER_TYPE_CLIENT_FOCUS = GUN_MARKER_TYPE.CLIENT + FOCUS_MARKER_TYPE_OFFSET
GUN_MARKER_TYPE_SERVER_FOCUS = GUN_MARKER_TYPE.SERVER + FOCUS_MARKER_TYPE_OFFSET


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
# - Every control mode related to gun markers (there are 7 of them) has their own gun marker decorator.
###########################################################

@overrideIn(AvatarInputHandler.AvatarInputHandler)
def updateGunMarker(func, self, pos, direction, size, relaxTime, collData):
    self._AvatarInputHandler__curCtrl.updateGunMarker(_GUN_MARKER_TYPE.CLIENT,
                                                      pos, direction, size, relaxTime, collData)
    self._AvatarInputHandler__curCtrl.updateGunMarker(GUN_MARKER_TYPE_CLIENT_FOCUS,
                                                      pos, direction, size, relaxTime, collData)


@overrideIn(AvatarInputHandler.AvatarInputHandler)
def updateGunMarker2(func, self, pos, direction, size, relaxTime, collData):
    self._AvatarInputHandler__curCtrl.updateGunMarker(_GUN_MARKER_TYPE.SERVER,
                                                      pos, direction, size, relaxTime, collData)
    self._AvatarInputHandler__curCtrl.updateGunMarker(GUN_MARKER_TYPE_SERVER_FOCUS,
                                                      pos, direction, size, relaxTime, collData)


###########################################################
# CrosshairDataProxy hooks
# Responsible for changing penetration indicator (that mark on the
# middle of the reticle) to proper color (red, orange, green) on new markerType.
#
# Without this override, client and server focus gun markers would
# always be red and since focus markers are displayed in front of vanilla reticles, color of
# vanilla reticle penetration indicator wouldn't be visible.
###########################################################

# crosshair_proxy
@overrideIn(CrosshairDataProxy)
def _CrosshairDataProxy__setGunMarkerState(func, self, markerType, value):
    position, direction, collision = value
    self.onGunMarkerStateChanged(markerType, position, direction, collision)
    self.onGunMarkerStateChanged(markerType + FOCUS_MARKER_TYPE_OFFSET, position, direction, collision)


###########################################################
# Adds linkage for new reticles so they'll use default reticle
# This is needed due to components having unique name restriction.
#
# Linkages to certain gun markers (to their properties like color)
# can be reused, so it is only needed to make new unique names
# for new marker types for certain aiming mode (arcade, sniper, SPG,
# arcade dual, sniper dual)
#
# Linkages are selected same like vanilla markers (arcade focus -> arcade linkage etc).
#
# Without adding unique names, factories in gm_factory.py would mess up
# in providing proper data provider for certain markerType.
#
# Also, GunMarkerComponents (gm_components.py) would raise exception due to
# components not having unique names (it would mess up some of its methods
# without this restrictions since components are stored in dictionary by name).
###########################################################

ARCADE_FOCUS_GUN_MARKER_NAME = 'arcadeFocusGunMarker'
SNIPER_FOCUS_GUN_MARKER_NAME = 'sniperFocusGunMarker'
DUAL_FOCUS_GUN_ARCADE_MARKER_NAME = 'arcadeDualFocusGunMarker'
DUAL_FOCUS_GUN_SNIPER_MARKER_NAME = 'sniperDualFocusGunMarker'
SPG_FOCUS_GUN_MARKER_NAME = 'spgFocusGunMarker'

# gm_factory
_GUN_MARKER_LINKAGES.update({
    ARCADE_FOCUS_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    SNIPER_FOCUS_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_LINKAGE,
    DUAL_FOCUS_GUN_ARCADE_MARKER_NAME: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
    DUAL_FOCUS_GUN_SNIPER_MARKER_NAME: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE,
    SPG_FOCUS_GUN_MARKER_NAME: _CONSTANTS.GUN_MARKER_SPG_LINKAGE
})


###########################################################
# Use new marker factory to create 2x Client marker or 2x Server marker
#
# In MOD_VERSION_CLIENT_SERVER it will create both of them
# if "Use server reticle" is enabled.
#
# Standard _ControlMarkersFactory (gm_factory) either instantiates or overrides
# crosshair flash component for each vehicle types (for ex. normal tanks needs
# only arcade and sniper reticle).
#
# So, for new gun markers, it is needed to instantiate crosshair flash component as well.
# Creation of markers internally uses linkages retrieved
# from _GUN_MARKER_LINKAGES (gm_factory) by marker name.
###########################################################


def selectProperType(markerType, currentType):
    if currentType != GUN_MARKER_TYPE.UNDEFINED:
        return markerType
    return GUN_MARKER_TYPE.UNDEFINED


def toFocusGunMarkerType(markerType):
    if markerType != GUN_MARKER_TYPE.UNDEFINED:
        return markerType + FOCUS_MARKER_TYPE_OFFSET
    return GUN_MARKER_TYPE.UNDEFINED


# gm_factory
class _NewControlMarkersFactory(_ControlMarkersFactory):

    def _createDefaultMarkers(self):
        markerType = self._getMarkerType()

        if is_version_server():
            clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
            clientFocusType = selectProperType(GUN_MARKER_TYPE_CLIENT_FOCUS, markerType)
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

            if is_version_disp():
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createArcadeMarker(clientFocusType, ARCADE_FOCUS_GUN_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.SNIPER_GUN_MARKER_NAME),
                    self._createSniperMarker(clientFocusType, SNIPER_FOCUS_GUN_MARKER_NAME))
            else:
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.SNIPER_GUN_MARKER_NAME))

            if markerType == GUN_MARKER_TYPE.SERVER:
                result += (
                    self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                    self._createSniperMarker(serverType, _CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME))

            return result

        focusMarkerType = toFocusGunMarkerType(markerType)
        return (
         self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
         self._createArcadeMarker(focusMarkerType, ARCADE_FOCUS_GUN_MARKER_NAME),
         self._createSniperMarker(markerType, _CONSTANTS.SNIPER_GUN_MARKER_NAME),
         self._createSniperMarker(focusMarkerType, SNIPER_FOCUS_GUN_MARKER_NAME))

    def _createSPGMarkers(self):
        markerType = self._getMarkerType()

        if is_version_server():
            clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
            clientFocusType = selectProperType(GUN_MARKER_TYPE_CLIENT_FOCUS, markerType)
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

            if is_version_disp():
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createArcadeMarker(clientFocusType, ARCADE_FOCUS_GUN_MARKER_NAME),
                    self._createSPGMarker(clientType, _CONSTANTS.SPG_GUN_MARKER_NAME),
                    self._createSPGMarker(clientFocusType, SPG_FOCUS_GUN_MARKER_NAME))
            else:
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
                    self._createSPGMarker(clientType, _CONSTANTS.SPG_GUN_MARKER_NAME))

            if markerType == GUN_MARKER_TYPE.SERVER:
                result += (
                    self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME),
                    self._createSPGMarker(serverType, _CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME))

            return result

        focusMarkerType = toFocusGunMarkerType(markerType)
        return (
         self._createArcadeMarker(markerType, _CONSTANTS.ARCADE_GUN_MARKER_NAME),
         self._createArcadeMarker(focusMarkerType, ARCADE_FOCUS_GUN_MARKER_NAME),
         self._createSPGMarker(markerType, _CONSTANTS.SPG_GUN_MARKER_NAME),
         self._createSPGMarker(focusMarkerType, SPG_FOCUS_GUN_MARKER_NAME))

    def _createDualGunMarkers(self):
        markerType = self._getMarkerType()

        if is_version_server():
            clientType = selectProperType(GUN_MARKER_TYPE.CLIENT, markerType)
            clientFocusType = selectProperType(GUN_MARKER_TYPE_CLIENT_FOCUS, markerType)
            serverType = selectProperType(GUN_MARKER_TYPE.SERVER, markerType)

            if is_version_disp():
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                    self._createArcadeMarker(clientFocusType, DUAL_FOCUS_GUN_ARCADE_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME),
                    self._createSniperMarker(clientFocusType, DUAL_FOCUS_GUN_SNIPER_MARKER_NAME))
            else:
                result = (
                    self._createArcadeMarker(clientType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
                    self._createSniperMarker(clientType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME))

            if markerType == GUN_MARKER_TYPE.SERVER:
                result += (
                    self._createArcadeMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME),
                    self._createSniperMarker(serverType, _CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME))

            return result

        focusMarkerType = toFocusGunMarkerType(markerType)
        return (
         self._createArcadeMarker(markerType, _CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME),
         self._createArcadeMarker(focusMarkerType, DUAL_FOCUS_GUN_ARCADE_MARKER_NAME),
         self._createSniperMarker(markerType, _CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME),
         self._createSniperMarker(focusMarkerType, DUAL_FOCUS_GUN_SNIPER_MARKER_NAME))


# It is needed to be overridden manually.
# Especially, first one in tuple is responsible for marker's instantiation.
gm_factory._FACTORIES_COLLECTION = (_NewControlMarkersFactory, _OptionalMarkersFactory, _EquipmentMarkersFactory)


###########################################################
# Adds data providers for each reticle type
#
# Each reticle MUST have their own data provider.
# Otherwise, GUI.WGCrosshairFlash will complain with failing
# to assign data provider by raising an exception.
#
# Basically, gun marker controllers and factories uses them.
#
# Controllers provides data (positionMatrix, startSize, maybe something more)
# and factories assigns providers of them to GUI.WGCrosshairFlash object
# that uses them to update it's position and size.
#
# Can't tell exactly why crosshair flash components can't share
# certain data provider (exception message isn't precise
# and code of GUI modules isn't accessible), however
# an easy workaround is just providing unique data provider
# for each reticle type and just mimic data of vanilla data providers
# to the new ones.
#
# To do this:
# - it is needed to register IDs of new data providers
#   in global AvatarInputHandler bindings and provide same default values
#   for them as vanilla data providers,
# - in _GunMarkersDPFactory (gun_marker_ctrl), add read-write access to
#   new providers that will be used to write data by controllers,
# - also, add singleton getters for each new data provider like for
#   vanilla ones,
# - in GunMarkersSetInfo (crosshair_proxy), add read-only access to
#   new providers that will be used by crosshair flash objects.
###########################################################

CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER = 13
CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER = 14
SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER = 15
SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER = 16

# aih_global_binding
BINDING_ID.RANGE += (
    CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER,
    CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER
)

# aih_global_binding
_DEFAULT_VALUES.update({
    CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None),
    CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None),
    SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None),
    SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER: lambda: _Observable(None)
})

# crosshair_proxy
_GUN_MARKERS_SET_IDS += (
    CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER,
    CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER,
    SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER
)

# gun_marker_ctrl
_GunMarkersDPFactory._clientFocusDataProvider = aih_global_binding.bindRW(CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER)
_GunMarkersDPFactory._serverFocusDataProvider = aih_global_binding.bindRW(SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER)
_GunMarkersDPFactory._clientSPGFocusDataProvider = aih_global_binding.bindRW(CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)
_GunMarkersDPFactory._serverSPGFocusDataProvider = aih_global_binding.bindRW(SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)

# crosshair_proxy
GunMarkersSetInfo.clientMarkerFocusDataProvider = aih_global_binding.bindRO(CLIENT_GUN_MARKER_FOCUS_DATA_PROVIDER)
GunMarkersSetInfo.clientSPGMarkerFocusDataProvider = aih_global_binding.bindRO(CLIENT_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)
GunMarkersSetInfo.serverMarkerFocusDataProvider = aih_global_binding.bindRO(SERVER_GUN_MARKER_FOCUS_DATA_PROVIDER)
GunMarkersSetInfo.serverSPGMarkerFocusDataProvider = aih_global_binding.bindRO(SERVER_SPG_GUN_MARKER_FOCUS_DATA_PROVIDER)


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getClientFocusProvider(self):
    if self._clientFocusDataProvider is None:
        self._clientFocusDataProvider = self._makeDefaultProvider()
    return self._clientFocusDataProvider


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getServerFocusProvider(self):
    if self._serverFocusDataProvider is None:
        self._serverFocusDataProvider = self._makeDefaultProvider()
    return self._serverFocusDataProvider


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getClientSPGFocusProvider(self):
    if self._clientSPGFocusDataProvider is None:
        self._clientSPGFocusDataProvider = self._makeSPGProvider()
    return self._clientSPGFocusDataProvider


# gun_marker_ctrl
@addMethodTo(_GunMarkersDPFactory)
def getServerSPGFocusProvider(self):
    if self._serverSPGFocusDataProvider is None:
        self._serverSPGFocusDataProvider = self._makeSPGProvider()
    return self._serverSPGFocusDataProvider


###########################################################
# Make getters of providers return proper data provider for new marker types
#
# It is needed, so an internal getter won't return None for new marker types.
# By this override, those methods can be reused without changing other methods
# that relies on it.
###########################################################

# gm_factory
@overrideIn(_GunMarkersFactory)
def _getMarkerDataProvider(func, self, markerType):
    if markerType is GUN_MARKER_TYPE.SERVER:
        return self._markersInfo.serverMarkerDataProvider
    if markerType is GUN_MARKER_TYPE_SERVER_FOCUS:
        return self._markersInfo.serverMarkerFocusDataProvider
    else:
        if markerType is GUN_MARKER_TYPE.CLIENT:
            return self._markersInfo.clientMarkerDataProvider
        if markerType is GUN_MARKER_TYPE_CLIENT_FOCUS:
            return self._markersInfo.clientMarkerFocusDataProvider
        return


# gm_factory
@overrideIn(_GunMarkersFactory)
def _getSPGDataProvider(func, self, markerType):
    if markerType is GUN_MARKER_TYPE.SERVER:
        return self._markersInfo.serverSPGMarkerDataProvider
    if markerType is GUN_MARKER_TYPE_SERVER_FOCUS:
        return self._markersInfo.serverSPGMarkerFocusDataProvider
    else:
        if markerType is GUN_MARKER_TYPE.CLIENT:
            return self._markersInfo.clientSPGMarkerDataProvider
        if markerType is GUN_MARKER_TYPE_CLIENT_FOCUS:
            return self._markersInfo.clientSPGMarkerFocusDataProvider
        return


###########################################################
# Return new decorator that includes new reticle controllers
#
# Basically, creates controllers of each markerType and provides them with proper
# data provider to communicate with crosshair flash component.
#
# Gun marker decorator manages all created controllers and forwards properly all methods
# related with them. Because decorator accepts only 2 controllers (vanilla client
# and server controllers), it is needed to provide custom decorator that handles
# new additional 2 controllers of dispersion reticles.
#
# In default controller (for normal tanks), it is needed to override
# size and idealSize in update method to represent focused dispersion of a gun.
#
# In SPG controller, it is only needed to provide focused dispersion angle
# in _updateDispersionData method.
###########################################################

# gun_marker_ctrl
@overrideIn(gun_marker_ctrl)
def createGunMarker(func, isStrategic):
    factory = _GunMarkersDPFactory()
    if isStrategic:
        clientMarker = _SPGGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientSPGProvider())
        serverMarker = _SPGGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerSPGProvider())
        clientMarkerFocus = _FocusSPGGunMarkerController(GUN_MARKER_TYPE_CLIENT_FOCUS, factory.getClientSPGFocusProvider())
        serverMarkerFocus = _FocusSPGGunMarkerController(GUN_MARKER_TYPE_SERVER_FOCUS, factory.getServerSPGFocusProvider())
    else:
        clientMarker = _DefaultGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientProvider())
        serverMarker = _DefaultGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerProvider())
        clientMarkerFocus = _FocusGunMarkerController(GUN_MARKER_TYPE_CLIENT_FOCUS, factory.getClientFocusProvider())
        serverMarkerFocus = _FocusGunMarkerController(GUN_MARKER_TYPE_SERVER_FOCUS, factory.getServerFocusProvider())
    return _NewGunMarkersDecorator(clientMarker, serverMarker, clientMarkerFocus, serverMarkerFocus)


@overrideIn(gun_marker_ctrl)
def useClientGunMarker(func):
    if is_version_server():
        return True
    return func()


@overrideIn(gun_marker_ctrl)
def useDefaultGunMarkers(func):
    if is_version_server():
        return False
    return func()


###########################################################
# Helper method to calculate diameter of fully aimed reticle
#
# Reads dispersion angle from vehicle descriptor and multiplies
# it with aim dispersion multiplier from PlayerAvatar (Avatar.py).
# Aim dispersion multiplier accounts things like crew, food, etc.
#
# Because reticle size is an 2D object on a 3D map, it needs
# to account a distance between a camera and reticle position.
# Otherwise, it would appear WAY smaller (or bigger in close distance) than it should be.
#
# Dispersion angle is an multiplier per 1m unit, so it is
# an easy multiplication with distance that is also in meters.
###########################################################
def getFocusedSize(positionMatrix):
    cameraPos = BigWorld.camera().position
    shotDir = positionMatrix.applyToOrigin() - cameraPos
    shotDist = shotDir.length

    playerAvatar = BigWorld.player()
    vehicleDesc = playerAvatar._PlayerAvatar__getDetailedVehicleDescriptor()

    shotDispersionAngle = vehicleDesc.gun.shotDispersionAngle
    shotDispMultiplierFactor = playerAvatar._PlayerAvatar__aimingInfo[2]
    dispersionAngle = shotDispersionAngle * shotDispMultiplierFactor
    return 2.0 * shotDist * dispersionAngle


# gun_marker_ctrl
class _FocusGunMarkerController(_DefaultGunMarkerController):

    def update(self, markerType, pos, direction, sizeVector, relaxTime, collData):
        super(_DefaultGunMarkerController, self).update(markerType, pos, direction, sizeVector, relaxTime, collData)
        positionMatrix = Math.Matrix()
        positionMatrix.setTranslate(pos)
        self._updateMatrixProvider(positionMatrix, relaxTime)

        # size = sizeVector[0]
        # idealSize = sizeVector[1]
        size = getFocusedSize(positionMatrix)
        idealSize = size

        # Those below lines of code have to be commented for dispersion gun markers.
        # Otherwise, this controller would:
        # - read current dispersion from replay controller, by this, it
        #   would override calculated focused dispersion in replays
        # - it would override gun dispersion of vanilla gun marker in
        #   replay file (undefined behavior, in replays it probably would
        #   display zero-size dispersion).
        #
        # replayCtrl = BattleReplay.g_replayCtrl
        # if replayCtrl.isPlaying and replayCtrl.isClientReady:
        #     s = replayCtrl.getArcadeGunMarkerSize()
        #     if s != -1.0:
        #         size = s
        # elif replayCtrl.isRecording:
        #     if replayCtrl.isServerAim and self._gunMarkerType == GUN_MARKER_TYPE_SERVER_FOCUS:
        #         replayCtrl.setArcadeGunMarkerSize(size)
        #     elif self._gunMarkerType == GUN_MARKER_TYPE_CLIENT_FOCUS:
        #         replayCtrl.setArcadeGunMarkerSize(size)

        positionMatrixForScale = self._DefaultGunMarkerController__checkAndRecalculateIfPositionInExtremeProjection(positionMatrix)
        worldMatrix = _makeWorldMatrix(positionMatrixForScale)
        currentSize = _calcScale(worldMatrix, size) * self._DefaultGunMarkerController__screenRatio
        idealSize = _calcScale(worldMatrix, idealSize) * self._DefaultGunMarkerController__screenRatio
        self._DefaultGunMarkerController__sizeFilter.update(currentSize, idealSize)
        self._DefaultGunMarkerController__curSize = self._DefaultGunMarkerController__sizeFilter.getSize()
        if self._DefaultGunMarkerController__replSwitchTime > 0.0:
            self._DefaultGunMarkerController__replSwitchTime -= relaxTime
            self._dataProvider.updateSize(self._DefaultGunMarkerController__curSize, 0.0)
        else:
            self._dataProvider.updateSize(self._DefaultGunMarkerController__curSize, relaxTime)


###########################################################
# Helper method to calculate dispersion angle of fully aimed SPG reticle
#
# Just reads dispersion angle from vehicle descriptor and multiplies
# it with dispersion multiplier from PlayerAvatar (Avatar.py).
###########################################################
def getFocusedDispersionAngle():
    playerAvatar = BigWorld.player()
    vehicleDesc = playerAvatar._PlayerAvatar__getDetailedVehicleDescriptor()

    shotDispersionAngle = vehicleDesc.gun.shotDispersionAngle
    shotDispMultiplierFactor = playerAvatar._PlayerAvatar__aimingInfo[2]
    return shotDispersionAngle * shotDispMultiplierFactor


# gun_marker_ctrl
class _FocusSPGGunMarkerController(_SPGGunMarkerController):
    def _updateDispersionData(self):
        # dispersionAngle = self._gunRotator.dispersionAngle
        dispersionAngle = getFocusedDispersionAngle()

        # Those below lines of code have to be commented for dispersion gun markers.
        # Otherwise, this controller would:
        # - read current dispersion from replay controller, by this, it
        #   would override calculated focused dispersion in replays
        # - it would override gun dispersion of vanilla gun marker in
        #   replay file (undefined behavior, in replays it probably would
        #   display zero-size dispersion).
        #
        # isServerAim = self._gunMarkerType == GUN_MARKER_TYPE_SERVER_FOCUS
        # replayCtrl = BattleReplay.g_replayCtrl
        # if replayCtrl.isPlaying and replayCtrl.isClientReady:
        #     d, s = replayCtrl.getSPGGunMarkerParams()
        #     if d != -1.0 and s != -1.0:
        #         dispersionAngle = d
        # elif replayCtrl.isRecording:
        #     if replayCtrl.isServerAim and isServerAim:
        #         replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)
        #     elif not isServerAim:
        #         replayCtrl.setSPGGunMarkerParams(dispersionAngle, 0.0)

        self._dataProvider.setupConicDispersion(dispersionAngle)


# gun_marker_ctrl
class _NewGunMarkersDecorator(IGunMarkerController):
    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)
    __clientState = aih_global_binding.bindRW(_BINDING_ID.CLIENT_GUN_MARKER_STATE)
    __serverState = aih_global_binding.bindRW(_BINDING_ID.SERVER_GUN_MARKER_STATE)

    def __init__(self, clientMarker, serverMarker, clientMarkerFocus, serverMarkerFocus):
        super(_NewGunMarkersDecorator, self).__init__()
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
