import logging

from dispersionreticle.settings.translations import Tr
from dispersionreticle.settings.config import g_config
from dispersionreticle.settings.config_param import g_configParams, createTooltip

from gui.modsSettingsApi import g_modsSettingsApi

logger = logging.getLogger(__name__)

modLinkage = "com.github.pruszko.dispersionreticle"


def registerSoftDependencySupport():
    # TODO update README
    # TODO reorganize GUI
    # TODO modify translations
    template = {
        "modDisplayName": Tr.MODNAME,
        "enabled": g_configParams.enabled.defaultMsaValue,
        "column1":
            _createIntroPart() +
            _emptyLine() +
            _createFocusedReticlePart() +
            _emptyLine() +
            _createHybridReticlePart() +
            _emptyLine() +
            _createServerReticlePart() +
            _emptyLine() +
            _createReticleSizeMultiplierPart(),
        "column2":
            _createCustomServerReticlePart()
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


def _createFocusedReticlePart():
    return [
        {
            "type": "Label",
            "text": "1. " + Tr.STANDARD_FOCUSED_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="1. " + Tr.STANDARD_FOCUSED_RETICLE_HEADER,
                body=Tr.STANDARD_FOCUSED_RETICLE_BODY + "\n",
                note=Tr.STANDARD_FOCUSED_RETICLE_NOTE + "\n\n" + _createImg(src="imgs/all.jpg", width=475, height=428)
            ),
        },
        g_configParams.standardFocusedReticleEnabled.renderParam(
            header=Tr.STANDARD_FOCUSED_RETICLE_ENABLED_HEADER,
            body=Tr.STANDARD_FOCUSED_RETICLE_ENABLED_BODY
        )
    ]


def _emptyLine():
    return [
        {
            "type": "Label",
            "text": "________________________________________"
        }
    ]


def _createHybridReticlePart():
    return [
        {
            "type": "Label",
            "text": "2. " + Tr.STANDARD_HYBRID_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="2. " + Tr.STANDARD_HYBRID_RETICLE_HEADER,
                body=Tr.STANDARD_HYBRID_RETICLE_BODY + "\n",
                note=Tr.STANDARD_HYBRID_RETICLE_NOTE + "\n\n" + _createImg(src="imgs/all.jpg", width=475, height=428)
            ),
        },
        g_configParams.standardHybridReticleEnabled.renderParam(
            header=Tr.STANDARD_HYBRID_RETICLE_ENABLED_HEADER,
            body=Tr.STANDARD_HYBRID_RETICLE_ENABLED_BODY
        ),
        g_configParams.standardHybridReticleHideStandardReticle.renderParam(
            header=Tr.STANDARD_HYBRID_RETICLE_HIDE_STANDARD_RETICLE_HEADER,
            body=Tr.STANDARD_HYBRID_RETICLE_HIDE_STANDARD_RETICLE_BODY + "\n",
            note=Tr.STANDARD_HYBRID_RETICLE_HIDE_STANDARD_RETICLE_NOTE
        )
    ]


def _createServerReticlePart():
    return [
        {
            "type": "Label",
            "text": "3. " + Tr.STANDARD_SERVER_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="3. " + Tr.STANDARD_SERVER_RETICLE_HEADER,
                body=Tr.STANDARD_SERVER_RETICLE_BODY + "\n\n" + _createImg(src="imgs/all.jpg", width=475, height=428)
            ),
        },
        g_configParams.standardServerReticleEnabled.renderParam(
            header=Tr.STANDARD_SERVER_RETICLE_ENABLED_HEADER,
            body=Tr.STANDARD_SERVER_RETICLE_ENABLED_BODY
        )
    ]


def _createCustomServerReticlePart():
    return [
        {
            "type": "Label",
            "text": "4. " + Tr.CUSTOM_SERVER_RETICLE_LABEL,
            "tooltip": createTooltip(
                header="4. " + Tr.CUSTOM_SERVER_RETICLE_HEADER,
                body=Tr.CUSTOM_SERVER_RETICLE_BODY + "\n",
                attention=Tr.CUSTOM_SERVER_RETICLE_ATTENTION + "\n\n" +
                          _createImg(src="imgs/all.jpg", width=475, height=428)
            )
        },
        g_configParams.customServerReticleEnabled.renderParam(
            header=Tr.CUSTOM_RETICLE_ENABLED_HEADER,
            body=Tr.CUSTOM_RETICLE_ENABLED_BODY
        ),
        g_configParams.customServerReticleShape.renderParam(
            header=Tr.CUSTOM_RETICLE_SHAPE_HEADER,
            body=Tr.CUSTOM_RETICLE_SHAPE_BODY + "\n",
            note=_createImg(src="imgs/simple_server.jpg", width=402, height=412)
        ),
        g_configParams.customServerReticleColor.renderParam(
            header=Tr.CUSTOM_RETICLE_COLOR_HEADER,
            body=Tr.CUSTOM_RETICLE_COLOR_BODY
        ),
        g_configParams.customServerReticleDrawCenterDot.renderParam(
            header=Tr.CUSTOM_RETICLE_DRAW_CENTER_DOT_HEADER,
            body=Tr.CUSTOM_RETICLE_DRAW_CENTER_DOT_BODY
        ),
        g_configParams.customServerReticleDrawOutline.renderParam(
            header=Tr.CUSTOM_RETICLE_DRAW_OUTLINE_HEADER,
            body=Tr.CUSTOM_RETICLE_DRAW_OUTLINE_BODY + "\n",
            note=Tr.CUSTOM_RETICLE_DRAW_OUTLINE_NOTE
        ),
        g_configParams.customServerReticleBlend.renderParam(
            header=Tr.CUSTOM_RETICLE_BLEND_HEADER,
            body=Tr.CUSTOM_RETICLE_BLEND_BODY + "\n",
            note=Tr.CUSTOM_RETICLE_BLEND_NOTE + "\n",
            attention=Tr.CUSTOM_RETICLE_BLEND_ATTENTION
        ),
        g_configParams.customServerReticleAlpha.renderParam(
            header=Tr.CUSTOM_RETICLE_ALPHA_HEADER,
            body=Tr.CUSTOM_RETICLE_ALPHA_BODY + "\n",
            note=Tr.CUSTOM_RETICLE_ALPHA_NOTE
        )
    ]


def _createReticleSizeMultiplierPart():
    return [
        g_configParams.reticleSizeMultiplier.renderParam(
            header=Tr.RETICLE_SIZE_MULTIPLIER_HEADER,
            body=Tr.RETICLE_SIZE_MULTIPLIER_BODY + "\n",
            note=Tr.RETICLE_SIZE_MULTIPLIER_NOTE
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

