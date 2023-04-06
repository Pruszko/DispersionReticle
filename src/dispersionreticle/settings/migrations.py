import os
import logging

from dispersionreticle.settings import toJson, toBool, copy, deleteEmptyFolderSafely, loadConfigDict, toPositiveFloat

logger = logging.getLogger(__name__)


def performMigrationsIfNecessary():
    v2_0_2_migrateConfigFileLocation()
    v2_0_4_addOptionLatencyReticleHideStandardReticle()


V2_0_0_CONFIG_CONTENT = """{
    // Config can be reloaded in game using hotkeys: CTRL + P
    // To generate default config, delete this file and:
    // - either reload it with above hotkey
    // - or launch a game again

    // Dispersion reticle (enabled by default)
    // Valid values: true/false (default: true)
    //
    // Adds green reticle displaying fully-focused dispersion to vanilla reticle.
    // When both client-side and server-side reticle is on, it attaches to client-side reticle.

    "dispersion-reticle-enabled": %(dispersion-reticle-enabled)s,

    // Latency reticle
    // Valid values: true/false (default: false)
    // 
    // Adds green reticle displaying current server-side dispersion to client-side reticle.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    //
    // Useful if you want to know server-side dispersion, but still want client-side responsiveness.

    "latency-reticle-enabled": %(latency-reticle-enabled)s,

    // Server reticle
    // Valid values: true/false (default: false)
    // 
    // Adds purple server-side reticle alongside with client-side reticle.

    "server-reticle-enabled": %(server-reticle-enabled)s,

    // Fix reticle size
    // Valid values: any number > 0.0 (for default vanilla behavior: 1.0)
    //
    // Scales all reticles size by factor, except SPG top-view reticle.
    //
    // WG's displayed reticle dispersion is noticeably bigger than actual gun dispersion.
    // By this setting you can scale it to actual displayed dispersion.
    //
    // Good known values:
    // - 1.0    (default "wrong" WG dispersion)
    // - 0.6    (factor determined by me)
    // - 0.5848 (factor determined by Jak_Attackka, StranikS_Scan and others)

    "reticle-size-multiplier": %(reticle-size-multiplier)s
}"""


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


V2_0_4_CONFIG_CONTENT = """{
    // Config can be reloaded in game using hotkeys: CTRL + P
    // To generate default config, delete this file and:
    // - either reload it with above hotkey
    // - or launch a game again

    // Dispersion reticle (enabled by default)
    //
    // Adds reticle displaying fully-focused dispersion to standard reticle.
    // When both client-side and server-side reticle are on, it attaches to client-side reticle.

    "dispersion-reticle": {

        // Valid values: true/false (default: true)
        //
        // If true, displays this reticle.
        "enabled": %(dispersion-reticle-enabled)s
    },

    // Latency reticle
    // 
    // Adds reticle displaying current server-side dispersion to client-side reticle.
    // Basically, client-side position, but server-side dispersion.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    //
    // Useful if you want to know server-side dispersion, but still want client-side responsiveness.

    "latency-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(latency-reticle-enabled)s,
        
        // Valid values: true/false (default: false)
        //
        // If true, standard client reticle is hidden.
        // Useful if you want to only use latency reticle instead of standard reticle.
        "hide-standard-reticle": %(latency-reticle-hide-standard-reticle)s
    },

    // Server reticle
    // 
    // Adds server-side reticle alongside with client-side reticle.

    "server-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(server-reticle-enabled)s
    },

    // Reticle size
    // Valid values: any number > 0.0 (for default behavior: 1.0)
    //
    // Scales all reticles size by factor, except SPG top-view reticle.
    //
    // WG's displayed reticle dispersion is noticeably bigger than actual gun dispersion.
    // By this setting you can scale it to actual displayed dispersion.
    //
    // Good known values:
    // - 1.0    (default "wrong" WG dispersion)
    // - 0.6    (factor determined by me)
    // - 0.5848 (factor determined by Jak_Attackka, StranikS_Scan and others)

    "reticle-size-multiplier": %(reticle-size-multiplier)s,

    // DO NOT touch "__version__" field
    // It is used by me to seamlessly update config file :)
    "__version__": 1
}"""


def v2_0_4_addOptionLatencyReticleHideStandardReticle():
    configFilePath = os.path.join("mods", "configs", "DispersionReticle", "config.json")

    if not os.path.isfile(configFilePath):
        return

    data = loadConfigDict(configFilePath)

    if "__version__" in data:
        return

    logger.info("Migrating config file to version 2.0.4 ...")

    dispersionReticleEnabled = toBool(data["dispersion-reticle-enabled"])
    latencyReticleEnabled = toBool(data["latency-reticle-enabled"])
    serverReticleEnabled = toBool(data["server-reticle-enabled"])
    reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

    newConfigFileContent = V2_0_4_CONFIG_CONTENT % {
        "dispersion-reticle-enabled": toJson(dispersionReticleEnabled),
        "latency-reticle-enabled": toJson(latencyReticleEnabled),
        "latency-reticle-hide-standard-reticle": toJson(False),
        "server-reticle-enabled": toJson(serverReticleEnabled),
        "reticle-size-multiplier": toJson(reticleSizeMultiplier),
    }

    with open(configFilePath, "w") as configFile:
        configFile.write(newConfigFileContent)

    logger.info("Migration finished.")
