import BigWorld
import GUI
import SCALEFORM
import Math
import logging

import Event
from AvatarInputHandler import cameras
from gui import DEPTH_OF_Aim
from gui.Scaleform.daapi.view.external_components import ExternalFlashComponent, ExternalFlashSettings
from gui.Scaleform.flash_wrapper import InputKeyMode
from gui.Scaleform.framework.entities.BaseDAAPIModule import BaseDAAPIModule

from dispersionreticle.flash import Layer
from dispersionreticle.settings import clamp
from dispersionreticle.settings.config import g_config
from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.utils import isClientWG, isClientLesta

logger = logging.getLogger(__name__)


class DispersionReticleFlashMeta(BaseDAAPIModule):

    def as_createMarker(self, reticleId, markerName):
        if self._isDAAPIInited():
            self.flashObject.as_createMarker(reticleId, markerName)

    def as_updateReticle(self, reticleId, reticleSize):
        if self._isDAAPIInited():
            self.flashObject.as_updateReticle(reticleId, reticleSize)

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

    def __init__(self, layer):
        super(DispersionReticleFlash, self).__init__(
            ExternalFlashSettings("DispersionReticleFlash",
                                  "DispersionReticleFlash.swf",
                                  "root", None)
        )
        self._layer = layer

        self.createExternalComponent()
        self._configureApp()

        self._markerPresence = []
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
        if isClientWG():
            self.component.wg_inputKeyMode = InputKeyMode.NO_HANDLE
        else:
            # Lesta started to rename stuff with wg_ prefix
            # I'm not sure if it is needed here, but let it be
            self.component.inputKeyMode = InputKeyMode.NO_HANDLE

        # depth sorting, required to be placed properly between other apps
        layerOffset = -0.02 if self._layer == Layer.TOP else 0.02
        self.component.position.z = DEPTH_OF_Aim + layerOffset

        # this also does something
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
        flashMarkerNames = reticle.reticleType.flashMarkerNames
        if not any(flashMarkerName in self._markerPresence for flashMarkerName in flashMarkerNames):
            return

        sizeConstraint = reticle.getStandardDataProvider().sizeConstraint
        minReticleSize = sizeConstraint[0]
        maxReticleSize = sizeConstraint[1]

        # fun note
        #
        # reticleSize is fully correctly calculated by controllers and my SWF app displays it perfectly
        # confirmed it by:
        # - debugging gun dispersion and reticleSize to logs
        # - displaying it in my SWF app (which have disabled scalling, so it matches screen pixels 1:1)
        # - comparing logged reticleSize with screenshots of reticle diameter displayed in-game
        #
        # however, for some reason, my reticle is visually way smaller than vanilla reticle
        # despite having exact same size (for example: fully focused vanilla reticle vs my extended focused reticle)
        #
        # and GUI.WGGunMarkerDataProvider is THE ONLY bridge in code
        # connecting controllers and GUI.WGCrosshairFlash wrapping reticle in CrosshairPanelContainer
        #
        # something in WG's GUI classes mess up it's size
        # so it's probably broken by hidden WG code either in GUI.WGCrosshairFlash or GUI.WGGunMarkerDataProvider
        #
        # sizeConstraints (min size and max size in pixels) are not affected by this bug
        # so reticle size alone is directly broken somewhere in hidden classes
        #
        # this means that
        # in order to properly match extended reticles to vanilla reticles
        # we have to deliberately mess up reticle size by the same factor that WG hidden classes do
        #
        # multiplier x1.72 matches it pixel-perfect
        #
        # I have no clue how that multiplier originated
        # it's not even close to some values like screen proportions, SWF app scale, interface scale,
        # square root of 3 (???) which is a little too big
        # or anything other
        #
        # lmao
        deliberatelyMessedUpReticleSize = reticleSize * 1.72
        deliberatelyMessedUpReticleSize = clamp(minReticleSize,
                                                deliberatelyMessedUpReticleSize,
                                                maxReticleSize)

        self.as_updateReticle(reticle.reticleType.reticleId, deliberatelyMessedUpReticleSize)

    def __onMarkerCreate(self, markerName, reticleType):
        if markerName in self._markerPresence or reticleType.flashLayer != self._layer:
            return

        self.as_createMarker(reticleType.reticleId, markerName)
        self._markerPresence.append(markerName)

    def __onMarkerDestroy(self, markerName, reticleType):
        if markerName not in self._markerPresence:
            return

        self._markerPresence.remove(markerName)
        self.as_destroyMarker(markerName)

    def __onMarkerDataProviderAttach(self, markerName, dataProvider):
        if markerName not in self._markerPresence:
            return

        self._markerDataProviders[markerName] = dataProvider

        self.as_setMarkerDataProviderPresence(markerName, True)

    def __onMarkerDataProviderDetach(self, markerName):
        if markerName not in self._markerPresence:
            return

        self.as_setMarkerDataProviderPresence(markerName, False)

        if markerName in self._markerDataProviders:
            del self._markerDataProviders[markerName]

    # IMPORTANT
    # those methods are called by an swf app every frame in-between game logic
    # even on its pause in replays
    #
    # most notable afraid of py_getNormalizedMarkerPosition method being called just
    # because it accesses data providers
    #
    # I generally didn't see in WG code any special synchronization in such cases, so I assume
    # that game engine and AVM handle it for us to some extent
    # or maybe those calls are not fully parallel?

    def py_warn(self, message):
        logger.warn("[DispersionReticleFlash] %s", message)

    def py_getScreenResolution(self):
        screenResolution = GUI.screenResolution()
        return [screenResolution[0], screenResolution[1]]

    def py_getNormalizedMarkerPosition(self, markerName):
        # this method should be called by swf app only if there is created marker
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

    def __onConfigReload(self):
        serializedConfig = {
            "focused-reticle-extended": self.__serializeFocusedReticleExtendedSection(),
            "hybrid-reticle-extended": self.__serializeHybridReticleExtendedSection(),
            "server-reticle-extended": self.__serializeServerReticleExtendedSection()
        }

        self.as_onConfigReload(serializedConfig)

    def __serializeFocusedReticleExtendedSection(self):
        return {
            "color": self.__serializeColorTuple(g_configParams.focusedReticleExtendedColor()),
            "shape": g_configParams.focusedReticleExtendedShape(),
            "center-dot-size": g_configParams.focusedReticleExtendedCenterDotSize(),
            "draw-outline": g_configParams.focusedReticleExtendedDrawOutline(),
            "blend": g_configParams.focusedReticleExtendedBlend(),
            "alpha": g_configParams.focusedReticleExtendedAlpha(),
            "shapes": self.__serializeFocusedReticleShapesSection()
        }

    def __serializeFocusedReticleShapesSection(self):
        return {
            "pentagon": {
                "width": g_configParams.focusedReticleExtendedShapesPentagonWidth(),
                "height": g_configParams.focusedReticleExtendedShapesPentagonHeight()
            },
            "t-shape": {
                "thickness": g_configParams.focusedReticleExtendedShapesTShapeThickness(),
                "length": g_configParams.focusedReticleExtendedShapesTShapeLength()
            }
        }

    def __serializeHybridReticleExtendedSection(self):
        return {
            "color": self.__serializeColorTuple(g_configParams.hybridReticleExtendedColor()),
            "shape": g_configParams.hybridReticleExtendedShape(),
            "center-dot-size": g_configParams.hybridReticleExtendedCenterDotSize(),
            "draw-outline": g_configParams.hybridReticleExtendedDrawOutline(),
            "blend": g_configParams.hybridReticleExtendedBlend(),
            "alpha": g_configParams.hybridReticleExtendedAlpha(),
            "shapes": self.__serializeHybridReticleShapesSection()
        }

    def __serializeHybridReticleShapesSection(self):
        return {
            "pentagon": {
                "width": g_configParams.hybridReticleExtendedShapesPentagonWidth(),
                "height": g_configParams.hybridReticleExtendedShapesPentagonHeight()
            },
            "t-shape": {
                "thickness": g_configParams.hybridReticleExtendedShapesTShapeThickness(),
                "length": g_configParams.hybridReticleExtendedShapesTShapeLength()
            }
        }

    def __serializeServerReticleExtendedSection(self):
        return {
            "color": self.__serializeColorTuple(g_configParams.serverReticleExtendedColor()),
            "shape": g_configParams.serverReticleExtendedShape(),
            "center-dot-size": g_configParams.serverReticleExtendedCenterDotSize(),
            "draw-outline": g_configParams.serverReticleExtendedDrawOutline(),
            "blend": g_configParams.serverReticleExtendedBlend(),
            "alpha": g_configParams.serverReticleExtendedAlpha(),
            "shapes": self.__serializeServerReticleShapesSection()
        }

    def __serializeServerReticleShapesSection(self):
        return {
            "pentagon": {
                "width": g_configParams.serverReticleExtendedShapesPentagonWidth(),
                "height": g_configParams.serverReticleExtendedShapesPentagonHeight()
            },
            "t-shape": {
                "thickness": g_configParams.serverReticleExtendedShapesTShapeThickness(),
                "length": g_configParams.serverReticleExtendedShapesTShapeLength()
            }
        }

    @staticmethod
    def __serializeColorTuple(colorTuple):
        red, green, blue = colorTuple

        color = 0
        color |= red << 16
        color |= green << 8
        color |= blue

        return color


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
