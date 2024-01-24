from AvatarInputHandler.aih_global_binding import BINDING_ID

from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.utils import isClientLesta
from dispersionreticle.utils.reticle_properties import ReticleType, ReticleLinkages, MarkerNames
from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle
from dispersionreticle.utils.reticle_types.extended_reticle import ExtendedReticle
from dispersionreticle.utils.reticle_types.overridden_reticle import OverriddenReticle


# Lesta specific
# avoid accessing Lesta bindings on WG client
# also, reticle classes are prepared to ignore them in such case
if isClientLesta():
    clientAssaultSpgDataProviderID = BINDING_ID.CLIENT_ASSAULT_SPG_GUN_MARKER_DATA_PROVIDER
    serverAssaultSpgDataProviderID = BINDING_ID.SERVER_ASSAULT_SPG_GUN_MARKER_DATA_PROVIDER
else:
    clientAssaultSpgDataProviderID = None
    serverAssaultSpgDataProviderID = None


class ReticleRegistry(object):

    # used only as reference
    VANILLA_CLIENT = VanillaReticle(markerNames=MarkerNames.createStandardMarkerNames(), gunMarkerType=1,
                                    reticleType=ReticleType.CLIENT,
                                    markerLinkagesProvider=ReticleLinkages.greenLinkagesProvider,
                                    standardDataProviderID=BINDING_ID.CLIENT_GUN_MARKER_DATA_PROVIDER,
                                    spgDataProviderID=BINDING_ID.CLIENT_SPG_GUN_MARKER_DATA_PROVIDER,
                                    assaultSpgDataProviderID=clientAssaultSpgDataProviderID)  # Lesta specific

    VANILLA_SERVER = VanillaReticle(markerNames=MarkerNames.createStandardMarkerNames(), gunMarkerType=2,
                                    reticleType=ReticleType.SERVER,
                                    markerLinkagesProvider=ReticleLinkages.greenLinkagesProvider,
                                    standardDataProviderID=BINDING_ID.SERVER_GUN_MARKER_DATA_PROVIDER,
                                    spgDataProviderID=BINDING_ID.SERVER_SPG_GUN_MARKER_DATA_PROVIDER,
                                    assaultSpgDataProviderID=serverAssaultSpgDataProviderID)  # Lesta specific

    # purposely not using DUAL_ACC here because it's ... special
    # we don't need it anyway

    # purposely declare separate server reticle to simplify linkage changes
    # otherwise, if VANILLA_SERVER were altered to debug linkages, then "Use server aim"
    # from in-game settings would be purple (it should be always green)
    #
    # by this, we also have better control over rendering order
    #
    # this is due to WG code using same marker names for VANILLA_CLIENT and VANILLA_SERVER reticles
    # what is problematic when we want to distinguish reticles by marker names
    DEBUG_SERVER = OverriddenReticle(nameSuffix="ServerDebug", gunMarkerType=4,
                                     reticleType=ReticleType.SERVER,
                                     markerLinkagesProvider=ReticleLinkages.createParamLinkagesProvider(g_configParams.serverReticleType))

    FOCUSED_CLIENT = OverriddenReticle(nameSuffix="ClientFocused", gunMarkerType=5,
                                       reticleType=ReticleType.CLIENT,
                                       markerLinkagesProvider=ReticleLinkages.createParamLinkagesProvider(g_configParams.focusedReticleType))

    FOCUSED_SERVER = OverriddenReticle(nameSuffix="ServerFocused", gunMarkerType=6,
                                       reticleType=ReticleType.SERVER,
                                       markerLinkagesProvider=ReticleLinkages.createParamLinkagesProvider(g_configParams.focusedReticleType))

    HYBRID_CLIENT = OverriddenReticle(nameSuffix="ClientHybrid", gunMarkerType=7,
                                      reticleType=ReticleType.CLIENT,
                                      markerLinkagesProvider=ReticleLinkages.createParamLinkagesProvider(g_configParams.hybridReticleType))

    FOCUSED_EXTENDED_CLIENT = ExtendedReticle(nameSuffix="ClientFocusedExtended", gunMarkerType=8,
                                              reticleType=ReticleType.CLIENT,
                                              markerLinkagesProvider=FOCUSED_CLIENT._markerLinkagesProvider,
                                              layerProvider=g_configParams.focusedReticleExtendedLayer)

    FOCUSED_EXTENDED_SERVER = ExtendedReticle(nameSuffix="ServerFocusedExtended", gunMarkerType=9,
                                              reticleType=ReticleType.SERVER,
                                              markerLinkagesProvider=FOCUSED_SERVER._markerLinkagesProvider,
                                              layerProvider=g_configParams.focusedReticleExtendedLayer)

    HYBRID_EXTENDED_CLIENT = ExtendedReticle(nameSuffix="ClientHybridExtended", gunMarkerType=10,
                                             reticleType=ReticleType.CLIENT,
                                             markerLinkagesProvider=HYBRID_CLIENT._markerLinkagesProvider,
                                             layerProvider=g_configParams.hybridReticleExtendedLayer)

    # I know it sounds dumb, but it is server "server-reticle-extended", so ...
    SERVER_EXTENDED_SERVER = ExtendedReticle(nameSuffix="ServerServerExtended", gunMarkerType=11,
                                             reticleType=ReticleType.SERVER,
                                             markerLinkagesProvider=DEBUG_SERVER._markerLinkagesProvider,
                                             layerProvider=g_configParams.serverReticleExtendedLayer)

    OVERRIDDEN_RETICLES = [DEBUG_SERVER, FOCUSED_CLIENT, FOCUSED_SERVER, HYBRID_CLIENT]

    EXTENDED_RETICLES = [FOCUSED_EXTENDED_CLIENT, FOCUSED_EXTENDED_SERVER, HYBRID_EXTENDED_CLIENT,
                         SERVER_EXTENDED_SERVER]

    ADDITIONAL_RETICLES = OVERRIDDEN_RETICLES + EXTENDED_RETICLES

    ALL_RETICLES = [VANILLA_CLIENT, VANILLA_SERVER] + ADDITIONAL_RETICLES

    @staticmethod
    def getReticleByFlashMarkerName(markerName):
        for reticle in ReticleRegistry.EXTENDED_RETICLES:
            if markerName in reticle.getFlashMarkerNames():
                return reticle

        return None
