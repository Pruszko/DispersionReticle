from dispersionreticle.settings.config_param_types import *
from dispersionreticle.settings.translations import Tr


class ConfigParams(object):

    def __init__(self):
        self.enabled = BooleanParam(
            ["enabled"],
            defaultValue=True, disabledValue=False
        )

        # standard focused reticle
        self.standardFocusedReticleEnabled = BooleanParam(
            ["standard-focused-reticle", "enabled"],
            defaultValue=True, disabledValue=False
        )

        # custom focused reticle
        self.customFocusedReticleEnabled = BooleanParam(
            ["custom-focused-reticle", "enabled"],
            defaultValue=False
        )
        self.customFocusedReticleShape = OptionsParam(
            ["custom-focused-reticle", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_DASHED)
            ],
            defaultValue="circle"
        )
        self.customFocusedReticleColor = ColorParam(
            ["custom-focused-reticle", "color"],
            defaultValue=(255, 255, 0)
        )
        self.customFocusedReticleDrawCenterDot = BooleanParam(
            ["custom-focused-reticle", "draw-center-dot"],
            defaultValue=False
        )
        self.customFocusedReticleDrawOutline = BooleanParam(
            ["custom-focused-reticle", "draw-outline"],
            defaultValue=False
        )
        self.customFocusedReticleBlend = FloatSliderParam(
            ["custom-focused-reticle", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.customFocusedReticleAlpha = FloatSliderParam(
            ["custom-focused-reticle", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        # standard hybrid reticle
        self.standardHybridReticleEnabled = BooleanParam(
            ["standard-hybrid-reticle", "enabled"],
            defaultValue=False
        )
        self.standardHybridReticleHideStandardReticle = BooleanParam(
            ["standard-hybrid-reticle", "hide-standard-reticle"],
            defaultValue=False
        )

        # custom hybrid reticle
        self.customHybridReticleEnabled = BooleanParam(
            ["custom-hybrid-reticle", "enabled"],
            defaultValue=False
        )
        self.customHybridReticleShape = OptionsParam(
            ["custom-hybrid-reticle", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_DASHED)
            ],
            defaultValue="circle"
        )
        self.customHybridReticleColor = ColorParam(
            ["custom-hybrid-reticle", "color"],
            defaultValue=(0, 255, 255)
        )
        self.customHybridReticleDrawCenterDot = BooleanParam(
            ["custom-hybrid-reticle", "draw-center-dot"],
            defaultValue=False
        )
        self.customHybridReticleDrawOutline = BooleanParam(
            ["custom-hybrid-reticle", "draw-outline"],
            defaultValue=False
        )
        self.customHybridReticleBlend = FloatSliderParam(
            ["custom-hybrid-reticle", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.customHybridReticleAlpha = FloatSliderParam(
            ["custom-hybrid-reticle", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        # standard server reticle
        self.standardServerReticleEnabled = BooleanParam(
            ["standard-server-reticle", "enabled"],
            defaultValue=False
        )

        # custom server reticle
        self.customServerReticleEnabled = BooleanParam(
            ["custom-server-reticle", "enabled"],
            defaultValue=False
        )
        self.customServerReticleShape = OptionsParam(
            ["custom-server-reticle", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.CUSTOM_RETICLE_SHAPE_OPTION_DASHED)
            ],
            defaultValue="pentagon"
        )
        self.customServerReticleColor = ColorParam(
            ["custom-server-reticle", "color"],
            defaultValue=(255, 0, 255)
        )
        self.customServerReticleDrawCenterDot = BooleanParam(
            ["custom-server-reticle", "draw-center-dot"],
            defaultValue=False
        )
        self.customServerReticleDrawOutline = BooleanParam(
            ["custom-server-reticle", "draw-outline"],
            defaultValue=False
        )
        self.customServerReticleBlend = FloatSliderParam(
            ["custom-server-reticle", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.customServerReticleAlpha = FloatSliderParam(
            ["custom-server-reticle", "alpha"],
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


g_configParams = ConfigParams()
