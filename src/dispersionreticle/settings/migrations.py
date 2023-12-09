import os
import logging

from dispersionreticle.settings import copy, deleteEmptyFolderSafely, loadConfigDict, CONFIG_TEMPLATE
from dispersionreticle.settings.config_param import g_configParams

logger = logging.getLogger(__name__)


class ConfigVersion(object):

    V2_0_X = 0
    V2_1_X = 1
    V2_2_X = 2
    V2_3_X = 3
    V2_4_X = 4
    V2_6_X = 5

    CURRENT = V2_6_X


def performConfigMigrations():
    configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

    v2_0_2_migrateConfigFileLocation(configFilePath)

    if not os.path.isfile(configFilePath):
        return

    configDict = loadConfigDict(configFilePath)
    if configDict is None:
        return

    if isVersion(configDict, ConfigVersion.CURRENT):
        return

    v2_1_0_addOptionLatencyReticleHideStandardReticle(configDict)
    v2_2_0_addSimpleServerReticle(configDict)
    v2_3_0_addNewSimpleServerReticleFeatures(configDict)
    v2_4_0_addSupportForModsSettingsAPI(configDict)
    v2_6_0_addDrawCenterDotToSimpleServerReticle(configDict)

    configTokens = flattenConfigDictToTokens(configDict)
    configContent = CONFIG_TEMPLATE % configTokens

    with open(configFilePath, "w") as configFile:
        configFile.write(configContent)


def v2_0_2_migrateConfigFileLocation(newConfigFilePath):
    legacyConfigDir = os.path.join("mods", "config")
    legacyConfigFileDir = os.path.join("mods", "config", "DispersionReticle")
    legacyConfigFilePath = os.path.join("mods", "config", "DispersionReticle", "config.json")

    # handle config folder name that differs from other mod configs folder
    if not os.path.isfile(legacyConfigFilePath):
        return

    logger.info("Legacy config location detected, moving file to new location ...")

    # move copy config to new location
    copy(legacyConfigFilePath, newConfigFilePath)

    # remove previous config
    os.remove(legacyConfigFilePath)

    # remove previous folders if they are empty
    deleteEmptyFolderSafely(legacyConfigFileDir)
    deleteEmptyFolderSafely(legacyConfigDir)

    logger.info("Finished moving config file to new location.")


def v2_1_0_addOptionLatencyReticleHideStandardReticle(configDict):
    if not isVersion(configDict, ConfigVersion.V2_0_X):
        return

    logger.info("Migrating config file from version 2.0.x to 2.1.0 ...")

    configDict["dispersion-reticle"] = {}
    configDict["dispersion-reticle"]["enabled"] = configDict["dispersion-reticle-enabled"]
    configDict["latency-reticle"] = {}
    configDict["latency-reticle"]["enabled"] = configDict["latency-reticle-enabled"]
    configDict["latency-reticle"]["hide-standard-reticle"] = False
    configDict["server-reticle"] = {}
    configDict["server-reticle"]["enabled"] = configDict["server-reticle-enabled"]

    del configDict["dispersion-reticle-enabled"]
    del configDict["latency-reticle-enabled"]
    del configDict["server-reticle-enabled"]

    progressVersion(configDict)

    logger.info("Migration finished.")


def v2_2_0_addSimpleServerReticle(configDict):
    if not isVersion(configDict, ConfigVersion.V2_1_X):
        return

    logger.info("Migrating config file from version 2.1.x to 2.2.0 ...")

    configDict["simple-server-reticle"] = {}
    configDict["simple-server-reticle"]["enabled"] = False
    configDict["simple-server-reticle"]["color"] = (255, 0, 255)
    configDict["simple-server-reticle"]["alpha"] = 1.0
    progressVersion(configDict)

    logger.info("Migration finished.")


def v2_3_0_addNewSimpleServerReticleFeatures(configDict):
    if not isVersion(configDict, ConfigVersion.V2_2_X):
        return

    logger.info("Migrating config file from version 2.2.x to 2.3.0 ...")

    configDict["simple-server-reticle"]["shape"] = "pentagon"
    configDict["simple-server-reticle"]["draw-outline"] = False
    configDict["simple-server-reticle"]["blend"] = 0.0
    progressVersion(configDict)

    logger.info("Migration finished.")


def v2_4_0_addSupportForModsSettingsAPI(configDict):
    if not isVersion(configDict, ConfigVersion.V2_3_X):
        return

    logger.info("Migrating config file from version 2.3.x to 2.4.0 ...")

    configDict["enabled"] = True
    progressVersion(configDict)

    logger.info("Migration finished.")


def v2_6_0_addDrawCenterDotToSimpleServerReticle(configDict):
    if not isVersion(configDict, ConfigVersion.V2_4_X):
        return

    logger.info("Migrating config file from version 2.4.x to 2.6.0 ...")

    configDict["simple-server-reticle"]["draw-center-dot"] = False
    progressVersion(configDict)

    logger.info("Migration finished.")


def flattenConfigDictToTokens(configDict):
    flattenedConfigDict = {}
    for tokenName, param in g_configParams.items():
        value = param.readValueFromConfigDictSafely(configDict)
        flattenedConfigDict[tokenName] = param.toJsonValue(value)
    return flattenedConfigDict


def progressVersion(configDict):
    if "__version__" not in configDict:
        configDict["__version__"] = ConfigVersion.V2_1_X
        return

    configDict["__version__"] = int(configDict["__version__"]) + 1


def isVersion(configDict, version):
    if "__version__" not in configDict:
        return ConfigVersion.V2_0_X == version

    return int(configDict["__version__"]) == version
