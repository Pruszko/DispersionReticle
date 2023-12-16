import os
import logging

from dispersionreticle.settings import copy, deleteEmptyFolderSafely
from dispersionreticle.settings.config_file import g_configFiles

logger = logging.getLogger(__name__)


class ConfigVersion(object):

    V2_0_X = 0
    V2_1_X = 1
    V2_2_X = 2
    V2_3_X = 3
    V2_4_X = 4
    V2_6_X = 5
    V3_0_X = 6

    CURRENT = V3_0_X


def performConfigMigrations():
    v2_0_2_migrateConfigFileLocation()

    if not g_configFiles.config.exists():
        return

    g_configFiles.config.loadConfigDict()
    configDict = g_configFiles.config.configDict

    if configDict is None:
        return

    if isVersion(configDict, ConfigVersion.CURRENT):
        return

    v2_1_0_addOptionLatencyReticleHideStandardReticle()
    v2_2_0_addSimpleServerReticle()
    v2_3_0_addNewSimpleServerReticleFeatures()
    v2_4_0_addSupportForModsSettingsAPI()
    v2_6_0_addDrawCenterDotToSimpleServerReticle()

    v3_0_0_addNewReticlesAndNewFeatures()

    g_configFiles.writeConfigDicts()


def v2_0_2_migrateConfigFileLocation():
    legacyConfigDir = os.path.join("mods", "config")
    legacyConfigFileDir = os.path.join("mods", "config", "DispersionReticle")
    legacyConfigFilePath = os.path.join("mods", "config", "DispersionReticle", "config.json")

    # handle config folder name that differs from other mod configs folder
    if not os.path.isfile(legacyConfigFilePath):
        return

    logger.info("Legacy config location detected, moving file to new location ...")

    newConfigFilePath = g_configFiles.config.configFilePath

    # move copy config to new location
    copy(legacyConfigFilePath, newConfigFilePath)

    # remove previous config
    os.remove(legacyConfigFilePath)

    # remove previous folders if they are empty
    deleteEmptyFolderSafely(legacyConfigFileDir)
    deleteEmptyFolderSafely(legacyConfigDir)

    logger.info("Finished moving config file to new location.")


def v2_1_0_addOptionLatencyReticleHideStandardReticle():
    configDict = g_configFiles.config.configDict

    if not isVersion(configDict, ConfigVersion.V2_0_X):
        return

    logger.info("Migrating config file from version 2.0.x to 2.1.x ...")

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


def v2_2_0_addSimpleServerReticle():
    configDict = g_configFiles.config.configDict
    if not isVersion(configDict, ConfigVersion.V2_1_X):
        return

    logger.info("Migrating config file from version 2.1.x to 2.2.x ...")

    configDict["simple-server-reticle"] = {}
    configDict["simple-server-reticle"]["enabled"] = False
    configDict["simple-server-reticle"]["color"] = (255, 0, 255)
    configDict["simple-server-reticle"]["alpha"] = 1.0
    progressVersion(configDict)

    logger.info("Migration finished.")


def v2_3_0_addNewSimpleServerReticleFeatures():
    configDict = g_configFiles.config.configDict
    if not isVersion(configDict, ConfigVersion.V2_2_X):
        return

    logger.info("Migrating config file from version 2.2.x to 2.3.x ...")

    configDict["simple-server-reticle"]["shape"] = "pentagon"
    configDict["simple-server-reticle"]["draw-outline"] = False
    configDict["simple-server-reticle"]["blend"] = 0.0
    progressVersion(configDict)

    logger.info("Migration finished.")


def v2_4_0_addSupportForModsSettingsAPI():
    configDict = g_configFiles.config.configDict
    if not isVersion(configDict, ConfigVersion.V2_3_X):
        return

    logger.info("Migrating config file from version 2.3.x to 2.4.x ...")

    configDict["enabled"] = True
    progressVersion(configDict)

    logger.info("Migration finished.")


def v2_6_0_addDrawCenterDotToSimpleServerReticle():
    configDict = g_configFiles.config.configDict
    if not isVersion(configDict, ConfigVersion.V2_4_X):
        return

    logger.info("Migrating config file from version 2.4.x to 2.6.x ...")

    configDict["simple-server-reticle"]["draw-center-dot"] = False
    progressVersion(configDict)

    logger.info("Migration finished.")


def v3_0_0_addNewReticlesAndNewFeatures():
    configDict = g_configFiles.config.configDict
    if not isVersion(configDict, ConfigVersion.V2_6_X):
        return

    logger.info("Migrating config file from version 2.6.x to 3.0.x ...")

    # focused reticle
    configDict["focused-reticle"] = {}
    configDict["focused-reticle"]["enabled"] = configDict["dispersion-reticle"]["enabled"]
    configDict["focused-reticle"]["type"] = "default"
    del configDict["dispersion-reticle"]

    # focused reticle extended
    configDict["focused-reticle-extended"] = {}
    configDict["focused-reticle-extended"]["enabled"] = False
    configDict["focused-reticle-extended"]["shape"] = "circle"
    configDict["focused-reticle-extended"]["color"] = (255, 255, 0)
    configDict["focused-reticle-extended"]["draw-center-dot"] = False
    configDict["focused-reticle-extended"]["draw-outline"] = False
    configDict["focused-reticle-extended"]["blend"] = 0.5
    configDict["focused-reticle-extended"]["alpha"] = 1.0

    # hybrid reticle
    configDict["hybrid-reticle"] = {}
    configDict["hybrid-reticle"]["enabled"] = configDict["latency-reticle"]["enabled"]
    configDict["hybrid-reticle"]["type"] = "default"
    configDict["hybrid-reticle"]["hide-standard-reticle"] = configDict["latency-reticle"]["hide-standard-reticle"]
    del configDict["latency-reticle"]

    # hybrid reticle extended
    configDict["hybrid-reticle-extended"] = {}
    configDict["hybrid-reticle-extended"]["enabled"] = False
    configDict["hybrid-reticle-extended"]["shape"] = "circle"
    configDict["hybrid-reticle-extended"]["color"] = (0, 255, 255)
    configDict["hybrid-reticle-extended"]["draw-center-dot"] = False
    configDict["hybrid-reticle-extended"]["draw-outline"] = False
    configDict["hybrid-reticle-extended"]["blend"] = 0.5
    configDict["hybrid-reticle-extended"]["alpha"] = 1.0

    # server reticle
    configDict["server-reticle"]["type"] = "purple"

    # server reticle extended
    configDict["server-reticle-extended"] = {}
    configDict["server-reticle-extended"]["enabled"] = configDict["simple-server-reticle"]["enabled"]
    configDict["server-reticle-extended"]["shape"] = configDict["simple-server-reticle"]["shape"]
    configDict["server-reticle-extended"]["color"] = configDict["simple-server-reticle"]["color"]
    configDict["server-reticle-extended"]["draw-center-dot"] = configDict["simple-server-reticle"]["draw-center-dot"]
    configDict["server-reticle-extended"]["draw-outline"] = configDict["simple-server-reticle"]["draw-outline"]
    configDict["server-reticle-extended"]["blend"] = configDict["simple-server-reticle"]["blend"]
    configDict["server-reticle-extended"]["alpha"] = configDict["simple-server-reticle"]["alpha"]
    del configDict["simple-server-reticle"]

    progressVersion(configDict)

    logger.info("Migration finished.")


def progressVersion(configDict):
    if "__version__" not in configDict:
        configDict["__version__"] = ConfigVersion.V2_1_X
        return

    configDict["__version__"] = int(configDict["__version__"]) + 1


def isVersion(configDict, version):
    if "__version__" not in configDict:
        return ConfigVersion.V2_0_X == version

    return int(configDict["__version__"]) == version
