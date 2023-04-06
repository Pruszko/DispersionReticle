import json
import logging
import os
import re

logger = logging.getLogger(__name__)


def getDefaultConfigContent():
    from dispersionreticle.settings.migrations import V2_0_4_CONFIG_CONTENT
    return V2_0_4_CONFIG_CONTENT % {
        "dispersion-reticle-enabled": toJson(True),
        "latency-reticle-enabled": toJson(False),
        "latency-reticle-hide-standard-reticle": toJson(False),
        "server-reticle-enabled": toJson(False),
        "reticle-size-multiplier": toJson(1.0),
    }


def loadConfigDict(configPath):
    with open(configPath, "r") as configFile:
        jsonRawData = configFile.read()

    jsonData = re.sub(r"^\s*//.*$", "", jsonRawData, flags=re.MULTILINE)
    return json.loads(jsonData, encoding="UTF-8")


def toBool(value):
    return str(value).lower() == "true"


def toPositiveFloat(value):
    floatValue = float(value)
    return floatValue if floatValue > 0.0 else 0.0


def clampFloat(minValue, value, maxValue):
    return min(max(minValue, value), maxValue)


def toColorTuple(value):
    if len(value) != 3:
        raise Exception("Provided color array does not have exactly 3 elements.")
    rawRed = float(value[0])
    rawGreen = float(value[1])
    rawBlue = float(value[2])
    red = clampFloat(0.0, rawRed, 255.0)
    green = clampFloat(0.0, rawGreen, 255.0)
    blue = clampFloat(0.0, rawBlue, 255.0)
    return red, green, blue


def toJson(obj):
    return json.dumps(obj, encoding="UTF-8")


def copy(oldPath, newPath):
    with open(oldPath, "r") as oldFile:
        oldRawData = oldFile.read()
        with open(newPath, "w") as newFile:
            newFile.write(oldRawData)


def createFolderSafely(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def deleteEmptyFolderSafely(path):
    try:
        os.rmdir(path)
    except OSError:
        pass
