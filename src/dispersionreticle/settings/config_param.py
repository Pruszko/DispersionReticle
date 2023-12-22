from dispersionreticle.settings.config_param_types import *
from dispersionreticle.settings.translations import Tr


class ConfigParams(object):

    def __init__(self):
        self.enabled = BooleanParam(
            ["enabled"],
            defaultValue=True, disabledValue=False
        )

        self.reticleSizeMultiplier = FloatTextParam(
            ["reticle-size-multiplier"],
            minValue=0.0, maxValue=None,
            defaultValue=1.0
        )

        # focused reticle
        self.focusedReticleEnabled = BooleanParam(
            ["focused-reticle", "enabled"],
            defaultValue=True, disabledValue=False
        )
        self.focusedReticleType = OptionsParam(
            ["focused-reticle", "type"],
            [
                Option("default", 0, "1. " + Tr.RETICLE_TYPE_OPTION_DEFAULT),
                Option("purple", 1, "2. " + Tr.RETICLE_TYPE_OPTION_PURPLE)
            ],
            defaultValue="default"
        )

        # focused reticle extended
        self.focusedReticleExtendedEnabled = BooleanParam(
            ["focused-reticle-extended", "enabled"],
            defaultValue=False
        )
        self.focusedReticleExtendedShape = OptionsParam(
            ["focused-reticle-extended", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_DASHED)
            ],
            defaultValue="circle"
        )
        self.focusedReticleExtendedColor = ColorParam(
            ["focused-reticle-extended", "color"],
            defaultValue=(255, 255, 0)
        )
        self.focusedReticleExtendedDrawCenterDot = BooleanParam(
            ["focused-reticle-extended", "draw-center-dot"],
            defaultValue=False
        )
        self.focusedReticleExtendedDrawOutline = BooleanParam(
            ["focused-reticle-extended", "draw-outline"],
            defaultValue=False
        )
        self.focusedReticleExtendedLayer = OptionsParam(
            ["focused-reticle-extended", "layer"],
            [
                Option("top", 0, Tr.RETICLE_EXTENDED_LAYER_OPTION_TOP),
                Option("bottom", 1, Tr.RETICLE_EXTENDED_LAYER_OPTION_BOTTOM)
            ],
            defaultValue="bottom"
        )
        self.focusedReticleExtendedBlend = FloatSliderParam(
            ["focused-reticle-extended", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.focusedReticleExtendedAlpha = FloatSliderParam(
            ["focused-reticle-extended", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        # hybrid reticle
        self.hybridReticleEnabled = BooleanParam(
            ["hybrid-reticle", "enabled"],
            defaultValue=False
        )
        self.hybridReticleType = OptionsParam(
            ["hybrid-reticle", "type"],
            [
                Option("default", 0, "1. " + Tr.RETICLE_TYPE_OPTION_DEFAULT),
                Option("purple", 1, "2. " + Tr.RETICLE_TYPE_OPTION_PURPLE)
            ],
            defaultValue="default"
        )
        self.hybridReticleHideStandardReticle = BooleanParam(
            ["hybrid-reticle", "hide-standard-reticle"],
            defaultValue=False
        )

        # hybrid reticle extended
        self.hybridReticleExtendedEnabled = BooleanParam(
            ["hybrid-reticle-extended", "enabled"],
            defaultValue=False
        )
        self.hybridReticleExtendedShape = OptionsParam(
            ["hybrid-reticle-extended", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_DASHED)
            ],
            defaultValue="circle"
        )
        self.hybridReticleExtendedColor = ColorParam(
            ["hybrid-reticle-extended", "color"],
            defaultValue=(0, 255, 255)
        )
        self.hybridReticleExtendedDrawCenterDot = BooleanParam(
            ["hybrid-reticle-extended", "draw-center-dot"],
            defaultValue=False
        )
        self.hybridReticleExtendedDrawOutline = BooleanParam(
            ["hybrid-reticle-extended", "draw-outline"],
            defaultValue=False
        )
        self.hybridReticleExtendedLayer = OptionsParam(
            ["hybrid-reticle-extended", "layer"],
            [
                Option("top", 0, Tr.RETICLE_EXTENDED_LAYER_OPTION_TOP),
                Option("bottom", 1, Tr.RETICLE_EXTENDED_LAYER_OPTION_BOTTOM)
            ],
            defaultValue="bottom"
        )
        self.hybridReticleExtendedBlend = FloatSliderParam(
            ["hybrid-reticle-extended", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.hybridReticleExtendedAlpha = FloatSliderParam(
            ["hybrid-reticle-extended", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

        # server reticle
        self.serverReticleEnabled = BooleanParam(
            ["server-reticle", "enabled"],
            defaultValue=False
        )
        self.serverReticleType = OptionsParam(
            ["server-reticle", "type"],
            [
                Option("default", 0, "1. " + Tr.RETICLE_TYPE_OPTION_DEFAULT),
                Option("purple", 1, "2. " + Tr.RETICLE_TYPE_OPTION_PURPLE)
            ],
            defaultValue="purple"
        )

        # server reticle extended
        self.serverReticleExtendedEnabled = BooleanParam(
            ["server-reticle-extended", "enabled"],
            defaultValue=False
        )
        self.serverReticleExtendedShape = OptionsParam(
            ["server-reticle-extended", "shape"],
            [
                Option("pentagon", 0, "1. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_PENTAGON),
                Option("t-shape", 1, "2. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_T_SHAPE),
                Option("circle", 2, "3. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_CIRCLE),
                Option("dashed", 3, "4. " + Tr.RETICLE_EXTENDED_SHAPE_OPTION_DASHED)
            ],
            defaultValue="pentagon"
        )
        self.serverReticleExtendedColor = ColorParam(
            ["server-reticle-extended", "color"],
            defaultValue=(255, 0, 255)
        )
        self.serverReticleExtendedDrawCenterDot = BooleanParam(
            ["server-reticle-extended", "draw-center-dot"],
            defaultValue=False
        )
        self.serverReticleExtendedDrawOutline = BooleanParam(
            ["server-reticle-extended", "draw-outline"],
            defaultValue=False
        )
        self.serverReticleExtendedLayer = OptionsParam(
            ["server-reticle-extended", "layer"],
            [
                Option("top", 0, Tr.RETICLE_EXTENDED_LAYER_OPTION_TOP),
                Option("bottom", 1, Tr.RETICLE_EXTENDED_LAYER_OPTION_BOTTOM)
            ],
            defaultValue="bottom"
        )
        self.serverReticleExtendedBlend = FloatSliderParam(
            ["server-reticle-extended", "blend"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=0.5
        )
        self.serverReticleExtendedAlpha = FloatSliderParam(
            ["server-reticle-extended", "alpha"],
            minValue=0.0, step=0.01, maxValue=1.0,
            defaultValue=1.0
        )

    def items(self):
        return PARAM_REGISTRY.items()


g_configParams = ConfigParams()
