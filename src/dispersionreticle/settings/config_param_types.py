import logging

from dispersionreticle.settings import toJson, toColorTuple, toBool, clamp
from dispersionreticle.settings.config_file import g_configFiles
from dispersionreticle.settings.translations import Tr

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

    def readValueFromConfigFile(self):
        return self.readValueFromConfigDict(g_configFiles.config.configDict)

    def readValueFromConfigDictSafely(self, configDict):
        value = self.readValueFromConfigDict(configDict)
        return value if value is not None else self.defaultValue

    def readValueFromConfigDict(self, configDict):
        readValue = None
        prevConfigSection = configDict

        for pathSegment in self.path:
            if pathSegment not in prevConfigSection:
                return None

            dictSection = prevConfigSection[pathSegment]

            readValue = dictSection
            prevConfigSection = dictSection

        return readValue

    def __call__(self):
        from dispersionreticle.settings.config_param import g_configParams

        if not g_configParams.enabled.value:
            return self.disabledValue
        return self.value

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
                header="%s (%s: %s)" % (header, Tr.DEFAULT_VALUE, Tr.CHECKED if self.defaultValue else Tr.UNCHECKED),
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
                header="%s (%s: %s)" % (header, Tr.DEFAULT_VALUE, self.defaultMsaValue),
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
                header="%s (%s: %s)" % (header, Tr.DEFAULT_VALUE, self.defaultMsaValue),
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
                header="%s (%s: %s)" % (header, Tr.DEFAULT_VALUE, self.defaultMsaValue),
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
                header="%s (%s: #%s)" % (header, Tr.DEFAULT_VALUE, self.defaultMsaValue),
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
                header="%s (%s: %s)" % (header, Tr.DEFAULT_VALUE, self.getOptionByValue(self.defaultValue).displayName),
                body=body,
                note=note,
                attention=attention
            ),
            "width": 200
        }


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
