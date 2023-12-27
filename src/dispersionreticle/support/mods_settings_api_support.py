import logging

from dispersionreticle.settings.translations import Tr
from dispersionreticle.settings.config import g_config
from dispersionreticle.settings.config_param import g_configParams, createTooltip

from gui.modsSettingsApi import g_modsSettingsApi

logger = logging.getLogger(__name__)

modLinkage = "com.github.pruszko.dispersionreticle"


def registerSoftDependencySupport():
    # TODO update README
    # TODO update RU and ZH_CN translations
    # TODO update images
    # TODO improve config error handling
    template = {
        "modDisplayName": Tr.MODNAME,
        "enabled": g_configParams.enabled.defaultMsaValue,
        "column1":
            _createIntroPart() +
            _emptyLine(3) +
            _endSection() +
            _createFocusedReticle() +
            _endSection() +
            _createFocusedReticleExtended() +
            _endSection() +
            _createHybridReticle() +
            _endSection() +
            _createHybridReticleExtended(),
        "column2":
            _createCommon() +
            _endSection() +
            _createServerReticle() +
            _endSection() +
            _createServerReticleExtended() +
            _endSection()
    }

    # we purposely ignore ModsSettingsAPI capability of saving mod configuration
    # due to config file being "master" configuration
    #
    # also, I don't like going against "standard setup" of ModsSettingsAPI support
    # but we still treat it only as a GUI, not a configuration framework
    #
    # so we also purposely always call setModTemplate instead of registerCallback
    # to keep always updated GUI template
    g_modsSettingsApi.setModTemplate(modLinkage, template, onModSettingsChanged)

    # update settings with actual values read from config file
    # this will purposely cause cycle like this:
    # - onConfigFileReload - write to MSA
    # - onModSettingsChanged - callback from MSA
    # - onConfigFileReload - callback from config reload event
    # - cancelled onModSettingsChanged to prevent cycle, because both mods are already synchronized
    onConfigFileReload()
    g_config.onConfigReload += onConfigFileReload


# onSettingsChanged can be called in an infinite cycle:
# - onSettingsChanged - callback from MSA
# - onConfigFileReload - callback from config reload event;
#                        config file, our mod state and MSA settings are updated
# - onSettingsChanged - unnecessary callback from MSA, because
#                       after onConfigFileReload both mods are already synchronized
#
# in order to prevent this, we have to track when this event
# is during execution of itself to cancel this cycle
#
# by exactly this kind of cycle, settings are synchronized in such way
# that GUI will have actual settings that entire settings synchronization process evaluated
# including parameters value constraints (for ex. handling abnormal values in FloatTextParam
# or invalid values from config file in general)
#
# unfortunately, we cannot update ModsSettingsAPI settings without triggering this event
# normally I would like to pass event trigger cause
# to react differently to MSA event triggered by onConfigFileReload event
# and actual user-triggered MSA save settings
_IS_DURING_SETTINGS_CHANGED = False


def onModSettingsChanged(linkage, newSettings):
    global _IS_DURING_SETTINGS_CHANGED

    if linkage != modLinkage or _IS_DURING_SETTINGS_CHANGED:
        return

    _IS_DURING_SETTINGS_CHANGED = True

    try:
        _onModSettingsChanged(newSettings)
    except Exception as e:
        logger.error("Error occurred while ModsSettingsAPI settings change.", exc_info=e)
    finally:
        _IS_DURING_SETTINGS_CHANGED = False


def _onModSettingsChanged(newSettings):
    serializedSettings = {}
    for tokenName, param in g_configParams.items():
        if tokenName not in newSettings:
            continue

        value = param.fromMsaValue(newSettings[tokenName])
        jsonValue = param.toJsonValue(value)

        serializedSettings[param.tokenName] = jsonValue

    g_config.updateConfigSafely(serializedSettings)


def onConfigFileReload():
    msaSettings = {}

    for tokenName, param in g_configParams.items():
        msaSettings[tokenName] = param.msaValue

    g_modsSettingsApi.updateModSettings(modLinkage, newSettings=msaSettings)


def _endSection():
    return _emptyLine() + _horizontalLine()


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


def _createCommon():
    return [
        g_configParams.reticleSizeMultiplier.renderParam(
            header=Tr.RETICLE_SIZE_MULTIPLIER_HEADER,
            body=Tr.RETICLE_SIZE_MULTIPLIER_BODY + "\n",
            note=Tr.RETICLE_SIZE_MULTIPLIER_NOTE
        )
    ]


def _createFocusedReticle():
    return [
        {
            "type": "Label",
            "text": "1. " + Tr.FOCUSED_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="1. " + Tr.FOCUSED_RETICLE_HEADER,
                body=Tr.FOCUSED_RETICLE_BODY + "\n",
                note=Tr.FOCUSED_RETICLE_NOTE + "\n\n" + _createImg(src="imgs/all.jpg", width=475, height=428)
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
            "text": "2. " + Tr.FOCUSED_RETICLE_EXTENDED_LABEL,
            "tooltip": createTooltip(
                header="2. " + Tr.FOCUSED_RETICLE_EXTENDED_HEADER,
                body=Tr.FOCUSED_RETICLE_EXTENDED_BODY + "\n",
                note=Tr.FOCUSED_RETICLE_EXTENDED_NOTE + "\n",
                attention=Tr.FOCUSED_RETICLE_EXTENDED_ATTENTION + "\n\n" +
                          _createImg(src="imgs/all.jpg", width=475, height=428)
            )
        },
        g_configParams.focusedReticleExtendedEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.focusedReticleExtendedShape.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPE_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPE_BODY + "\n",
            note=_createImg(src="imgs/simple_server.jpg", width=402, height=412)
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
            "text": "3. " + Tr.SERVER_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="3. " + Tr.SERVER_RETICLE_HEADER,
                body=Tr.SERVER_RETICLE_BODY + "\n\n" + _createImg(src="imgs/all.jpg", width=475, height=428)
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
            "text": "4. " + Tr.SERVER_RETICLE_EXTENDED_LABEL,
            "tooltip": createTooltip(
                header="4. " + Tr.SERVER_RETICLE_EXTENDED_HEADER,
                body=Tr.SERVER_RETICLE_EXTENDED_BODY + "\n",
                attention=Tr.SERVER_RETICLE_EXTENDED_ATTENTION + "\n\n" +
                          _createImg(src="imgs/all.jpg", width=475, height=428)
            )
        },
        g_configParams.serverReticleExtendedEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.serverReticleExtendedShape.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPE_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPE_BODY + "\n",
            note=_createImg(src="imgs/simple_server.jpg", width=402, height=412)
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
            "text": "5. " + Tr.HYBRID_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="5. " + Tr.HYBRID_RETICLE_HEADER,
                body=Tr.HYBRID_RETICLE_BODY + "\n",
                note=Tr.HYBRID_RETICLE_NOTE + "\n\n" + _createImg(src="imgs/all.jpg", width=475, height=428)
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
            "text": "6. " + Tr.HYBRID_RETICLE_EXTENDED_LABEL,
            "tooltip": createTooltip(
                header="6. " + Tr.HYBRID_RETICLE_EXTENDED_HEADER,
                body=Tr.HYBRID_RETICLE_EXTENDED_BODY + "\n",
                note=Tr.HYBRID_RETICLE_EXTENDED_NOTE + "\n",
                attention=Tr.HYBRID_RETICLE_EXTENDED_ATTENTION + "\n\n" +
                          _createImg(src="imgs/all.jpg", width=475, height=428)
            )
        },
        g_configParams.hybridReticleExtendedEnabled.renderParam(
            header=Tr.RETICLE_ENABLED_HEADER,
            body=Tr.RETICLE_ENABLED_BODY
        ),
        g_configParams.hybridReticleExtendedShape.renderParam(
            header=Tr.RETICLE_EXTENDED_SHAPE_HEADER,
            body=Tr.RETICLE_EXTENDED_SHAPE_BODY + "\n",
            note=_createImg(src="imgs/simple_server.jpg", width=402, height=412)
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

