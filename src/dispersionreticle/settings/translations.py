import json
import logging

import ResMgr
from helpers import getClientLanguage


# Thanks to:
# - shuxue - for Russian translations
# - yinx2002 - for Chinese translations


logger = logging.getLogger(__name__)

# if this is set to some language code, then below code will treat game language as that
# used only for debugging
#
# TODO
# On EU clients, using "zh_cn" language code crashes on glyph lookup in AS3
# resulting in "squares" instead of glyph.
#
# Most likely because EU client doesn't have font with Chinese glyphs
# CN clients probably have them, I hope it works there, lol
DEBUG_LANGUAGE = None


DEFAULT_TRANSLATIONS_MAP = {}
TRANSLATIONS_MAP = {}


def loadTranslations():
    defaultTranslationsMap = _loadLanguage("en")

    global DEFAULT_TRANSLATIONS_MAP
    DEFAULT_TRANSLATIONS_MAP = defaultTranslationsMap if defaultTranslationsMap is not None else {}

    if DEBUG_LANGUAGE is not None:
        language = DEBUG_LANGUAGE
        logger.info("Client language (debug): %s", language)
    else:
        language = getClientLanguage()
        logger.info("Client language: %s", language)

    translationsMap = _loadLanguage(language)

    if translationsMap is not None:
        logger.info("Translations for language %s detected" % language)
        global TRANSLATIONS_MAP
        TRANSLATIONS_MAP = translationsMap
    else:
        logger.info("Translations for language %s not present, fallback to en" % language)


def _loadLanguage(language):
    translationsRes = ResMgr.openSection("gui/dispersionreticle/translations/translations_%s.json" % language)
    if translationsRes is None:
        return None

    translationsStr = str(translationsRes.asBinary)
    return json.loads(translationsStr, encoding="UTF-8")


class TranslationBase(object):

    def __init__(self, tokenName):
        self._tokenName = tokenName
        self._value = None

    def __get__(self, instance, owner=None):
        if self._value is None:
            self._value = self._generateTranslation()
        return self._value

    def _generateTranslation(self):
        raise NotImplementedError()


class TranslationElement(TranslationBase):

    def _generateTranslation(self):
        global TRANSLATIONS_MAP
        if self._tokenName in TRANSLATIONS_MAP:
            return TRANSLATIONS_MAP[self._tokenName]

        global DEFAULT_TRANSLATIONS_MAP
        return DEFAULT_TRANSLATIONS_MAP[self._tokenName]


class TranslationList(TranslationBase):

    def _generateTranslation(self):
        global TRANSLATIONS_MAP
        if self._tokenName in TRANSLATIONS_MAP:
            return "".join(TRANSLATIONS_MAP[self._tokenName])

        global DEFAULT_TRANSLATIONS_MAP
        return "".join(DEFAULT_TRANSLATIONS_MAP[self._tokenName])


class Tr(object):
    # common
    MODNAME = TranslationElement("modname")
    CHECKED = TranslationElement("checked")
    UNCHECKED = TranslationElement("unchecked")
    DEFAULT_VALUE = TranslationElement("defaultValue")

    # intro
    INTRO_PART_LABEL = TranslationElement("introPart.label")
    INTRO_PART_HEADER = TranslationElement("introPart.header")
    INTRO_PART_BODY = TranslationList("introPart.body")
    INTRO_PART_NOTE = TranslationList("introPart.note")
    INTRO_PART_ATTENTION = TranslationList("introPart.attention")

    # dispersion reticle
    DISPERSION_RETICLE_PART_LABEL = TranslationElement("dispersionReticlePart.label")
    DISPERSION_RETICLE_PART_HEADER = TranslationElement("dispersionReticlePart.header")
    DISPERSION_RETICLE_PART_BODY = TranslationList("dispersionReticlePart.body")
    DISPERSION_RETICLE_PART_NOTE = TranslationList("dispersionReticlePart.note")

    DISPERSION_RETICLE_PART_ENABLED_HEADER = TranslationElement("dispersionReticlePart.enabled.header")
    DISPERSION_RETICLE_PART_ENABLED_BODY = TranslationList("dispersionReticlePart.enabled.body")

    # latency reticle
    LATENCY_RETICLE_PART_LABEL = TranslationElement("latencyReticlePart.label")
    LATENCY_RETICLE_PART_HEADER = TranslationElement("latencyReticlePart.header")
    LATENCY_RETICLE_PART_BODY = TranslationList("latencyReticlePart.body")
    LATENCY_RETICLE_PART_NOTE = TranslationList("latencyReticlePart.note")

    LATENCY_RETICLE_PART_ENABLED_HEADER = TranslationElement("latencyReticlePart.enabled.header")
    LATENCY_RETICLE_PART_ENABLED_BODY = TranslationList("latencyReticlePart.enabled.body")

    LATENCY_RETICLE_PART_HIDE_STANDARD_RETICLE_HEADER = TranslationElement("latencyReticlePart.hideStandardReticle.header")
    LATENCY_RETICLE_PART_HIDE_STANDARD_RETICLE_BODY = TranslationList("latencyReticlePart.hideStandardReticle.body")
    LATENCY_RETICLE_PART_HIDE_STANDARD_RETICLE_NOTE = TranslationList("latencyReticlePart.hideStandardReticle.note")

    # server reticle
    SERVER_RETICLE_PART_LABEL = TranslationElement("serverReticlePart.label")
    SERVER_RETICLE_PART_HEADER = TranslationElement("serverReticlePart.header")
    SERVER_RETICLE_PART_BODY = TranslationList("serverReticlePart.body")

    SERVER_RETICLE_PART_ENABLED_HEADER = TranslationElement("serverReticlePart.enabled.header")
    SERVER_RETICLE_PART_ENABLED_BODY = TranslationList("serverReticlePart.enabled.body")

    # simple server reticle
    SIMPLE_SERVER_RETICLE_PART_LABEL = TranslationElement("simpleServerReticlePart.label")
    SIMPLE_SERVER_RETICLE_PART_HEADER = TranslationElement("simpleServerReticlePart.header")
    SIMPLE_SERVER_RETICLE_PART_BODY = TranslationList("simpleServerReticlePart.body")
    SIMPLE_SERVER_RETICLE_PART_ATTENTION = TranslationList("simpleServerReticlePart.attention")

    SIMPLE_SERVER_RETICLE_PART_ENABLED_HEADER = TranslationElement("simpleServerReticlePart.enabled.header")
    SIMPLE_SERVER_RETICLE_PART_ENABLED_BODY = TranslationList("simpleServerReticlePart.enabled.body")

    SIMPLE_SERVER_RETICLE_PART_SHAPE_HEADER = TranslationElement("simpleServerReticlePart.shape.header")
    SIMPLE_SERVER_RETICLE_PART_SHAPE_BODY = TranslationList("simpleServerReticlePart.shape.body")

    SIMPLE_SERVER_RETICLE_PART_SHAPE_OPTION_PENTAGON = TranslationElement("simpleServerReticlePart.shape.option.pentagon")
    SIMPLE_SERVER_RETICLE_PART_SHAPE_OPTION_T_SHAPE = TranslationElement("simpleServerReticlePart.shape.option.t-shape")
    SIMPLE_SERVER_RETICLE_PART_SHAPE_OPTION_CIRCLE = TranslationElement("simpleServerReticlePart.shape.option.circle")
    SIMPLE_SERVER_RETICLE_PART_SHAPE_OPTION_DASHED = TranslationElement("simpleServerReticlePart.shape.option.dashed")

    SIMPLE_SERVER_RETICLE_PART_COLOR_HEADER = TranslationElement("simpleServerReticlePart.color.header")
    SIMPLE_SERVER_RETICLE_PART_COLOR_BODY = TranslationList("simpleServerReticlePart.color.body")

    SIMPLE_SERVER_RETICLE_PART_DRAW_CENTER_DOT_HEADER = TranslationElement("simpleServerReticlePart.drawCenterDot.header")
    SIMPLE_SERVER_RETICLE_PART_DRAW_CENTER_DOT_BODY = TranslationList("simpleServerReticlePart.drawCenterDot.body")

    SIMPLE_SERVER_RETICLE_PART_DRAW_OUTLINE_HEADER = TranslationElement("simpleServerReticlePart.drawOutline.header")
    SIMPLE_SERVER_RETICLE_PART_DRAW_OUTLINE_BODY = TranslationList("simpleServerReticlePart.drawOutline.body")
    SIMPLE_SERVER_RETICLE_PART_DRAW_OUTLINE_NOTE = TranslationList("simpleServerReticlePart.drawOutline.note")

    SIMPLE_SERVER_RETICLE_PART_BLEND_HEADER = TranslationElement("simpleServerReticlePart.blend.header")
    SIMPLE_SERVER_RETICLE_PART_BLEND_BODY = TranslationList("simpleServerReticlePart.blend.body")
    SIMPLE_SERVER_RETICLE_PART_BLEND_NOTE = TranslationList("simpleServerReticlePart.blend.note")
    SIMPLE_SERVER_RETICLE_PART_BLEND_ATTENTION = TranslationList("simpleServerReticlePart.blend.attention")

    SIMPLE_SERVER_RETICLE_PART_ALPHA_HEADER = TranslationElement("simpleServerReticlePart.alpha.header")
    SIMPLE_SERVER_RETICLE_PART_ALPHA_BODY = TranslationList("simpleServerReticlePart.alpha.body")
    SIMPLE_SERVER_RETICLE_PART_ALPHA_NOTE = TranslationList("simpleServerReticlePart.alpha.note")

    # reticle size multiplier
    RETICLE_SIZE_MULTIPLIER_PART_HEADER = TranslationElement("reticleSizeMultiplier.header")
    RETICLE_SIZE_MULTIPLIER_PART_BODY = TranslationList("reticleSizeMultiplier.body")
    RETICLE_SIZE_MULTIPLIER_PART_NOTE = TranslationList("reticleSizeMultiplier.note")
