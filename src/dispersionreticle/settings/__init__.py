import json
import logging
import os
import re

logger = logging.getLogger(__name__)


CONFIG_TEMPLATE = """{
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

    // Simple server reticle
    // 
    // Adds server-side reticle made of pentagons alongside with client-side reticle.
    // For SPG artillery view, it will implicitly enable "server-reticle" above instead of this reticle.

    "simple-server-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(simple-server-reticle-enabled)s,

        // Valid values: ["pentagon", "t-shape", "circle", "dashed"]
        // Default value: "pentagon"
        //
        // Shape which this reticle should have:
        // - "pentagon" - displays reticle made of pentagons,
        // - "t-shape"  - displays reticle made of T-shaped figures,
        // - "circle"   - displays reticle as a circle with 1 pixel thickness; similar to vanilla reticle,
        // - "dashed"   - displays reticle made of dash lines; similar to vanilla reticle.
        "shape": %(simple-server-reticle-shape)s,

        // Valid value: 3-element array of numbers between 0 and 255
        // Default value: [255, 0, 255] (this is purple color)
        //
        // Colors this reticle using red, green and blue components.
        // You can use color picker from internet to visually choose desired color.
        "color": %(simple-server-reticle-color)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with 1 pixel black outline.
        // Useful if shape color blends with the background.
        "draw-outline": %(simple-server-reticle-draw-outline)s,

        // Valid values: number between 0.0 and 1.0 (default 0.5)
        //
        // Controls, how much reticle color will blend with the background color instead of replacing it.
        // Vanilla "dashed" reticle uses this with value 1.0 without outline to make reticle look more natural.
        //
        // Set it to 1.0 if you want color to fully act as an addition to background color.
        // Set it to 0.0 if you want color to fully replace background color.
        // Values between them controls strength of those effects the closer it gets to them.
        //
        // Value 1.0 effectively prevents you from getting dark colors
        // because ... black color + background color = background color.
        "blend": %(simple-server-reticle-blend)s,

        // Valid values: number between 0.0 and 1.0 (default 1.0)
        //
        // Controls transparency of displayed reticle:
        // - value 1.0 means full visibility
        // - value 0.0 means zero visibility
        "alpha": %(simple-server-reticle-alpha)s
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
    "__version__": 3
}"""


def getDefaultConfigReplaceTokens():
    return {
        "dispersion-reticle-enabled": toJson(True),
        "latency-reticle-enabled": toJson(False),
        "latency-reticle-hide-standard-reticle": toJson(False),
        "server-reticle-enabled": toJson(False),
        "simple-server-reticle-enabled": toJson(False),
        "simple-server-reticle-shape": toJson("pentagon"),
        "simple-server-reticle-color": toJson([255, 0, 255]),
        "simple-server-reticle-draw-outline": toJson(False),
        "simple-server-reticle-blend": toJson(0.5),
        "simple-server-reticle-alpha": toJson(1.0),
        "reticle-size-multiplier": toJson(1.0),
    }


def getDefaultConfigContent():
    return CONFIG_TEMPLATE % getDefaultConfigReplaceTokens()


def loadConfigDict(configPath):
    with open(configPath, "r") as configFile:
        jsonRawData = configFile.read()

    jsonData = re.sub(r"^\s*//.*$", "", jsonRawData, flags=re.MULTILINE)
    return json.loads(jsonData, encoding="UTF-8")


def toJson(obj):
    return json.dumps(obj, encoding="UTF-8")


def toBool(value):
    return str(value).lower() == "true"


def toPositiveFloat(value):
    floatValue = float(value)
    return floatValue if floatValue > 0.0 else 0.0


def clamp(minValue, value, maxValue):
    return min(max(minValue, value), maxValue)


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
