import logging

from dispersionreticle.settings.translations import Tr
from dispersionreticle.settings.config import g_config
from dispersionreticle.settings.config_param import g_configParams, createTooltip
from dispersionreticle.utils import ObservingSemaphore

from gui.modsSettingsApi import g_modsSettingsApi


logger = logging.getLogger(__name__)

modLinkage = "com.github.pruszko.dispersionreticle"


def registerSoftDependencySupport():
    template = {
        "modDisplayName": Tr.MODNAME,
        "enabled": g_configParams.enabled.defaultMsaValue,
        "column1":
            _createIntroPart() +
            _emptyLine(9) +
            _endSection() +
            _createFocusedReticle() +
            _innerSectionSeparator() +
            _createFocusedReticleExtended() +
            _endSection() +
            _createHybridReticle() +
            _innerSectionSeparator() +
            _createHybridReticleExtended(),
        "column2":
            _createReticleSize() +
            _endSection() +
            _createServerReticle() +
            _innerSectionSeparator() +
            _createServerReticleExtended() +
            _endSection()
    }

    # we purposely ignore ModsSettingsAPI capability of saving mod configuration
    # due to config file being "master" configuration
    #
    # also, I don't like going against "standard setup" of ModsSettingsAPI support, but
    # we still treat it only as a GUI, not a configuration framework
    #
    # so we also purposely always call setModTemplate instead of registerCallback
    # to keep always updated GUI template
    g_modsSettingsApi.setModTemplate(modLinkage, template, onModSettingsChanged)


# we cannot update ModsSettingsAPI settings without triggering onModSettingsChanged callback,
# so we will use "semaphore" to control when we want to ignore it
settingsChangedSemaphore = ObservingSemaphore()


# this is called only on manual config reload
def onConfigFileReload():
    msaSettings = {}

    for tokenName, param in g_configParams.items():
        msaSettings[tokenName] = param.msaValue

    logger.info("Synchronizing config file -> ModsSettingsAPI")
    g_modsSettingsApi.updateModSettings(modLinkage, newSettings=msaSettings)


@settingsChangedSemaphore.withIgnoringLock(returnForIgnored=None)
def onModSettingsChanged(linkage, newSettings):
    if linkage != modLinkage:
        return

    try:
        serializedSettings = {}
        for tokenName, param in g_configParams.items():
            if tokenName not in newSettings:
                continue

            value = param.fromMsaValue(newSettings[tokenName])
            jsonValue = param.toJsonValue(value)

            serializedSettings[param.tokenName] = jsonValue

        logger.info("Synchronizing ModsSettingsAPI -> config file")
        g_config.updateConfigSafely(serializedSettings)
    except Exception:
        logger.error("Error occurred while ModsSettingsAPI settings change.", exc_info=True)


def _endSection():
    return _emptyLine() + _horizontalLine()


def _innerSectionSeparator():
    return _emptyLine(4)


def _emptyLine(count=1):
    return [
        {
            "type": "Empty"
        }
    ] * count


def _horizontalLine():
    return [
        {
            "type": "Label",
            "text": "________________________________________"
        }
    ]


def _createIntroPart():
    return [
        {
            "type": "Label",
            "text": Tr.INTRO_LABEL,
            "tooltip": createTooltip(
                header=Tr.INTRO_HEADER,
                body=Tr.INTRO_BODY + "\n",
                note=Tr.INTRO_NOTE + "\n",
                attention=Tr.INTRO_ATTENTION
            )
        }
    ]


def _createReticleSize():
    return [
        {
            "type": "Label",
            "text": Tr.RETICLE_SIZE_LABEL
        },
        g_configParams.reticleSizeMultiplier.renderParam(
            header=Tr.RETICLE_SIZE_MULTIPLIER_HEADER,
            body=Tr.RETICLE_SIZE_MULTIPLIER_BODY + "\n",
            note=Tr.RETICLE_SIZE_MULTIPLIER_NOTE
        ),
        g_configParams.reticleSizeScaleOnlyServerReticles.renderParam(
            header=Tr.RETICLE_SIZE_SCALE_ONLY_SERVER_RETICLES_HEADER,
            body=Tr.RETICLE_SIZE_SCALE_ONLY_SERVER_RETICLES_BODY + "\n",
            note=Tr.RETICLE_SIZE_SCALE_ONLY_SERVER_RETICLES_NOTE
        )
    ]


def _createFocusedReticle():
    return [
        {
            "type": "Label",
            "text": Tr.FOCUSED_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="1. " + Tr.FOCUSED_RETICLE_HEADER,
                body=Tr.FOCUSED_RETICLE_BODY + "\n",
                note=Tr.FOCUSED_RETICLE_NOTE + "\n\n" + _createImg(src="imgs/all.jpg", width=427, height=324)
            ),
        },
        g_configParams.focusedReticleEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.focusedReticleType.renderParam(
            header=Tr.RETICLE_TYPE_HEADER,
            body=Tr.RETICLE_TYPE_BODY + "\n",
            note=Tr.RETICLE_TYPE_NOTE + "\n",
            attention=Tr.RETICLE_TYPE_ATTENTION
        )
    ]


def _createFocusedReticleExtended():
    return [
        {
            "type": "Label",
            "text": Tr.FOCUSED_RETICLE_EXTENDED_LABEL,
            "tooltip": createTooltip(
                header="1. " + Tr.FOCUSED_RETICLE_EXTENDED_HEADER,
                body=Tr.FOCUSED_RETICLE_EXTENDED_BODY + "\n",
                note=Tr.FOCUSED_RETICLE_EXTENDED_NOTE + "\n",
                attention=Tr.FOCUSED_RETICLE_EXTENDED_ATTENTION + "\n\n" +
                          _createImg(src="imgs/all-extended.jpg", width=602, height=352)
            )
        },
        g_configParams.focusedReticleExtendedEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.focusedReticleExtendedShape.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPE_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPE_BODY + "\n",
            note=_createImg(src="imgs/shapes-extended.jpg", width=402, height=412)
        ),
        g_configParams.focusedReticleExtendedColor.renderParam(
            header=Tr.RETICLE_EXTENDED_COLOR_HEADER,
            body=Tr.RETICLE_EXTENDED_COLOR_BODY
        ),
        g_configParams.focusedReticleExtendedCenterDotSize.renderParam(
            header=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_HEADER,
            body=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_NOTE
        ),
        g_configParams.focusedReticleExtendedDrawOutline.renderParam(
            header=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_HEADER,
            body=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_NOTE
        ),
        g_configParams.focusedReticleExtendedLayer.renderParam(
            header=Tr.RETICLE_EXTENDED_LAYER_HEADER,
            body=Tr.RETICLE_EXTENDED_LAYER_BODY
        ),
        g_configParams.focusedReticleExtendedBlend.renderParam(
            header=Tr.RETICLE_EXTENDED_BLEND_HEADER,
            body=Tr.RETICLE_EXTENDED_BLEND_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_BLEND_NOTE + "\n",
            attention=Tr.RETICLE_EXTENDED_BLEND_ATTENTION
        ),
        g_configParams.focusedReticleExtendedAlpha.renderParam(
            header=Tr.RETICLE_EXTENDED_ALPHA_HEADER,
            body=Tr.RETICLE_EXTENDED_ALPHA_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_ALPHA_NOTE
        ),
        {
            "type": "Label",
            "text": Tr.RETICLE_EXTENDED_SHAPES_HEADER
        },
        g_configParams.focusedReticleExtendedShapesPentagonWidth.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_BODY,
        ),
        g_configParams.focusedReticleExtendedShapesPentagonHeight.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_BODY,
        ),
        g_configParams.focusedReticleExtendedShapesTShapeThickness.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_BODY,
        ),
        g_configParams.focusedReticleExtendedShapesTShapeLength.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_NOTE
        )
    ]


def _createServerReticle():
    return [
        {
            "type": "Label",
            "text": Tr.SERVER_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="2. " + Tr.SERVER_RETICLE_HEADER,
                body=Tr.SERVER_RETICLE_BODY + "\n\n" + _createImg(src="imgs/all.jpg", width=427, height=324)
            ),
        },
        g_configParams.serverReticleEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.serverReticleType.renderParam(
            header=Tr.RETICLE_TYPE_HEADER,
            body=Tr.RETICLE_TYPE_BODY + "\n",
            note=Tr.RETICLE_TYPE_NOTE + "\n",
            attention=Tr.RETICLE_TYPE_ATTENTION
        )
    ]


def _createServerReticleExtended():
    return [
        {
            "type": "Label",
            "text": Tr.SERVER_RETICLE_EXTENDED_LABEL,
            "tooltip": createTooltip(
                header="2. " + Tr.SERVER_RETICLE_EXTENDED_HEADER,
                body=Tr.SERVER_RETICLE_EXTENDED_BODY + "\n",
                attention=Tr.SERVER_RETICLE_EXTENDED_ATTENTION + "\n\n" +
                          _createImg(src="imgs/all-extended.jpg", width=602, height=352)
            )
        },
        g_configParams.serverReticleExtendedEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.serverReticleExtendedShape.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPE_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPE_BODY + "\n",
            note=_createImg(src="imgs/shapes-extended.jpg", width=402, height=412)
        ),
        g_configParams.serverReticleExtendedColor.renderParam(
            header=Tr.RETICLE_EXTENDED_COLOR_HEADER,
            body=Tr.RETICLE_EXTENDED_COLOR_BODY
        ),
        g_configParams.serverReticleExtendedCenterDotSize.renderParam(
            header=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_HEADER,
            body=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_NOTE
        ),
        g_configParams.serverReticleExtendedDrawOutline.renderParam(
            header=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_HEADER,
            body=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_NOTE
        ),
        g_configParams.serverReticleExtendedLayer.renderParam(
            header=Tr.RETICLE_EXTENDED_LAYER_HEADER,
            body=Tr.RETICLE_EXTENDED_LAYER_BODY
        ),
        g_configParams.serverReticleExtendedBlend.renderParam(
            header=Tr.RETICLE_EXTENDED_BLEND_HEADER,
            body=Tr.RETICLE_EXTENDED_BLEND_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_BLEND_NOTE + "\n",
            attention=Tr.RETICLE_EXTENDED_BLEND_ATTENTION
        ),
        g_configParams.serverReticleExtendedAlpha.renderParam(
            header=Tr.RETICLE_EXTENDED_ALPHA_HEADER,
            body=Tr.RETICLE_EXTENDED_ALPHA_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_ALPHA_NOTE
        ),
        {
            "type": "Label",
            "text": Tr.RETICLE_EXTENDED_SHAPES_HEADER
        },
        g_configParams.serverReticleExtendedShapesPentagonWidth.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_BODY,
        ),
        g_configParams.serverReticleExtendedShapesPentagonHeight.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_BODY,
        ),
        g_configParams.serverReticleExtendedShapesTShapeThickness.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_BODY,
        ),
        g_configParams.serverReticleExtendedShapesTShapeLength.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_NOTE
        )
    ]


def _createHybridReticle():
    return [
        {
            "type": "Label",
            "text": Tr.HYBRID_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="3. " + Tr.HYBRID_RETICLE_HEADER,
                body=Tr.HYBRID_RETICLE_BODY + "\n",
                note=Tr.HYBRID_RETICLE_NOTE + "\n\n" + _createImg(src="imgs/all.jpg", width=427, height=324)
            ),
        },
        g_configParams.hybridReticleEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.hybridReticleType.renderParam(
            header=Tr.RETICLE_TYPE_HEADER,
            body=Tr.RETICLE_TYPE_BODY + "\n",
            note=Tr.RETICLE_TYPE_NOTE + "\n",
            attention=Tr.RETICLE_TYPE_ATTENTION
        ),
        g_configParams.hybridReticleHideStandardReticle.renderParam(
            header=Tr.HYBRID_RETICLE_HIDE_STANDARD_RETICLE_HEADER,
            body=Tr.HYBRID_RETICLE_HIDE_STANDARD_RETICLE_BODY + "\n",
            note=Tr.HYBRID_RETICLE_HIDE_STANDARD_RETICLE_NOTE
        )
    ]


def _createHybridReticleExtended():
    return [
        {
            "type": "Label",
            "text": Tr.HYBRID_RETICLE_EXTENDED_LABEL,
            "tooltip": createTooltip(
                header="3. " + Tr.HYBRID_RETICLE_EXTENDED_HEADER,
                body=Tr.HYBRID_RETICLE_EXTENDED_BODY + "\n",
                note=Tr.HYBRID_RETICLE_EXTENDED_NOTE + "\n",
                attention=Tr.HYBRID_RETICLE_EXTENDED_ATTENTION + "\n\n" +
                          _createImg(src="imgs/all-extended.jpg", width=602, height=352)
            )
        },
        g_configParams.hybridReticleExtendedEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.hybridReticleExtendedShape.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPE_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPE_BODY + "\n",
            note=_createImg(src="imgs/shapes-extended.jpg", width=402, height=412)
        ),
        g_configParams.hybridReticleExtendedColor.renderParam(
            header=Tr.RETICLE_EXTENDED_COLOR_HEADER,
            body=Tr.RETICLE_EXTENDED_COLOR_BODY
        ),
        g_configParams.hybridReticleExtendedCenterDotSize.renderParam(
            header=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_HEADER,
            body=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_CENTER_DOT_SIZE_NOTE
        ),
        g_configParams.hybridReticleExtendedDrawOutline.renderParam(
            header=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_HEADER,
            body=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_DRAW_OUTLINE_NOTE
        ),
        g_configParams.hybridReticleExtendedLayer.renderParam(
            header=Tr.RETICLE_EXTENDED_LAYER_HEADER,
            body=Tr.RETICLE_EXTENDED_LAYER_BODY
        ),
        g_configParams.hybridReticleExtendedBlend.renderParam(
            header=Tr.RETICLE_EXTENDED_BLEND_HEADER,
            body=Tr.RETICLE_EXTENDED_BLEND_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_BLEND_NOTE + "\n",
            attention=Tr.RETICLE_EXTENDED_BLEND_ATTENTION
        ),
        g_configParams.hybridReticleExtendedAlpha.renderParam(
            header=Tr.RETICLE_EXTENDED_ALPHA_HEADER,
            body=Tr.RETICLE_EXTENDED_ALPHA_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_ALPHA_NOTE
        ),
        {
            "type": "Label",
            "text": Tr.RETICLE_EXTENDED_SHAPES_HEADER
        },
        g_configParams.hybridReticleExtendedShapesPentagonWidth.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_WIDTH_BODY,
        ),
        g_configParams.hybridReticleExtendedShapesPentagonHeight.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_PENTAGON_HEIGHT_BODY,
        ),
        g_configParams.hybridReticleExtendedShapesTShapeThickness.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_THICKNESS_BODY,
        ),
        g_configParams.hybridReticleExtendedShapesTShapeLength.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_BODY + "\n",
            note=Tr.RETICLE_EXTENDED_SHAPES_T_SHAPE_LENGTH_NOTE
        )
    ]


# UtilsManager
def _createImg(src, width=None, height=None, vSpace=None, hSpace=None):
    template = "<img src='{0}' "

    absoluteUrl = "img://gui/dispersionreticle/" + src
    if width is not None:
        template += "width='{1}' "
    if height is not None:
        template += "height='{2}' "
    if vSpace is not None:
        template += "vspace='{3}' "
    if hSpace is not None:
        template += "hspace='{4}'  "

    template += "/>"
    return template.format(absoluteUrl, width, height, vSpace, hSpace)

