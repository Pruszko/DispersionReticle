import json
import logging
import os

logger = logging.getLogger(__name__)


class ConfigException(Exception):
    pass


def getDefaultConfigTokens():
    from dispersionreticle.settings.config_param import g_configParams

    return {
        tokenName: param.defaultJsonValue for tokenName, param in g_configParams.items()
    }


def toJson(obj):
    return json.dumps(obj, encoding="UTF-8")


def toBool(value):
    return str(value).lower() == "true"


def toPositiveFloat(value):
    floatValue = float(value)
    return floatValue if floatValue > 0.0 else 0.0


def clamp(minValue, value, maxValue):
    if minValue is not None:
        value = max(minValue, value)
    if maxValue is not None:
        value = min(value, maxValue)
    return value


def toColorTuple(value):
    if len(value) != 3:
        raise Exception("Provided color array does not have exactly 3 elements.")
    rawRed = int(value[0])
    rawGreen = int(value[1])
    rawBlue = int(value[2])
    red = clamp(0, rawRed, 255)
    green = clamp(0, rawGreen, 255)
    blue = clamp(0, rawBlue, 255)
    return red, green, blue


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
