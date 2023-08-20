import logging

from dispersionreticle.settings import toJson, toColorTuple, toBool, clamp

PARAM_REGISTRY = {}

logger = logging.getLogger(__name__)


class Param(object):

    def __init__(self, path, defaultValue, disabledValue=None):
        self.name = path[-1]
        self.path = path
        self.tokenName = "-".join(self.path)

        self.value = defaultValue
        self.defaultValue = defaultValue
        self.disabledValue = disabledValue if disabledValue is not None else defaultValue

        PARAM_REGISTRY[self.tokenName] = self

    def readJsonValueFromConfigDictSafely(self, configDict):
        jsonValue = None
        prevConfigSection = configDict

        for pathSegment in self.path:
            if pathSegment not in prevConfigSection:
                return self.jsonValue

            dictSection = prevConfigSection[pathSegment]

            jsonValue = dictSection
            prevConfigSection = dictSection

        return jsonValue

    @property
    def jsonValue(self):
        return self.toJsonValue(self.value)

    @jsonValue.setter
    def jsonValue(self, jsonValue):
        try:
            self.value = self.fromJsonValue(jsonValue)
        except Exception as e:
            logger.warn("Error occurred while saving parameter %s with jsonValue %s, "
                        "fallback to previous valid value.",
                        self.tokenName, jsonValue, exc_info=e)

    @property
    def msaValue(self):
        return self.toMsaValue(self.value)

    @msaValue.setter
    def msaValue(self, msaValue):
        try:
            self.value = self.fromMsaValue(msaValue)
        except Exception as e:
            logger.warn("Error occurred while saving parameter %s with msaValue %s, "
                        "fallback to previous valid value.",
                        self.tokenName, msaValue, exc_info=e)

    @property
    def defaultMsaValue(self):
        return self.toMsaValue(self.defaultValue)

    @property
    def defaultJsonValue(self):
        return self.toJsonValue(self.defaultValue)

    def toMsaValue(self, value):
        raise NotImplementedError()

    def fromMsaValue(self, msaValue):
        raise NotImplementedError()

    def toJsonValue(self, value):
        raise NotImplementedError()

    def fromJsonValue(self, jsonValue):
        raise NotImplementedError()

    def renderParam(self, header, body=None, note=None, attention=None):
        raise NotImplementedError()

    def __repr__(self):
        return self.tokenName


class BooleanParam(Param):

    def __init__(self, path, defaultValue=None, disabledValue=None):
        super(BooleanParam, self).__init__(path, defaultValue, disabledValue)

    def toMsaValue(self, value):
        return value

    def fromMsaValue(self, msaValue):
        return msaValue

    def toJsonValue(self, value):
        return toJson(value)

    def fromJsonValue(self, jsonValue):
        return toBool(jsonValue)

    def renderParam(self, header, body=None, note=None, attention=None):
        return {
            "type": "CheckBox",
            "text": header,
            "varName": self.tokenName,
            "value": self.defaultMsaValue,
            "tooltip": createTooltip(
                header="%s (default: %s)" % (header, "checked" if self.defaultValue else "unchecked"),
                body=body,
                note=note,
                attention=attention
            )
        }


class FloatParam(Param):

    def __init__(self, path, minValue, step, maxValue, defaultValue, disabledValue=None):
        super(FloatParam, self).__init__(path, defaultValue, disabledValue)
        self.minValue = minValue
        self.step = step
        self.maxValue = maxValue

    def toMsaValue(self, value):
        return clamp(self.minValue, value, self.maxValue)

    def fromMsaValue(self, msaValue):
        return clamp(self.minValue, msaValue, self.maxValue)

    def toJsonValue(self, value):
        return toJson(clamp(self.minValue, value, self.maxValue))

    def fromJsonValue(self, jsonValue):
        value = float(jsonValue)
        return clamp(self.minValue, value, self.maxValue)

    def renderParam(self, header, body=None, note=None, attention=None):
        raise NotImplementedError()


class FloatTextParam(Param):

    def __init__(self, path, minValue, maxValue, defaultValue, disabledValue=None):
        super(FloatTextParam, self).__init__(path, defaultValue, disabledValue)
        self.minValue = minValue
        self.maxValue = maxValue

    def toMsaValue(self, value):
        return "%.4f" % (clamp(self.minValue, value, self.maxValue))

    def fromMsaValue(self, msaValue):
        floatValue = float(msaValue.replace(",", "."))
        return clamp(self.minValue, floatValue, self.maxValue)

    def toJsonValue(self, value):
        clampedValue = clamp(self.minValue, value, self.maxValue)
        return toJson(clampedValue)

    def fromJsonValue(self, jsonValue):
        rawValue = float(jsonValue)
        return clamp(self.minValue, rawValue, self.maxValue)

    def renderParam(self, header, body=None, note=None, attention=None):
        return {
            "type": "TextInput",
            "text": header,
            "varName": self.tokenName,
            "value": self.defaultMsaValue,
            "tooltip": createTooltip(
                header="%s (default: %s)" % (header, self.defaultMsaValue),
                body=body,
                note=note,
                attention=attention
            ),
            "width": 200
        }


# currently not used, because you can't manually input floating-point values
# it is only possible by up and down arrows, but using them with snapInterval 0.001 is an overkill
class FloatStepperParam(FloatParam):

    def __init__(self, path, minValue, step, maxValue, defaultValue, disabledValue=None):
        super(FloatStepperParam, self).__init__(path, minValue, step, maxValue, defaultValue, disabledValue)

    def renderParam(self, header, body=None, note=None, attention=None):
        return {
            "type": "NumericStepper",
            "text": header,
            "varName": self.tokenName,
            "value": self.defaultMsaValue,
            "minimum": self.minValue,
            "maximum": self.maxValue,
            "snapInterval": self.step,
            "tooltip": createTooltip(
                header="%s (default: %s)" % (header, self.defaultMsaValue),
                body=body,
                note=note,
                attention=attention
            )
        }


class FloatSliderParam(FloatParam):

    def __init__(self, path, minValue, step, maxValue, defaultValue, disabledValue=None):
        super(FloatSliderParam, self).__init__(path, minValue, step, maxValue, defaultValue, disabledValue)

    def renderParam(self, header, body=None, note=None, attention=None):
        return {
            "type": "Slider",
            "text": header,
            "varName": self.tokenName,
            "value": self.defaultMsaValue,
            "minimum": self.minValue,
            "maximum": self.maxValue,
            "snapInterval": self.step,
            "format": "{{value}}",
            "tooltip": createTooltip(
                header="%s (default: %s)" % (header, self.defaultMsaValue),
                body=body,
                note=note,
                attention=attention
            )
        }


class ColorParam(Param):

    def __init__(self, path, defaultValue=None, disabledValue=None):
        super(ColorParam, self).__init__(path, defaultValue, disabledValue)

    def toMsaValue(self, value):
        return self.__colorToHex(value)

    def fromMsaValue(self, msaValue):
        return self.__hexToColor(msaValue)

    def toJsonValue(self, value):
        return toJson(value)

    def fromJsonValue(self, jsonValue):
        return toColorTuple(jsonValue)

    def renderParam(self, header, body=None, note=None, attention=None):
        return {
            "type": "ColorChoice",
            "text": header,
            "varName": self.tokenName,
            "value": self.defaultMsaValue,
            "tooltip": createTooltip(
                header="%s (default: #%s)" % (header, self.defaultMsaValue),
                body=body,
                note=note,
                attention=attention
            )
        }

    def __hexToColor(self, hexColor):
        return tuple(int(hexColor[i:i + 2], 16) for i in (0, 2, 4))

    def __colorToHex(self, color):
        return ("%02x%02x%02x" % color).upper()


class Option(object):

    def __init__(self, value, msaValue, displayName):
        self.value = value
        self.msaValue = msaValue
        self.displayName = displayName


class OptionsParam(Param):

    def __init__(self, path, options, defaultValue, disabledValue=None):
        super(OptionsParam, self).__init__(path, defaultValue, disabledValue)
        self.options = options

    def toMsaValue(self, value):
        return self.getOptionByValue(value).msaValue

    def fromMsaValue(self, msaValue):
        return self.getOptionByMsaValue(msaValue).value

    def toJsonValue(self, value):
        return toJson(value)

    def fromJsonValue(self, jsonValue):
        option = self.getOptionByValue(jsonValue)
        if option is None:
            raise Exception("Invalid value %s for config param %s" % (jsonValue, self.tokenName))
        return option.value

    def getOptionByValue(self, value):
        foundOptions = filter(lambda option: option.value == value, self.options)
        return foundOptions[0] if len(foundOptions) > 0 else None

    def getOptionByMsaValue(self, msaValue):
        foundOptions = filter(lambda option: option.msaValue == msaValue, self.options)
        return foundOptions[0] if len(foundOptions) > 0 else None

    def renderParam(self, header, body=None, note=None, attention=None):
        return {
            "type": "Dropdown",
            "text": header,
            "varName": self.tokenName,
            "value": self.defaultMsaValue,
            "options": [
                {"label": option.displayName} for option in self.options
            ],
            "tooltip": createTooltip(
                header="%s (default: %s)" % (header, self.getOptionByValue(self.defaultValue).displayName),
                body=body,
                note=note,
                attention=attention
            ),
            "width": 200
        }


class ConfigParams(object):

    def __init__(self):
        self.__tokenNameRegistry = {}

        self.enabled = BooleanParam(
            ["enabled"],
            defaultValue=True, disabledValue=False
        )
        self.dispersionReticleEnabled = BooleanParam(
            ["dispersion-reticle", "enabled"],
            defaultValue=True, disabledValue=False
        )

        self.latencyReticleEnabled = BooleanParam(
            ["latency-reticle", "enabled"],
            defaultValue=False
        )
        self.latencyReticleHideStandardReticle = BooleanParam(
            ["latency-reticle", "hide-standard-reticle"],
            defaultValue=False
        )

        self.serverReticleEnabled = BooleanParam(
            ["server-reticle", "enabled"],
            defaultValue=False
        )

        self.simpleServerReticleEnabled = BooleanParam(
            ["simple-server-reticle", "enabled"],
            defaultValue=False
        )
        self.simpleServerReticleShape = OptionsParam(
            ["simple-server-reticle", "shape"],
            [
                Option("pentagon", 0, "Pentagon"),
                Option("t-shape", 1, "T-shape"),
                Option("circle", 2, "Circle"),
                Option("dashed", 3, "Dashed")
            ],
            defaultValue="pentagon"
        )
        self.simpleServerReticleColor = ColorParam(
            ["simple-server-reticle", "color"],
            defaultValue=(255, 0, 255)
        )
        self.simpleServerReticleDrawOutline = BooleanParam(
            ["simple-server-reticle", "draw-outline"],
            defaultValue=False
        )
        self.simpleServerReticleBlend = FloatSliderParam(
            ["simple-server-reticle", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.simpleServerReticleAlpha = FloatSliderParam(
            ["simple-server-reticle", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        self.reticleSizeMultiplier = FloatTextParam(
            ["reticle-size-multiplier"],
            minValue=0.0, maxValue=None,
            defaultValue=1.0
        )

    def items(self):
        return PARAM_REGISTRY.items()


# functions
def createTooltip(header=None, body=None, note=None, attention=None):
    res_str = ''
    if header is not None:
        res_str += '{HEADER}%s{/HEADER}' % header
    if body is not None:
        res_str += '{BODY}%s{/BODY}' % body
    if note is not None:
        res_str += '{NOTE}%s{/NOTE}' % note
    if attention is not None:
        res_str += '{ATTENTION}%s{/ATTENTION}' % attention
    return res_str


g_configParams = ConfigParams()
