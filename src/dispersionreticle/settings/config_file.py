import logging
import os

from dispersionreticle.settings import loadConfigDict, createFolderSafely, getDefaultConfigTokens
from dispersionreticle.settings.config_template import CONFIG_TEMPLATE


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

    def loadConfigDict(self):
        self.config.loadConfigDict()

    def writeConfigDicts(self):
        self.config.writeConfigDict()

    def writeConfigTokens(self, configTokens):
        self.config.writeConfigTokens(configTokens)

    def areAllExists(self):
        return self.config.exists()

    def areAllValid(self):
        return self.config.configDict is not None

    def createMissingConfigFiles(self):
        logger.info("Checking config existence ...")
        if self.areAllExists():
            logger.info("Config already exists.")
            return

        logger.info("Creating config directory ...")
        createFolderSafely(CONFIG_FILE_DIR)

        logger.info("Creating missing config files ...")

        defaultConfigTokens = getDefaultConfigTokens()
        if self.config.exists():
            return

        self.config.writeConfigTokens(defaultConfigTokens)


g_configFiles = ConfigFiles()
