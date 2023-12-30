import json
import logging
import os
import re

from dispersionreticle.settings import createFolderSafely, getDefaultConfigTokens, ConfigException
from dispersionreticle.settings.config_template import CONFIG_TEMPLATE


logger = logging.getLogger(__name__)


CONFIG_FILE_DIR = os.path.join("mods", "configs", "DispersionReticle")


class ConfigFile(object):

    def __init__(self, configTemplate, configFilePath):
        self.configTemplate = configTemplate
        self.configFilePath = configFilePath

    def loadConfigDict(self):
        try:
            with open(self.configFilePath, "r") as configFile:
                jsonRawData = configFile.read()

            jsonData = re.sub(r"^ *//.*$", "", jsonRawData, flags=re.MULTILINE)
            return json.loads(jsonData, encoding="UTF-8")
        except ValueError as e:
            logger.error("Failed to read config file because it is not a valid JSON object.", exc_info=True)
            raise ConfigException("Failed to read config file (probably invalid JSON syntax).\n"
                                  "Check config file content for any typos and reload it with CTRL + P.\n"
                                  "Message: " + e.message)
        except Exception:
            logger.error("Unknown error occurred while loading config file.", exc_info=True)
            raise ConfigException("Failed to read config file due to unknown error.\n"
                                  "Contact mod developer for further support with provided logs.")

    def writeConfigDict(self, configDict):
        configTokens = self.flattenConfigDictToTokens(configDict)
        self.writeConfigTokens(configTokens)

    def writeConfigTokens(self, configTokens):
        try:
            with open(self.configFilePath, "w") as configFile:
                configContent = self.configTemplate % configTokens
                configFile.write(configContent)
        except Exception:
            logger.error("Failed to write to config file.", exc_info=True)
            raise ConfigException("Failed to write to config file due to unknown error.\n"
                                  "Contact mod developer for further support with provided logs.")

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

    def createMissingConfigFiles(self):
        if self.config.exists():
            return

        createFolderSafely(CONFIG_FILE_DIR)

        defaultConfigTokens = getDefaultConfigTokens()
        self.config.writeConfigTokens(defaultConfigTokens)

        logger.info("Created default config file.")


g_configFiles = ConfigFiles()
