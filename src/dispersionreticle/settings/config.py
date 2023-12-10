import logging

import Event
import Keys
import game

from dispersionreticle.settings import getDefaultConfigTokens
from dispersionreticle.settings.config_file import g_configFiles
from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.settings.migrations import performConfigMigrations
from dispersionreticle.utils import *
from dispersionreticle.utils import debug_state
from dispersionreticle.utils.debug_state import g_debugStateCollector

logger = logging.getLogger(__name__)


class Config(object):

    def __init__(self):
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
            g_configFiles.createMissingConfigFiles()
            g_configFiles.loadConfigDict()

            if not g_configFiles.areAllValid():
                return

            for tokenName, param in g_configParams.items():
                value = param.readValueFromConfigFile()
                value = value if value is not None else param.defaultValue

                param.jsonValue = value

            logger.info("Finished config loading.")
        except Exception as e:
            logger.error("Failed to load (or create) config", exc_info=e)

    def updateConfigSafely(self, rawSerializedSettings):
        # reload config prior to saving
        # to make sure everything is created
        # and potentially migrated
        self.loadConfigSafely()

        try:
            logger.info("Starting config saving ...")

            serializedSettings = getDefaultConfigTokens()
            serializedSettings.update(rawSerializedSettings)

            g_configFiles.writeConfigTokens(serializedSettings)

            logger.info("Finished config saving.")
        except Exception as e:
            logger.error("Failed to save config", exc_info=e)

        # reload config again to update our mod internal config state
        # with changes written to config file
        self.loadConfigSafely()
        self.onConfigReload()


g_config = Config()


@overrideIn(game)
def handleKeyEvent(func, event):
    if event.isKeyDown() and event.isCtrlDown():
        if event.key == Keys.KEY_P:
            g_config.loadConfigSafely()
            g_config.refreshGameState()

    return func(event)
