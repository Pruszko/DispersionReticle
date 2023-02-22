import json
import logging
import os
import re

import Event
import Keys
import game

from dispersionreticle.utils import *

DEFAULT_CONFIG_CONTENT = """{
    // Config can be reloaded in game using hotkeys: CTRL + P
    
    // Valid values: true/false (default: true)
    // 
    // Adds green fully-focused dispersion reticle to vanilla reticle.
    // 
    // When used together with "server-reticle-enabled" or "latency-reticle-enabled", it
    // attaches dispersion reticle to client reticle
    "dispersion-reticle-enabled": true,
    
    // Valid values: true/false (default: false)
    // 
    // Adds green latency reticle to client reticle.
    // Basically, attaches additional green server reticle to client reticle position.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    // 
    // IMPORTANT:
    // To enable latency reticle, you MUST also check "Use server aim" in game settings.
    "latency-reticle-enabled": false,
    
    // Valid values: true/false (default: false)
    // 
    // Separates client reticle and server reticle from vanilla reticle.
    // By this, client reticle is always displayed and additional purple server reticle
    // can be displayed with checked "Use server aim" in game settings.
    // 
    // IMPORTANT:
    // To enable server reticle, you MUST also check "Use server aim" in game settings.
    "server-reticle-enabled": false,
    
    // Valid values: any number > 0.0 (for default vanilla behavior: 1.0)
    //
    // Scales all reticles size by below factor.
    // WG's displayed reticle dispersion is noticeably bigger than actual gun dispersion, so
    // by this setting you can scale it to actual displayed dispersion.
    //
    // Good known values:
    // - 1.0    (default "wrong" WG dispersion)
    // - 0.6    (factor determined by me)
    // - 0.5848 (factor determined by Jak_Attackka, StranikS_Scan and others)
    "reticle-size-multiplier": 1.0
}"""

logger = logging.getLogger(__name__)


class Config:

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
