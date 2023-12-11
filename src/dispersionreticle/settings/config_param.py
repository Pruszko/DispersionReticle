from dispersionreticle.settings.config_file import g_configFiles
from dispersionreticle.settings.config_param_types import *
from dispersionreticle.settings.translations import Tr


class ConfigParams(object):

    def __init__(self):
        self.enabled = BooleanParam(
            g_configFiles.config, ["enabled"],
            defaultValue=True, disabledValue=False
        )

        # standard focused reticle
        self.standardFocusedReticleEnabled = BooleanParam(
            g_configFiles.configFocusedReticle, ["standard-focused-reticle", "enabled"],
            defaultValue=True, disabledValue=False
        )

        # custom focused reticle
        self.customFocusedReticleEnabled = BooleanParam(
            g_configFiles.configFocusedReticle, ["custom-focused-reticle", "enabled"],
            defaultValue=False
        )
        self.customFocusedReticleShape = OptionsParam(
            g_configFiles.configFocusedReticle, ["custom-focused-reticle", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_DASHED)
            ],
            defaultValue="circle"
        )
        self.customFocusedReticleColor = ColorParam(
            g_configFiles.configFocusedReticle, ["custom-focused-reticle", "color"],
            defaultValue=(255, 0, 255)
        )
        self.customFocusedReticleDrawCenterDot = BooleanParam(
            g_configFiles.configFocusedReticle, ["custom-focused-reticle", "draw-center-dot"],
            defaultValue=False
        )
        self.customFocusedReticleDrawOutline = BooleanParam(
            g_configFiles.configFocusedReticle, ["custom-focused-reticle", "draw-outline"],
            defaultValue=False
        )
        self.customFocusedReticleBlend = FloatSliderParam(
            g_configFiles.configFocusedReticle, ["custom-focused-reticle", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.customFocusedReticleAlpha = FloatSliderParam(
            g_configFiles.configFocusedReticle, ["custom-focused-reticle", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        # standard hybrid reticle
        self.standardHybridReticleEnabled = BooleanParam(
            g_configFiles.configHybridReticle, ["standard-hybrid-reticle", "enabled"],
            defaultValue=False
        )
        self.standardHybridReticleHideStandardReticle = BooleanParam(
            g_configFiles.configHybridReticle, ["standard-hybrid-reticle", "hide-standard-reticle"],
            defaultValue=False
        )

        # custom hybrid reticle
        self.customHybridReticleEnabled = BooleanParam(
            g_configFiles.configHybridReticle, ["custom-hybrid-reticle", "enabled"],
            defaultValue=False
        )
        self.customHybridReticleShape = OptionsParam(
            g_configFiles.configHybridReticle, ["custom-hybrid-reticle", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_DASHED)
            ],
            defaultValue="circle"
        )
        self.customHybridReticleColor = ColorParam(
            g_configFiles.configHybridReticle, ["custom-hybrid-reticle", "color"],
            defaultValue=(255, 0, 255)
        )
        self.customHybridReticleDrawCenterDot = BooleanParam(
            g_configFiles.configHybridReticle, ["custom-hybrid-reticle", "draw-center-dot"],
            defaultValue=False
        )
        self.customHybridReticleDrawOutline = BooleanParam(
            g_configFiles.configHybridReticle, ["custom-hybrid-reticle", "draw-outline"],
            defaultValue=False
        )
        self.customHybridReticleBlend = FloatSliderParam(
            g_configFiles.configHybridReticle, ["custom-hybrid-reticle", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.customHybridReticleAlpha = FloatSliderParam(
            g_configFiles.configHybridReticle, ["custom-hybrid-reticle", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        # standard server reticle
        self.standardServerReticleEnabled = BooleanParam(
            g_configFiles.configServerReticle, ["standard-server-reticle", "enabled"],
            defaultValue=False
        )

        # custom server reticle
        self.customServerReticleEnabled = BooleanParam(
            g_configFiles.configServerReticle, ["custom-server-reticle", "enabled"],
            defaultValue=False
        )
        self.customServerReticleShape = OptionsParam(
            g_configFiles.configServerReticle, ["custom-server-reticle", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_DASHED)
            ],
            defaultValue="pentagon"
        )
        self.customServerReticleColor = ColorParam(
            g_configFiles.configServerReticle, ["custom-server-reticle", "color"],
            defaultValue=(255, 0, 255)
        )
        self.customServerReticleDrawCenterDot = BooleanParam(
            g_configFiles.configServerReticle, ["custom-server-reticle", "draw-center-dot"],
            defaultValue=False
        )
        self.customServerReticleDrawOutline = BooleanParam(
            g_configFiles.configServerReticle, ["custom-server-reticle", "draw-outline"],
            defaultValue=False
        )
        self.customServerReticleBlend = FloatSliderParam(
            g_configFiles.configServerReticle, ["custom-server-reticle", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.customServerReticleAlpha = FloatSliderParam(
            g_configFiles.configServerReticle, ["custom-server-reticle", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        self.reticleSizeMultiplier = FloatTextParam(
            g_configFiles.config, ["reticle-size-multiplier"],
            minValue=0.0, maxValue=None,
            defaultValue=1.0
        )

    def items(self):
        return PARAM_REGISTRY.items()


g_configParams = ConfigParams()
