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
    INTRO_LABEL = TranslationElement("intro.label")
    INTRO_HEADER = TranslationElement("intro.header")
    INTRO_BODY = TranslationList("intro.body")
    INTRO_NOTE = TranslationList("intro.note")
    INTRO_ATTENTION = TranslationList("intro.attention")

    # dispersion reticle
    STANDARD_FOCUSED_RETICLE_LABEL = TranslationElement("standardFocusedReticle.label")
    STANDARD_FOCUSED_RETICLE_HEADER = TranslationElement("standardFocusedReticle.header")
    STANDARD_FOCUSED_RETICLE_BODY = TranslationList("standardFocusedReticle.body")
    STANDARD_FOCUSED_RETICLE_NOTE = TranslationList("standardFocusedReticle.note")

    STANDARD_FOCUSED_RETICLE_ENABLED_HEADER = TranslationElement("standardFocusedReticle.enabled.header")
    STANDARD_FOCUSED_RETICLE_ENABLED_BODY = TranslationList("standardFocusedReticle.enabled.body")

    # latency reticle
    STANDARD_HYBRID_RETICLE_LABEL = TranslationElement("standardHybridReticle.label")
    STANDARD_HYBRID_RETICLE_HEADER = TranslationElement("standardHybridReticle.header")
    STANDARD_HYBRID_RETICLE_BODY = TranslationList("standardHybridReticle.body")
    STANDARD_HYBRID_RETICLE_NOTE = TranslationList("standardHybridReticle.note")

    STANDARD_HYBRID_RETICLE_ENABLED_HEADER = TranslationElement("standardHybridReticle.enabled.header")
    STANDARD_HYBRID_RETICLE_ENABLED_BODY = TranslationList("standardHybridReticle.enabled.body")

    STANDARD_HYBRID_RETICLE_HIDE_STANDARD_RETICLE_HEADER = TranslationElement("standardHybridReticle.hideStandardReticle.header")
    STANDARD_HYBRID_RETICLE_HIDE_STANDARD_RETICLE_BODY = TranslationList("standardHybridReticle.hideStandardReticle.body")
    STANDARD_HYBRID_RETICLE_HIDE_STANDARD_RETICLE_NOTE = TranslationList("standardHybridReticle.hideStandardReticle.note")

    # server reticle
    STANDARD_SERVER_RETICLE_LABEL = TranslationElement("standardServerReticle.label")
    STANDARD_SERVER_RETICLE_HEADER = TranslationElement("standardServerReticle.header")
    STANDARD_SERVER_RETICLE_BODY = TranslationList("standardServerReticle.body")

    STANDARD_SERVER_RETICLE_ENABLED_HEADER = TranslationElement("standardServerReticle.enabled.header")
    STANDARD_SERVER_RETICLE_ENABLED_BODY = TranslationList("standardServerReticle.enabled.body")

    # simple server reticle
    CUSTOM_SERVER_RETICLE_LABEL = TranslationElement("customServerReticle.label")
    CUSTOM_SERVER_RETICLE_HEADER = TranslationElement("customServerReticle.header")
    CUSTOM_SERVER_RETICLE_BODY = TranslationList("customServerReticle.body")
    CUSTOM_SERVER_RETICLE_ATTENTION = TranslationList("customServerReticle.attention")

    CUSTOM_SERVER_RETICLE_ENABLED_HEADER = TranslationElement("customServerReticle.enabled.header")
    CUSTOM_SERVER_RETICLE_ENABLED_BODY = TranslationList("customServerReticle.enabled.body")

    CUSTOM_SERVER_RETICLE_SHAPE_HEADER = TranslationElement("customServerReticle.shape.header")
    CUSTOM_SERVER_RETICLE_SHAPE_BODY = TranslationList("customServerReticle.shape.body")

    CUSTOM_SERVER_RETICLE_SHAPE_OPTION_PENTAGON = TranslationElement("customServerReticle.shape.option.pentagon")
    CUSTOM_SERVER_RETICLE_SHAPE_OPTION_T_SHAPE = TranslationElement("customServerReticle.shape.option.t-shape")
    CUSTOM_SERVER_RETICLE_SHAPE_OPTION_CIRCLE = TranslationElement("customServerReticle.shape.option.circle")
    CUSTOM_SERVER_RETICLE_SHAPE_OPTION_DASHED = TranslationElement("customServerReticle.shape.option.dashed")

    CUSTOM_SERVER_RETICLE_COLOR_HEADER = TranslationElement("customServerReticle.color.header")
    CUSTOM_SERVER_RETICLE_COLOR_BODY = TranslationList("customServerReticle.color.body")

    CUSTOM_SERVER_RETICLE_DRAW_CENTER_DOT_HEADER = TranslationElement("customServerReticle.drawCenterDot.header")
    CUSTOM_SERVER_RETICLE_DRAW_CENTER_DOT_BODY = TranslationList("customServerReticle.drawCenterDot.body")

    CUSTOM_SERVER_RETICLE_DRAW_OUTLINE_HEADER = TranslationElement("customServerReticle.drawOutline.header")
    CUSTOM_SERVER_RETICLE_DRAW_OUTLINE_BODY = TranslationList("customServerReticle.drawOutline.body")
    CUSTOM_SERVER_RETICLE_DRAW_OUTLINE_NOTE = TranslationList("customServerReticle.drawOutline.note")

    CUSTOM_SERVER_RETICLE_BLEND_HEADER = TranslationElement("customServerReticle.blend.header")
    CUSTOM_SERVER_RETICLE_BLEND_BODY = TranslationList("customServerReticle.blend.body")
    CUSTOM_SERVER_RETICLE_BLEND_NOTE = TranslationList("customServerReticle.blend.note")
    CUSTOM_SERVER_RETICLE_BLEND_ATTENTION = TranslationList("customServerReticle.blend.attention")

    CUSTOM_SERVER_RETICLE_ALPHA_HEADER = TranslationElement("customServerReticle.alpha.header")
    CUSTOM_SERVER_RETICLE_ALPHA_BODY = TranslationList("customServerReticle.alpha.body")
    CUSTOM_SERVER_RETICLE_ALPHA_NOTE = TranslationList("customServerReticle.alpha.note")

    # reticle size multiplier
    RETICLE_SIZE_MULTIPLIER_HEADER = TranslationElement("reticleSizeMultiplier.header")
    RETICLE_SIZE_MULTIPLIER_BODY = TranslationList("reticleSizeMultiplier.body")
    RETICLE_SIZE_MULTIPLIER_NOTE = TranslationList("reticleSizeMultiplier.note")
