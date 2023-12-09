import logging
import os

import Event
import Keys
import game

from dispersionreticle.settings import getDefaultConfigContent, loadConfigDict, \
    createFolderSafely, getDefaultConfigTokens, CONFIG_TEMPLATE
from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.settings.migrations import performConfigMigrations
from dispersionreticle.utils import *
from dispersionreticle.utils import debug_state
from dispersionreticle.utils.debug_state import g_debugStateCollector

logger = logging.getLogger(__name__)


class Config:

    def __init__(self):
        self.__configFileDir = os.path.join("mods", "configs", "DispersionReticle")
        self.__configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

        self.__eventManager = Event.EventManager()
        self.onConfigReload = Event.Event(self.__eventManager)

    def refreshGameState(self):
        self.onConfigReload()

        if debug_state.IS_DEBUGGING:
            g_debugStateCollector.collectStateAfterConfigReload()

    def loadConfigSafely(self):
        try:
            logger.info("Starting config loading ...")

            performConfigMigrations()
            self.createConfigIfNotExists()

            data = loadConfigDict(self.__configFilePath)

            if data is None:
                return

            for tokenName, param in g_configParams.items():
                value = param.readValueFromConfigDictSafely(data)
                param.jsonValue = value

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

            defaultConfigTokens = getDefaultConfigTokens()
            defaultConfigTokens.update(serializedSettings)

            newConfigFileContent = CONFIG_TEMPLATE % defaultConfigTokens

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


g_config = Config()


@overrideIn(game)
def handleKeyEvent(func, event):
    if event.isKeyDown() and event.isCtrlDown():
        if event.key == Keys.KEY_P:
            g_config.loadConfigSafely()
            g_config.refreshGameState()

    return func(event)
