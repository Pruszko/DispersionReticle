import json
import logging
import os
import re

import Event
import Keys
import game
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

from dispersionreticle.utils import *

DEFAULT_CONFIG_CONTENT = """{
    // Config can be reloaded in game using hotkeys: CTRL + P
    // To generate default config, delete this file and:
    // - either reload it with above hotkey
    // - or launch a game again
    
    // Dispersion reticle (enabled by default)
    // Valid values: true/false (default: true)
    //
    // Adds green reticle displaying fully-focused dispersion to vanilla reticle.
    // When both client-side and server-side reticle is on, it attaches to client-side reticle.
    
    "dispersion-reticle-enabled": true,
    
    // Latency reticle
    // Valid values: true/false (default: false)
    // 
    // Adds green reticle displaying current server-side dispersion to client-side reticle.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    
    "latency-reticle-enabled": false,
    
    // Server reticle
    // Valid values: true/false (default: false)
    // 
    // Adds purple server-side reticle alongside with client-side reticle.
    
    "server-reticle-enabled": false,
    
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
    
    "reticle-size-multiplier": 1.0
}"""

logger = logging.getLogger(__name__)


class Config:

    settingsCore = dependency.descriptor(ISettingsCore)

    def __init__(self):
        self.__configFileDir = os.path.join("mods", "config", "DispersionReticle")
        self.__configFilePath = os.path.join("mods", "config", "DispersionReticle", "config.json")

        self.__dispersionReticleEnabled = True
        self.__latencyReticleEnabled = False
        self.__serverReticleEnabled = False
        self.__reticleSizeMultiplier = 1.0

        self.__eventManager = Event.EventManager()
        self.onConfigReload = Event.Event(self.__eventManager)

    def loadConfigSafely(self):
        try:
            logger.info("Starting config loading ...")
            self.createConfigIfNotExists()

            with open(self.__configFilePath, "r") as configFile:
                jsonRawData = configFile.read()

            jsonData = re.sub(r"^\s*//.*$", "", jsonRawData, flags=re.MULTILINE)
            data = json.loads(jsonData, encoding="UTF-8")

            dispersionReticleEnabled = toBool(data["dispersion-reticle-enabled"])
            latencyReticleEnabled = toBool(data["latency-reticle-enabled"])
            serverReticleEnabled = toBool(data["server-reticle-enabled"])
            reticleSizeMultiplier = toPositiveFloat(data["reticle-size-multiplier"])

            self.__dispersionReticleEnabled = dispersionReticleEnabled
            self.__latencyReticleEnabled = latencyReticleEnabled
            self.__serverReticleEnabled = serverReticleEnabled
            self.__reticleSizeMultiplier = reticleSizeMultiplier

            logger.info("Loaded dispersion-reticle-enabled: %s", dispersionReticleEnabled)
            logger.info("Loaded    latency-reticle-enabled: %s", latencyReticleEnabled)
            logger.info("Loaded     server-reticle-enabled: %s", serverReticleEnabled)
            logger.info("Loaded    reticle-size-multiplier: %s", reticleSizeMultiplier)
            logger.info("Finished config loading.")
        except Exception as e:
            logger.error("Failed to load config", exc_info=e)

    def createConfigIfNotExists(self):
        try:
            logger.info("Checking config existence ...")
            if os.path.isfile(self.__configFilePath):
                logger.info("Config already exists.")
                return

            logger.info("Creating config directory ...")
            os.makedirs(self.__configFileDir)

            logger.info("Creating config file ...")
            with open(self.__configFilePath, "w") as configFile:
                configFile.write(DEFAULT_CONFIG_CONTENT)
        except Exception as e:
            logger.error("Failed to save default config", exc_info=e)

    def isDispersionReticleEnabled(self):
        return self.__dispersionReticleEnabled

    def isLatencyReticleEnabled(self):
        return self.__latencyReticleEnabled

    def isServerReticleEnabled(self):
        return self.__serverReticleEnabled

    def getReticleSizeMultiplier(self):
        return self.__reticleSizeMultiplier

    def isServerAimRequired(self):
        return self.__latencyReticleEnabled or self.__serverReticleEnabled

    def isServerAimEnabled(self):
        return self.settingsCore.getSetting('useServerAim')


g_config = Config()


def toBool(value):
    return str(value).lower() == "true"


def toPositiveFloat(value):
    try:
        floatValue = float(value)
        return floatValue if floatValue > 0.0 else 0.0
    except ValueError as e:
        logger.error("Failed to convert value %s to float", value, exc_info=e)
        return 1.0


@overrideIn(game)
def handleKeyEvent(func, event):
    if event.isKeyDown() and event.isCtrlDown():
        if event.key == Keys.KEY_P:
            g_config.loadConfigSafely()
            g_config.onConfigReload()

    return func(event)
