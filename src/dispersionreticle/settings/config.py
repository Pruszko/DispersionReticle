import logging
import os

import Event
import Keys
import game

from dispersionreticle.settings import getDefaultConfigContent, loadConfigDict, toBool, toPositiveFloat, \
    createFolderSafely, toColorTuple, clamp
from dispersionreticle.settings.migrations import performMigrationsIfNecessary
from dispersionreticle.utils import *
from dispersionreticle.utils.debug_state import g_debugStateCollector

logger = logging.getLogger(__name__)

VALID_SIMPLE_SERVER_RETICLE_SHAPES = ["pentagon", "t-shape", "circle", "dashed"]


class _ReticleConfig(object):

    def __init__(self, section):
        self.enabled = toBool(section["enabled"])
        pass


class _LatencyReticleConfig(_ReticleConfig):
    
    def __init__(self, section):
        super(_LatencyReticleConfig, self).__init__(section)
        self.hideStandardReticle = toBool(section["hide-standard-reticle"])


class _SimpleServerReticleConfig(_ReticleConfig):

    def __init__(self, section):
        super(_SimpleServerReticleConfig, self).__init__(section)

        rawShape = str(section["shape"]).lower()
        if rawShape not in VALID_SIMPLE_SERVER_RETICLE_SHAPES:
            raise Exception("Shape %s is not a valid value for simple server reticle" % rawShape)

        self.shape = rawShape
        self.color = toColorTuple(section["color"])
        self.drawOutline = toBool(section["draw-outline"])
        self.blend = clamp(0.0, toPositiveFloat(section["blend"]), 1.0)
        self.alpha = clamp(0.0, toPositiveFloat(section["alpha"]), 1.0)


class Config:

    def __init__(self):
        self.__configFileDir = os.path.join("mods", "configs", "DispersionReticle")
        self.__configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

        self.dispersionReticle = _ReticleConfig({
            "enabled": True,
        })
        self.latencyReticle = _LatencyReticleConfig({
            "enabled": False,
            "hide-standard-reticle": False,
        })
        self.serverReticle = _ReticleConfig({
            "enabled": False,
        })
        self.simpleServerReticle = _SimpleServerReticleConfig({
            "enabled": False,
            "shape": "pentagon",
            "color": (255, 0, 255),
            "draw-outline": False,
            "blend": 0.5,
            "alpha": 1.0
        })
        self.__reticleSizeMultiplier = 1.0

        self.__eventManager = Event.EventManager()
        self.onConfigReload = Event.Event(self.__eventManager)

    def loadConfigSafely(self):
        try:
            logger.info("Starting config loading ...")
            self.createConfigIfNotExists()

            performMigrationsIfNecessary()

            data = loadConfigDict(self.__configFilePath)

            dispersionReticle = _ReticleConfig(data["dispersion-reticle"])
            latencyReticle = _LatencyReticleConfig(data["latency-reticle"])
            serverReticle = _ReticleConfig(data["server-reticle"])
            simpleServerReticle = _SimpleServerReticleConfig(data["simple-server-reticle"])

            reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

            self.dispersionReticle = dispersionReticle
            self.latencyReticle = latencyReticle
            self.serverReticle = serverReticle
            self.simpleServerReticle = simpleServerReticle

            self.__reticleSizeMultiplier = reticleSizeMultiplier

            logger.info("Finished config loading.")
        except Exception as e:
            logger.error("Failed to load (or create) config", exc_info=e)

    def createConfigIfNotExists(self):
        logger.info("Checking config existence ...")
        if os.path.isfile(self.__configFilePath):
            logger.info("Config already exists.")
            return

        logger.info("Creating config directory ...")
        createFolderSafely(self.__configFileDir)

        logger.info("Creating config file ...")
        with open(self.__configFilePath, "w") as configFile:
            defaultConfigContent = getDefaultConfigContent()
            configFile.write(defaultConfigContent)

    def getReticleSizeMultiplier(self):
        return self.__reticleSizeMultiplier

    def isServerAimRequired(self):
        return self.latencyReticle.enabled or \
               self.serverReticle.enabled or \
               self.simpleServerReticle.enabled

    def shouldHideStandardReticle(self):
        return self.latencyReticle.enabled and self.latencyReticle.hideStandardReticle


g_config = Config()


@overrideIn(game)
def handleKeyEvent(func, event):
    if event.isKeyDown() and event.isCtrlDown():
        if event.key == Keys.KEY_P:
            g_config.loadConfigSafely()
            g_config.onConfigReload()

            if debug_state.IS_DEBUGGING:
                g_debugStateCollector.collectStateAfterConfigReload()

    return func(event)
