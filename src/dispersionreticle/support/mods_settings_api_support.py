import logging

from dispersionreticle.settings.config import g_config
from dispersionreticle.settings.config_param import g_configParams, createTooltip

from gui.modsSettingsApi import g_modsSettingsApi


logger = logging.getLogger(__name__)

modLinkage = "com.github.pruszko.dispersionreticle"


def registerSoftDependencySupport():
    template = {
        "modDisplayName": "DispersionReticle",
        "enabled": g_configParams.enabled.defaultMsaValue,
        "column1":
            _createIntroPart() +
            _emptyLine() +
            _createDispersionReticlePart() +
            _emptyLine() +
            _createLatencyReticlePart() +
            _emptyLine() +
            _createServerReticlePart() +
            _emptyLine() +
            _createReticleSizeMultiplierPart(),
        "column2":
            _createSimpleServerReticlePart()
    }

    # we purposely ignore ModsSettingsAPI capability of saving mod configuration
    # due to config file being "master" configuration
    #
    # also, I don't like going against "standard setup" of ModsSettingsAPI support
    # but we still treat it only as a GUI, not an configuration framework
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

        param.msaValue = newSettings[tokenName]

        serializedSettings[param.tokenName] = param.jsonValue

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
            "text": "Config file info:",
            "tooltip": createTooltip(
                header="Config file",
                body="Config can also be changed by manually altering config file.\n"
                     "For changes to take effect, reload it in game using hotkeys:\n"
                     "- CTRL + P\n\n"
                     "Config file location:\n"
                     "- [WoT game directory]/mods/configs/DispersionReticle/config.json\n",
                note="If you want to generate default config file, delete its file and:\n"
                     "- either reload it with above hotkey\n"
                     "- or launch a game again\n",
                attention="Don't use CTRL + P hotkey with open mod configurator.\n"
                          "This gui won't notice it unless reopened."
            )
        }
    ]


def _createDispersionReticlePart():
    return [
        {
            "type": "Label",
            "text": "Dispersion reticle",
            "tooltip": createTooltip(
                header="Dispersion reticle",
                body="Adds reticle displaying fully-focused dispersion to standard reticle.\n",
                note="When both client-side and server-side reticle are on, it attaches to client-side reticle.\n\n" +
                     _createImg(src="all.jpg", width=475, height=428)
            ),
        },
        g_configParams.dispersionReticleEnabled.renderParam(
            header="Enabled",
            body="If checked, display this reticle."
        )
    ]


def _emptyLine():
    return [
        {
            "type": "Empty"
        },
        {
            "type": "Empty"
        }
    ]


def _createLatencyReticlePart():
    return [
        {
            "type": "Label",
            "text": "Latency reticle",
            "tooltip": createTooltip(
                header="Latency reticle",
                body="Adds reticle displaying current server-side dispersion to client-side reticle.\n",
                note="Basically, client-side position, but server-side dispersion.\n"
                     "By this, client-side and server-side dispersion desynchronization is clearly visible.\n\n"
                     "Useful if you want to know server-side dispersion, but still want "
                     "client-side responsiveness.\n\n" +
                     _createImg(src="all.jpg", width=475, height=428)
            ),
        },
        g_configParams.latencyReticleEnabled.renderParam(
            header="Enabled",
            body="If checked, display this reticle."
        ),
        g_configParams.latencyReticleHideStandardReticle.renderParam(
            header="Hide standard reticle",
            body="If checked, standard client reticle is hidden while latency reticle is enabled.\n",
            note="Useful if you want to only use latency reticle instead of standard reticle."
        )
    ]


def _createServerReticlePart():
    return [
        {
            "type": "Label",
            "text": "Server reticle",
            "tooltip": createTooltip(
                header="Server reticle",
                body="Adds server-side reticle alongside with client-side reticle.\n\n" +
                     _createImg(src="all.jpg", width=475, height=428)
            ),
        },
        g_configParams.serverReticleEnabled.renderParam(
            header="Enabled",
            body="If checked, display this reticle."
        )
    ]


def _createSimpleServerReticlePart():
    return [
        {
            "type": "Label",
            "text": "Simple server reticle",
            "tooltip": createTooltip(
                header="Simple server reticle",
                body="Adds server-side reticle with customizable shape alongside with client-side reticle.\n",
                attention="For SPG artillery view, it will implicitly enable Server reticle on the left "
                          "instead of this reticle.\n\n" +
                          _createImg(src="all.jpg", width=475, height=428)
            )
        },
        g_configParams.simpleServerReticleEnabled.renderParam(
            header="Enabled",
            body="If checked, display this reticle."
        ),
        g_configParams.simpleServerReticleShape.renderParam(
            header="Shape",
            body="Shape which this reticle should have.\n",
            note=_createImg(src="simple_server.jpg", width=402, height=412)
        ),
        g_configParams.simpleServerReticleColor.renderParam(
            header="Color",
            body="Colors this reticle using provided color."
        ),
        g_configParams.simpleServerReticleDrawOutline.renderParam(
            header="Draw outline",
            body="If checked, shape is additionally displayed with 1 pixel black outline.\n",
            note="Useful if shape color blends with the background."
        ),
        g_configParams.simpleServerReticleBlend.renderParam(
            header="Blend",
            body="Controls, how much reticle color will blend with the background color "
                 "instead of replacing it.\n"
                 "Vanilla \"dashed\" reticle uses this with value 1.0 without outline to make reticle "
                 "look more natural.\n",
            note="Set it to 1.0 if you want color to fully act as an addition to background color.\n"
                 "Set it to 0.0 if you want color to fully replace background color.\n"
                 "Values between them controls strength of those effects the closer it gets to them.\n",
            attention="Value 1.0 effectively prevents you from getting dark colors\n"
                      "because ... black color + background color = background color."
        ),
        g_configParams.simpleServerReticleAlpha.renderParam(
            header="Alpha",
            body="Controls transparency of displayed reticle.\n",
            note="Value 1.0 means full visibility\n"
                 "Value 0.0 means zero visibility"
        )
    ]


def _createReticleSizeMultiplierPart():
    return [
        g_configParams.reticleSizeMultiplier.renderParam(
            header="Reticle size multiplier",
            body="Scales all reticles size by factor, except SPG top-view reticle.\n",
            note="WG's displayed reticle dispersion is noticeably bigger than actual gun dispersion.\n"
                 "It was discovered by Jak_Attackka, StranikS_Scan and others.\n"
                 "By this setting you can scale it to actual displayed dispersion.\n\n"
                 "Good known values:\n"
                 "- 1.0 (default \"wrong\" WG dispersion)\n"
                 "- 0.6 (factor determined by me)\n"
                 "- 0.5848 (factor determined by Jak_Attackka, StranikS_Scan and others)"
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

