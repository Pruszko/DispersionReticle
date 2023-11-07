import os
import logging

from dispersionreticle.settings import toJson, toBool, copy, deleteEmptyFolderSafely, \
    loadConfigDict, toPositiveFloat, getDefaultConfigReplaceTokens, CONFIG_TEMPLATE, toColorTuple

logger = logging.getLogger(__name__)


def performMigrationsIfNecessary():
    v2_0_2_migrateConfigFileLocation()
    v2_1_0_addOptionLatencyReticleHideStandardReticle()
    v2_2_0_addSimpleServerReticle()
    v2_3_0_addNewSimpleServerReticleFeatures()
    v2_4_0_addSupportForModsSettingsAPI()
    v2_6_0_addDrawCenterDotToSimpleServerReticle()


def v2_0_2_migrateConfigFileLocation():
    legacyConfigDir = os.path.join("mods", "config")
    legacyConfigFileDir = os.path.join("mods", "config", "DispersionReticle")
    legacyConfigFilePath = os.path.join("mods", "config", "DispersionReticle", "config.json")

    newConfigFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

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


def v2_1_0_addOptionLatencyReticleHideStandardReticle():
    configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

    if not os.path.isfile(configFilePath):
        return

    data = loadConfigDict(configFilePath)

    if data is None or "__version__" in data:
        return

    logger.info("Migrating config file from version 2.0.x ...")

    dispersionReticleEnabled = toBool(data["dispersion-reticle-enabled"])
    latencyReticleEnabled = toBool(data["latency-reticle-enabled"])
    serverReticleEnabled = toBool(data["server-reticle-enabled"])
    reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

    tokens = getDefaultConfigReplaceTokens()
    tokens.update({
        "dispersion-reticle-enabled": toJson(dispersionReticleEnabled),
        "latency-reticle-enabled": toJson(latencyReticleEnabled),
        "server-reticle-enabled": toJson(serverReticleEnabled),
        "reticle-size-multiplier": toJson(reticleSizeMultiplier),
    })

    newConfigFileContent = CONFIG_TEMPLATE % tokens

    with open(configFilePath, "w") as configFile:
        configFile.write(newConfigFileContent)

    logger.info("Migration finished.")


def v2_2_0_addSimpleServerReticle():
    configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

    if not os.path.isfile(configFilePath):
        return

    data = loadConfigDict(configFilePath)

    if data is None or "__version__" not in data or data["__version__"] != 1:
        return

    logger.info("Migrating config file from version 2.1.x ...")

    dispersionReticleEnabled = toBool(data["dispersion-reticle"]["enabled"])

    latencyReticleEnabled = toBool(data["latency-reticle"]["enabled"])
    latencyReticleHideStandardReticle = toBool(data["latency-reticle"]["hide-standard-reticle"])
    serverReticleEnabled = toBool(data["server-reticle"]["enabled"])
    reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

    tokens = getDefaultConfigReplaceTokens()
    tokens.update({
        "dispersion-reticle-enabled": toJson(dispersionReticleEnabled),
        "latency-reticle-enabled": toJson(latencyReticleEnabled),
        "latency-reticle-hide-standard-reticle": toJson(latencyReticleHideStandardReticle),
        "server-reticle-enabled": toJson(serverReticleEnabled),
        "reticle-size-multiplier": toJson(reticleSizeMultiplier),
    })

    newConfigFileContent = CONFIG_TEMPLATE % tokens

    with open(configFilePath, "w") as configFile:
        configFile.write(newConfigFileContent)

    logger.info("Migration finished.")


def v2_3_0_addNewSimpleServerReticleFeatures():
    configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

    if not os.path.isfile(configFilePath):
        return

    data = loadConfigDict(configFilePath)

    if data is None or "__version__" not in data or data["__version__"] != 2:
        return

    logger.info("Migrating config file from version 2.2.x ...")

    dispersionReticleEnabled = toBool(data["dispersion-reticle"]["enabled"])

    latencyReticleEnabled = toBool(data["latency-reticle"]["enabled"])
    latencyReticleHideStandardReticle = toBool(data["latency-reticle"]["hide-standard-reticle"])

    serverReticleEnabled = toBool(data["server-reticle"]["enabled"])

    simpleServerReticleEnabled = toBool(data["simple-server-reticle"]["enabled"])
    simpleServerReticleColor = toColorTuple(data["simple-server-reticle"]["color"])
    simpleServerReticleAlpha = toPositiveFloat(data["simple-server-reticle"]["alpha"])

    reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

    tokens = getDefaultConfigReplaceTokens()
    tokens.update({
        "dispersion-reticle-enabled": toJson(dispersionReticleEnabled),
        "latency-reticle-enabled": toJson(latencyReticleEnabled),
        "latency-reticle-hide-standard-reticle": toJson(latencyReticleHideStandardReticle),
        "server-reticle-enabled": toJson(serverReticleEnabled),
        "simple-server-reticle-enabled": toJson(simpleServerReticleEnabled),
        "simple-server-reticle-color": toJson(simpleServerReticleColor),
        "simple-server-reticle-blend": toJson(0.0),
        "simple-server-reticle-alpha": toJson(simpleServerReticleAlpha),
        "reticle-size-multiplier": toJson(reticleSizeMultiplier),
    })

    newConfigFileContent = CONFIG_TEMPLATE % tokens

    with open(configFilePath, "w") as configFile:
        configFile.write(newConfigFileContent)

    logger.info("Migration finished.")


def v2_4_0_addSupportForModsSettingsAPI():
    configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

    if not os.path.isfile(configFilePath):
        return

    data = loadConfigDict(configFilePath)

    if data is None or "__version__" not in data or data["__version__"] != 3:
        return

    logger.info("Migrating config file from version 2.3.x ...")

    dispersionReticleEnabled = toBool(data["dispersion-reticle"]["enabled"])

    latencyReticleEnabled = toBool(data["latency-reticle"]["enabled"])
    latencyReticleHideStandardReticle = toBool(data["latency-reticle"]["hide-standard-reticle"])

    serverReticleEnabled = toBool(data["server-reticle"]["enabled"])

    simpleServerReticleEnabled = toBool(data["simple-server-reticle"]["enabled"])
    simpleServerReticleShape = data["simple-server-reticle"]["shape"]
    simpleServerReticleColor = toColorTuple(data["simple-server-reticle"]["color"])
    simpleServerReticleDrawOutline = toBool(data["simple-server-reticle"]["draw-outline"])
    simpleServerReticleBlend = toPositiveFloat(data["simple-server-reticle"]["blend"])
    simpleServerReticleAlpha = toPositiveFloat(data["simple-server-reticle"]["alpha"])

    reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

    tokens = getDefaultConfigReplaceTokens()
    tokens.update({
        "dispersion-reticle-enabled": toJson(dispersionReticleEnabled),
        "latency-reticle-enabled": toJson(latencyReticleEnabled),
        "latency-reticle-hide-standard-reticle": toJson(latencyReticleHideStandardReticle),
        "server-reticle-enabled": toJson(serverReticleEnabled),
        "simple-server-reticle-enabled": toJson(simpleServerReticleEnabled),
        "simple-server-reticle-color": toJson(simpleServerReticleColor),
        "simple-server-reticle-shape": toJson(simpleServerReticleShape),
        "simple-server-reticle-draw-outline": toJson(simpleServerReticleDrawOutline),
        "simple-server-reticle-blend": toJson(simpleServerReticleBlend),
        "simple-server-reticle-alpha": toJson(simpleServerReticleAlpha),
        "reticle-size-multiplier": toJson(reticleSizeMultiplier),
    })

    newConfigFileContent = CONFIG_TEMPLATE % tokens

    with open(configFilePath, "w") as configFile:
        configFile.write(newConfigFileContent)

    logger.info("Migration finished.")


def v2_6_0_addDrawCenterDotToSimpleServerReticle():
    configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

    if not os.path.isfile(configFilePath):
        return

    data = loadConfigDict(configFilePath)

    if data is None or "__version__" not in data or data["__version__"] != 4:
        return

    logger.info("Migrating config file from version 2.4.x ...")

    enabled = toBool(data["enabled"])
    dispersionReticleEnabled = toBool(data["dispersion-reticle"]["enabled"])

    latencyReticleEnabled = toBool(data["latency-reticle"]["enabled"])
    latencyReticleHideStandardReticle = toBool(data["latency-reticle"]["hide-standard-reticle"])

    serverReticleEnabled = toBool(data["server-reticle"]["enabled"])

    simpleServerReticleEnabled = toBool(data["simple-server-reticle"]["enabled"])
    simpleServerReticleShape = data["simple-server-reticle"]["shape"]
    simpleServerReticleColor = toColorTuple(data["simple-server-reticle"]["color"])
    simpleServerReticleDrawOutline = toBool(data["simple-server-reticle"]["draw-outline"])
    simpleServerReticleBlend = toPositiveFloat(data["simple-server-reticle"]["blend"])
    simpleServerReticleAlpha = toPositiveFloat(data["simple-server-reticle"]["alpha"])

    reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

    tokens = getDefaultConfigReplaceTokens()
    tokens.update({
        "enabled": toJson(enabled),
        "dispersion-reticle-enabled": toJson(dispersionReticleEnabled),
        "latency-reticle-enabled": toJson(latencyReticleEnabled),
        "latency-reticle-hide-standard-reticle": toJson(latencyReticleHideStandardReticle),
        "server-reticle-enabled": toJson(serverReticleEnabled),
        "simple-server-reticle-enabled": toJson(simpleServerReticleEnabled),
        "simple-server-reticle-color": toJson(simpleServerReticleColor),
        "simple-server-reticle-shape": toJson(simpleServerReticleShape),
        "simple-server-reticle-draw-outline": toJson(simpleServerReticleDrawOutline),
        "simple-server-reticle-blend": toJson(simpleServerReticleBlend),
        "simple-server-reticle-alpha": toJson(simpleServerReticleAlpha),
        "reticle-size-multiplier": toJson(reticleSizeMultiplier),
    })

    newConfigFileContent = CONFIG_TEMPLATE % tokens

    with open(configFilePath, "w") as configFile:
        configFile.write(newConfigFileContent)

    logger.info("Migration finished.")
