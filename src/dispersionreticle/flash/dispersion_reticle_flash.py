import BigWorld
import GUI
import SCALEFORM
import Math
import logging

import Event
from AvatarInputHandler import cameras
from gui import DEPTH_OF_GunMarker
from gui.Scaleform.daapi.view.external_components import ExternalFlashComponent, ExternalFlashSettings
from gui.Scaleform.flash_wrapper import InputKeyMode
from gui.Scaleform.framework.entities.BaseDAAPIModule import BaseDAAPIModule

from dispersionreticle.settings.config import g_config
from dispersionreticle.settings.config_param import g_configParams

logger = logging.getLogger(__name__)


class DispersionReticleFlashMeta(BaseDAAPIModule):

    def as_createMarker(self, gunMarkerType, markerName, isServerReticle):
        if self._isDAAPIInited():
            self.flashObject.as_createMarker(gunMarkerType, markerName, isServerReticle)

    def as_updateReticle(self, gunMarkerType, reticleSize):
        if self._isDAAPIInited():
            self.flashObject.as_updateReticle(gunMarkerType, reticleSize)

    def as_destroyMarker(self, markerName):
        if self._isDAAPIInited():
            self.flashObject.as_destroyMarker(markerName)

    def as_setMarkerDataProviderPresence(self, markerName, visible):
        if self._isDAAPIInited():
            self.flashObject.as_setMarkerDataProviderPresence(markerName, visible)

    def as_onConfigReload(self, serializedConfig):
        if self._isDAAPIInited():
            self.flashObject.as_onConfigReload(serializedConfig)


class DispersionReticleFlash(ExternalFlashComponent, DispersionReticleFlashMeta):

    __eventManager = Event.EventManager()

    onReticleUpdate = Event.Event(__eventManager)

    onMarkerCreate = Event.Event(__eventManager)
    onMarkerDestroy = Event.Event(__eventManager)
    onMarkerDataProviderAttach = Event.Event(__eventManager)
    onMarkerDataProviderDetach = Event.Event(__eventManager)

    def __init__(self):
        super(DispersionReticleFlash, self).__init__(
            ExternalFlashSettings("DispersionReticleFlash",
                                  "DispersionReticleFlash.swf",
                                  "root", None)
        )

        self.createExternalComponent()
        self._configureApp()

        self._markerDataProviders = {}

        self.onReticleUpdate += self.__onReticleUpdate

        self.onMarkerCreate += self.__onMarkerCreate
        self.onMarkerDestroy += self.__onMarkerDestroy

        self.onMarkerDataProviderAttach += self.__onMarkerDataProviderAttach
        self.onMarkerDataProviderDetach += self.__onMarkerDataProviderDetach

        g_config.onConfigReload += self.__onConfigReload

        self.__onConfigReload()

    def close(self):
        self.onReticleUpdate -= self.__onReticleUpdate

        self.onMarkerCreate -= self.__onMarkerCreate
        self.onMarkerDestroy -= self.__onMarkerDestroy

        self.onMarkerDataProviderAttach -= self.__onMarkerDataProviderAttach
        self.onMarkerDataProviderDetach -= self.__onMarkerDataProviderDetach

        g_config.onConfigReload -= self.__onConfigReload

        super(DispersionReticleFlash, self).close()

    def _configureApp(self):
        # this is needed, otherwise everything will be white
        self.movie.backgroundAlpha = 0.0

        # scales the app to match 1:1 pixels of app to screen
        self.movie.scaleMode = SCALEFORM.eMovieScaleMode.NO_SCALE

        # this does something
        # I guess it makes app not capture any user inputs
        self.component.wg_inputKeyMode = InputKeyMode.NO_HANDLE

        # depth sorting, required to be placed properly between other apps
        self.component.position.z = DEPTH_OF_GunMarker + 0.02

        # this is *probably* to ignore any focus on our app
        self.component.focus = False
        self.component.moveFocus = False

        # those below just don't work
        # I've lost way too much time to attempt to do so
        #
        # it is properly positioned by DispersionReticleFlash in AS3 as a workaround
        #
        # self.component.horizontalPositionMode = GUI.Simple.ePositionMode.CLIP
        # self.component.verticalPositionMode = GUI.Simple.ePositionMode.CLIP
        # self.component.horizontalAnchor = GUI.Simple.eHAnchor.LEFT
        # self.component.verticalAnchor = GUI.Simple.eVAnchor.TOP
        #
        # self.component.widthMode = GUI.Simple.eSizeMode.CLIP
        # self.component.heightMode = GUI.Simple.eSizeMode.CLIP
        #
        # self.component.position[0] = -1
        # self.component.position[1] = 1
        #
        # self.component.size = (1, 1)

    def __onReticleUpdate(self, reticle, reticleSize):
        self.as_updateReticle(reticle.gunMarkerType, reticleSize)

    def __onMarkerCreate(self, markerName, reticle):
        self.as_createMarker(reticle.gunMarkerType, markerName, reticle.isServerReticle())

    def __onMarkerDestroy(self, markerName, reticle):
        self.as_destroyMarker(markerName)

    def __onMarkerDataProviderAttach(self, markerName, dataProvider):
        self._markerDataProviders[markerName] = dataProvider

        self.as_setMarkerDataProviderPresence(markerName, True)

    def __onMarkerDataProviderDetach(self, markerName):
        self.as_setMarkerDataProviderPresence(markerName, False)

        if markerName in self._markerDataProviders:
            del self._markerDataProviders[markerName]

    def __onConfigReload(self):
        serializedConfig = {
            "simple-server-reticle": self.__serializeSimpleServerReticleSection()
        }

        self.as_onConfigReload(serializedConfig)

    def __serializeSimpleServerReticleSection(self):
        return {
            "color": self.__serializeColorTuple(g_configParams.simpleServerReticleColor()),
            "shape": g_configParams.simpleServerReticleShape(),
            "draw-center-dot": g_configParams.simpleServerReticleDrawCenterDot(),
            "draw-outline": g_configParams.simpleServerReticleDrawOutline(),
            "blend": g_configParams.simpleServerReticleBlend(),
            "alpha": g_configParams.simpleServerReticleAlpha()
        }

    @staticmethod
    def __serializeColorTuple(colorTuple):
        red, green, blue = colorTuple

        color = 0
        color |= red << 16
        color |= green << 8
        color |= blue

        return color

    # IMPORTANT
    # those methods are called by an swf app every frame in-between game logic
    # even on its pause in replays
    #
    # most notable afraid of py_getNormalizedMarkerPosition method being called just
    # because it accesses data providers
    #
    # I generally didn't see in WG code any special synchronization in such cases, so I assume
    # that game engine and AVM handle it for us to some extend
    # or maybe those calls are not fully parallel?

    def py_warn(self, message):
        logger.warn("[DispersionReticleFlash] %s", message)

    def py_getScreenResolution(self):
        screenResolution = GUI.screenResolution()
        return [screenResolution[0], screenResolution[1]]

    def py_getNormalizedMarkerPosition(self, markerName):
        # this method should be called by an swf app only, if there is created marker
        # in its display list and has marker data provider presence
        #
        # by this we assume, that its data provider MUST be present prior to it being called
        dataProvider = self._markerDataProviders[markerName]

        # projected point has scaled x and y between -1 and 1
        # where x starts from left -1 to right 1
        # and y starts from bottom -1 to top 1
        #
        # for AS3, we will need them scaled between 0 and 1 and have inverted y
        # because (0, 0) point in Flash starts from top left
        #
        # here we will only normalize it between 0 and 1 and invert y
        # and swf app will use it properly according to full screen
        partialPosition3d = Math.Matrix(dataProvider.positionMatrixProvider).translation

        projectedPartialPosition2d = cameras.projectPoint(partialPosition3d)

        normalizedPartialPositionX = 0.5 + 0.5 * projectedPartialPosition2d.x
        normalizedPartialPositionY = 0.5 - 0.5 * projectedPartialPosition2d.y

        isPointOnScreen = isPointOnScreenInFrontOfCamera(partialPosition3d)

        return [normalizedPartialPositionX, normalizedPartialPositionY, isPointOnScreen]


###########################################################
# A copied versions of functions to calculate if 3d position
# is on the screen.
#
# Because of "posInClip.w != 0" expression, function could return True
# for position behind camera, but in a clip of projection, in result,
# markers would be displayed both in front of a tank and behind it.
#
# Changing expression to "posInClip.w > 0" restricts it only to camera front.
# I just changed it like so and it works like a charm, lmao
###########################################################

# cameras
def isPointOnScreenInFrontOfCamera(point):
    if point.lengthSquared == 0.0:
        return False
    posInClip = Math.Vector4(point.x, point.y, point.z, 1)
    posInClip = getViewProjectionMatrix().applyV4Point(posInClip)
    if posInClip.w > 0 and -1 <= posInClip.x / posInClip.w <= 1 and -1 <= posInClip.y / posInClip.w <= 1:
        return True
    return False


def getViewProjectionMatrix():
    result = Math.Matrix(BigWorld.camera().matrix)
    result.postMultiply(getProjectionMatrix())
    return result


def getProjectionMatrix():
    proj = BigWorld.projection()
    aspect = getScreenAspectRatio()
    result = Math.Matrix()
    result.perspectiveProjection(proj.fov, aspect, proj.nearPlane, proj.farPlane)
    return result


def getScreenAspectRatio():
    return BigWorld.getAspectRatio()
