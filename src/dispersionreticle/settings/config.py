import logging
import os

import Event
import Keys
import game

from dispersionreticle.settings import getDefaultConfigContent, loadConfigDict, toBool, toPositiveFloat, \
    createFolderSafely
from dispersionreticle.settings.migrations import performMigrationsIfNecessary
from dispersionreticle.utils import *

logger = logging.getLogger(__name__)


class _ReticleConfig(object):

    def __init__(self, section):
        self.enabled = toBool(section["enabled"])
        pass


class _LatencyReticleConfig(_ReticleConfig):
    
    def __init__(self, section):
        super(_LatencyReticleConfig, self).__init__(section)
        self.hideStandardReticle = toBool(section["hide-standard-reticle"])


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

            reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

            self.dispersionReticle = dispersionReticle
            self.latencyReticle = latencyReticle
            self.serverReticle = serverReticle

            self.__reticleSizeMultiplier = reticleSizeMultiplier

            logger.info("Finished config loading.")
        except Exception as e:
            print(e)
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
        return self.latencyReticle.enabled or self.serverReticle.enabled

    def shouldHideStandardReticle(self):
        return self.latencyReticle.enabled and self.latencyReticle.hideStandardReticle


g_config = Config()


@overrideIn(game)
def handleKeyEvent(func, event):
    if event.isKeyDown() and event.isCtrlDown():
        if event.key == Keys.KEY_P:
            g_config.loadConfigSafely()
            g_config.onConfigReload()

    return func(event)
