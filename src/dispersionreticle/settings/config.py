import logging
import os

import Event
import Keys
import game

from dispersionreticle.settings import getDefaultConfigContent, loadConfigDict, \
    createFolderSafely, getDefaultConfigReplaceTokens, CONFIG_TEMPLATE
from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.settings.migrations import performMigrationsIfNecessary
from dispersionreticle.utils import *
from dispersionreticle.utils.debug_state import g_debugStateCollector

logger = logging.getLogger(__name__)


class _DispersionReticleConfig(object):

    @property
    def enabled(self):
        return enabledAware(g_configParams.dispersionReticleEnabled)

    def writeJsonValuesSafely(self, configDict):
        writeJsonValueSafely(configDict, g_configParams.dispersionReticleEnabled)


class _ServerReticleConfig(object):

    @property
    def enabled(self):
        return enabledAware(g_configParams.serverReticleEnabled)

    def writeJsonValuesSafely(self, configDict):
        writeJsonValueSafely(configDict, g_configParams.serverReticleEnabled)


class _LatencyReticleConfig(object):

    @property
    def enabled(self):
        return enabledAware(g_configParams.latencyReticleEnabled)

    @property
    def hideStandardReticle(self):
        return enabledAware(g_configParams.latencyReticleHideStandardReticle)

    def writeJsonValuesSafely(self, configDict):
        writeJsonValueSafely(configDict, g_configParams.latencyReticleEnabled)
        writeJsonValueSafely(configDict, g_configParams.latencyReticleHideStandardReticle)


class _SimpleServerReticleConfig(object):

    @property
    def enabled(self):
        return enabledAware(g_configParams.simpleServerReticleEnabled)

    @property
    def shape(self):
        return enabledAware(g_configParams.simpleServerReticleShape)

    @property
    def color(self):
        return enabledAware(g_configParams.simpleServerReticleColor)

    @property
    def drawOutline(self):
        return enabledAware(g_configParams.simpleServerReticleDrawOutline)

    @property
    def blend(self):
        return enabledAware(g_configParams.simpleServerReticleBlend)

    @property
    def alpha(self):
        return enabledAware(g_configParams.simpleServerReticleAlpha)

    def writeJsonValuesSafely(self, configDict):
        writeJsonValueSafely(configDict, g_configParams.simpleServerReticleEnabled)
        writeJsonValueSafely(configDict, g_configParams.simpleServerReticleShape)
        writeJsonValueSafely(configDict, g_configParams.simpleServerReticleColor)
        writeJsonValueSafely(configDict, g_configParams.simpleServerReticleDrawOutline)
        writeJsonValueSafely(configDict, g_configParams.simpleServerReticleBlend)
        writeJsonValueSafely(configDict, g_configParams.simpleServerReticleAlpha)


class Config:

    def __init__(self):
        self.__configFileDir = os.path.join("mods", "configs", "DispersionReticle")
        self.__configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

        self.enabled = g_configParams.enabled.value

        self.dispersionReticle = _DispersionReticleConfig()
        self.latencyReticle = _LatencyReticleConfig()
        self.serverReticle = _ServerReticleConfig()
        self.simpleServerReticle = _SimpleServerReticleConfig()

        self.reticleSizeMultiplier = g_configParams.reticleSizeMultiplier.value

        self.__eventManager = Event.EventManager()
        self.onConfigReload = Event.Event(self.__eventManager)

    def refreshGameState(self):
        self.onConfigReload()

        if debug_state.IS_DEBUGGING:
            g_debugStateCollector.collectStateAfterConfigReload()

    def loadConfigSafely(self):
        try:
            logger.info("Starting config loading ...")
            self.createConfigIfNotExists()

            performMigrationsIfNecessary()

            data = loadConfigDict(self.__configFilePath)

            if data is None:
                return

            self.enabled = writeJsonValueSafely(data, g_configParams.enabled)

            self.dispersionReticle.writeJsonValuesSafely(data)
            self.latencyReticle.writeJsonValuesSafely(data)
            self.serverReticle.writeJsonValuesSafely(data)
            self.simpleServerReticle.writeJsonValuesSafely(data)

            self.reticleSizeMultiplier = writeJsonValueSafely(data, g_configParams.reticleSizeMultiplier)

            logger.info("Finished config loading.")
        except Exception as e:
            logger.error("Failed to load (or create) config", exc_info=e)

    def updateConfigSafely(self, serializedSettings):
        # reload config prior to saving
        # to make sure everything is created
        # and potentially migrated
        self.loadConfigSafely()

        try:
            logger.info("Starting config saving ...")

            tokens = getDefaultConfigReplaceTokens()
            tokens.update(serializedSettings)

            newConfigFileContent = CONFIG_TEMPLATE % tokens

            with open(self.__configFilePath, "w") as configFile:
                configFile.write(newConfigFileContent)

            logger.info("Finished config saving.")
        except Exception as e:
            logger.error("Failed to save config", exc_info=e)

        # reload config again to update our mod internal config state
        # with changes written to config file
        self.loadConfigSafely()
        self.onConfigReload()

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

    def isServerAimRequired(self):
        return self.latencyReticle.enabled or \
               self.serverReticle.enabled or \
               self.simpleServerReticle.enabled

    def shouldHideStandardReticle(self):
        return self.latencyReticle.enabled and self.latencyReticle.hideStandardReticle


def writeJsonValueSafely(configDict, param):
    jsonValue = param.readJsonValueFromConfigDictSafely(configDict)
    param.jsonValue = jsonValue
    return param.value


def enabledAware(param):
    if not g_config.enabled:
        return param.disabledValue
    return param.value


g_config = Config()


@overrideIn(game)
def handleKeyEvent(func, event):
    if event.isKeyDown() and event.isCtrlDown():
        if event.key == Keys.KEY_P:
            g_config.loadConfigSafely()
            g_config.refreshGameState()

    return func(event)
