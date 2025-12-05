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

    # reticle size
    RETICLE_SIZE_LABEL = TranslationElement("reticleSize.label")

    RETICLE_SIZE_MULTIPLIER_HEADER = TranslationElement("reticleSize.multiplier.header")
    RETICLE_SIZE_MULTIPLIER_BODY = TranslationList("reticleSize.multiplier.body")
    RETICLE_SIZE_MULTIPLIER_NOTE = TranslationList("reticleSize.multiplier.note")

    RETICLE_SIZE_SCALE_ONLY_SERVER_RETICLES_HEADER = TranslationElement("reticleSize.scale-only-server-reticles.header")
    RETICLE_SIZE_SCALE_ONLY_SERVER_RETICLES_BODY = TranslationList("reticleSize.scale-only-server-reticles.body")
    RETICLE_SIZE_SCALE_ONLY_SERVER_RETICLES_NOTE = TranslationList("reticleSize.scale-only-server-reticles.note")

    # focused reticle
    FOCUSED_RETICLE_LABEL = TranslationElement("focusedReticle.label")
    FOCUSED_RETICLE_HEADER = TranslationElement("focusedReticle.header")
    FOCUSED_RETICLE_BODY = TranslationList("focusedReticle.body")
    FOCUSED_RETICLE_NOTE = TranslationList("focusedReticle.note")

    # focused reticle extended
    FOCUSED_RETICLE_EXTENDED_LABEL = TranslationElement("focusedReticleExtended.label")
    FOCUSED_RETICLE_EXTENDED_HEADER = TranslationElement("focusedReticleExtended.header")
    FOCUSED_RETICLE_EXTENDED_BODY = TranslationList("focusedReticleExtended.body")
    FOCUSED_RETICLE_EXTENDED_NOTE = TranslationList("focusedReticleExtended.note")
    FOCUSED_RETICLE_EXTENDED_ATTENTION = TranslationList("focusedReticleExtended.attention")

    # hybrid reticle
    HYBRID_RETICLE_LABEL = TranslationElement("hybridReticle.label")
    HYBRID_RETICLE_HEADER = TranslationElement("hybridReticle.header")
    HYBRID_RETICLE_BODY = TranslationList("hybridReticle.body")
    HYBRID_RETICLE_NOTE = TranslationList("hybridReticle.note")

    HYBRID_RETICLE_HIDE_STANDARD_RETICLE_HEADER = TranslationElement("hybridReticle.hideStandardReticle.header")
    HYBRID_RETICLE_HIDE_STANDARD_RETICLE_BODY = TranslationList("hybridReticle.hideStandardReticle.body")
    HYBRID_RETICLE_HIDE_STANDARD_RETICLE_NOTE = TranslationList("hybridReticle.hideStandardReticle.note")

    # hybrid reticle extended
    HYBRID_RETICLE_EXTENDED_LABEL = TranslationElement("hybridReticleExtended.label")
    HYBRID_RETICLE_EXTENDED_HEADER = TranslationElement("hybridReticleExtended.header")
    HYBRID_RETICLE_EXTENDED_BODY = TranslationList("hybridReticleExtended.body")
    HYBRID_RETICLE_EXTENDED_NOTE = TranslationList("hybridReticleExtended.note")
    HYBRID_RETICLE_EXTENDED_ATTENTION = TranslationList("hybridReticleExtended.attention")

    # server reticle
    SERVER_RETICLE_LABEL = TranslationElement("serverReticle.label")
    SERVER_RETICLE_HEADER = TranslationElement("serverReticle.header")
    SERVER_RETICLE_BODY = TranslationList("serverReticle.body")

    # server reticle extended
    SERVER_RETICLE_EXTENDED_LABEL = TranslationElement("serverReticleExtended.label")
    SERVER_RETICLE_EXTENDED_HEADER = TranslationElement("serverReticleExtended.header")
    SERVER_RETICLE_EXTENDED_BODY = TranslationList("serverReticleExtended.body")
    SERVER_RETICLE_EXTENDED_ATTENTION = TranslationList("serverReticleExtended.attention")

    # commons for reticles
    RETICLE_ENABLED_HEADER = TranslationElement("reticle.enabled.header")
    RETICLE_ENABLED_BODY = TranslationList("reticle.enabled.body")

    RETICLE_TYPE_HEADER = TranslationElement("reticle.type.header")
    RETICLE_TYPE_BODY = TranslationList("reticle.type.body")
    RETICLE_TYPE_NOTE = TranslationList("reticle.type.note")
    RETICLE_TYPE_ATTENTION = TranslationList("reticle.type.attention")
    RETICLE_TYPE_OPTION_DEFAULT = TranslationElement("reticle.type.option.default")
    RETICLE_TYPE_OPTION_PURPLE = TranslationElement("reticle.type.option.purple")

    # commons for extended reticle
    RETICLE_EXTENDED_SHAPE_HEADER = TranslationElement("reticleExtended.shape.header")
    RETICLE_EXTENDED_SHAPE_BODY = TranslationList("reticleExtended.shape.body")

    RETICLE_EXTENDED_SHAPE_OPTION_PENTAGON = TranslationElement("reticleExtended.shape.option.pentagon")
    RETICLE_EXTENDED_SHAPE_OPTION_T_SHAPE = TranslationElement("reticleExtended.shape.option.t-shape")
    RETICLE_EXTENDED_SHAPE_OPTION_CIRCLE = TranslationElement("reticleExtended.shape.option.circle")
    RETICLE_EXTENDED_SHAPE_OPTION_DASHED = TranslationElement("reticleExtended.shape.option.dashed")

    RETICLE_EXTENDED_COLOR_HEADER = TranslationElement("reticleExtended.color.header")
    RETICLE_EXTENDED_COLOR_BODY = TranslationList("reticleExtended.color.body")

    RETICLE_EXTENDED_CENTER_DOT_SIZE_HEADER = TranslationElement("reticleExtended.centerDotSize.header")
    RETICLE_EXTENDED_CENTER_DOT_SIZE_BODY = TranslationList("reticleExtended.centerDotSize.body")
    RETICLE_EXTENDED_CENTER_DOT_SIZE_NOTE = TranslationList("reticleExtended.centerDotSize.note")

    RETICLE_EXTENDED_DRAW_OUTLINE_HEADER = TranslationElement("reticleExtended.drawOutline.header")
    RETICLE_EXTENDED_DRAW_OUTLINE_BODY = TranslationList("reticleExtended.drawOutline.body")
    RETICLE_EXTENDED_DRAW_OUTLINE_NOTE = TranslationList("reticleExtended.drawOutline.note")

    RETICLE_EXTENDED_LAYER_HEADER = TranslationElement("reticleExtended.layer.header")
    RETICLE_EXTENDED_LAYER_BODY = TranslationList("reticleExtended.layer.body")

    RETICLE_EXTENDED_LAYER_OPTION_TOP = TranslationElement("reticleExtended.layer.option.top")
    RETICLE_EXTENDED_LAYER_OPTION_BOTTOM = TranslationElement("reticleExtended.layer.option.bottom")

    RETICLE_EXTENDED_BLEND_HEADER = TranslationElement("reticleExtended.blend.header")
    RETICLE_EXTENDED_BLEND_BODY = TranslationList("reticleExtended.blend.body")
    RETICLE_EXTENDED_BLEND_NOTE = TranslationList("reticleExtended.blend.note")
    RETICLE_EXTENDED_BLEND_ATTENTION = TranslationList("reticleExtended.blend.attention")

    RETICLE_EXTENDED_ALPHA_HEADER = TranslationElement("reticleExtended.alpha.header")
    RETICLE_EXTENDED_ALPHA_BODY = TranslationList("reticleExtended.alpha.body")
    RETICLE_EXTENDED_ALPHA_NOTE = TranslationList("reticleExtended.alpha.note")

    RETICLE_EXTENDED_SHAPES_HEADER = TranslationElement("reticleExtended.shapes.header")

    RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_HEADER = TranslationElement("reticleExtended.shapes.pentagon.width.header")
    RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_BODY = TranslationList("reticleExtended.shapes.pentagon.width.body")

    RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_HEADER = TranslationElement("reticleExtended.shapes.pentagon.height.header")
    RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_BODY = TranslationList("reticleExtended.shapes.pentagon.height.body")

    RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_HEADER = TranslationElement("reticleExtended.shapes.t-shape.thickness.header")
    RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_BODY = TranslationList("reticleExtended.shapes.t-shape.thickness.body")

    RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_HEADER = TranslationElement("reticleExtended.shapes.t-shape.length.header")
    RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_BODY = TranslationList("reticleExtended.shapes.t-shape.length.body")
    RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_NOTE = TranslationList("reticleExtended.shapes.t-shape.length.note")
