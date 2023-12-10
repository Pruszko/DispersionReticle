import logging
import os

from dispersionreticle.settings import loadConfigDict, createFolderSafely, getDefaultConfigTokens
from dispersionreticle.settings.templates.config_focused_reticle_template import CONFIG_FOCUSED_RETICLE_TEMPLATE
from dispersionreticle.settings.templates.config_hybrid_reticle_template import CONFIG_HYBRID_RETICLE_TEMPLATE
from dispersionreticle.settings.templates.config_server_reticle_template import CONFIG_SERVER_RETICLE_TEMPLATE
from dispersionreticle.settings.templates.config_template import CONFIG_TEMPLATE


logger = logging.getLogger(__name__)


CONFIG_FILE_DIR = os.path.join("mods", "configs", "DispersionReticle")


class ConfigFile(object):

    def __init__(self, configTemplate, configFilePath):
        self.configTemplate = configTemplate
        self.configFilePath = configFilePath

        self.configDict = {}

    def loadConfigDict(self):
        self.configDict = loadConfigDict(self.configFilePath)

    def writeConfigDict(self):
        configTokens = self.flattenConfigDictToTokens(self.configDict)
        self.writeConfigTokens(configTokens)

    def writeConfigTokens(self, configTokens):
        with open(self.configFilePath, "w") as configFile:
            configContent = self.configTemplate % configTokens
            configFile.write(configContent)

    def flattenConfigDictToTokens(self, configDict):
        from dispersionreticle.settings.config_param import g_configParams

        flattenedConfigDict = {}
        for tokenName, param in g_configParams.items():
            value = param.readValueFromConfigDict(configDict)

            if value is None:
                continue

            flattenedConfigDict[tokenName] = param.toJsonValue(value)
        return flattenedConfigDict

    def exists(self):
        return os.path.isfile(self.configFilePath)


class ConfigFiles(object):

    def __init__(self):
        self.config = ConfigFile(CONFIG_TEMPLATE, os.path.join(CONFIG_FILE_DIR, "config.json"))
        self.configFocusedReticle = ConfigFile(CONFIG_FOCUSED_RETICLE_TEMPLATE, os.path.join(CONFIG_FILE_DIR, "focused-reticle.json"))
        self.configLatencyReticle = ConfigFile(CONFIG_HYBRID_RETICLE_TEMPLATE, os.path.join(CONFIG_FILE_DIR, "hybrid-reticle.json"))
        self.configServerReticle = ConfigFile(CONFIG_SERVER_RETICLE_TEMPLATE, os.path.join(CONFIG_FILE_DIR, "server-reticle.json"))

        self.allConfigFiles = [self.config,
                               self.configFocusedReticle, self.configLatencyReticle, self.configServerReticle]

    def loadConfigDict(self):
        for configFile in self.allConfigFiles:
            configFile.loadConfigDict()

    def writeConfigDicts(self):
        for configFile in self.allConfigFiles:
            configFile.writeConfigDict()

    def writeConfigTokens(self, configTokens):
        for configFile in self.allConfigFiles:
            configFile.writeConfigTokens(configTokens)

    def areAllExists(self):
        return all(configFile.exists() for configFile in self.allConfigFiles)

    def areAllValid(self):
        return all(configFile.configDict is not None for configFile in self.allConfigFiles)

    def createMissingConfigFiles(self):
        logger.info("Checking configs existence ...")
        if g_configFiles.areAllExists():
            logger.info("Configs already exists.")
            return

        logger.info("Creating config directory ...")
        createFolderSafely(CONFIG_FILE_DIR)

        logger.info("Creating missing config files ...")

        defaultConfigTokens = getDefaultConfigTokens()
        for configFile in self.allConfigFiles:
            if configFile.exists():
                continue

            configFile.writeConfigTokens(defaultConfigTokens)


g_configFiles = ConfigFiles()
