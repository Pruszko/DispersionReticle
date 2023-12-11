from dispersionreticle.utils.reticle_properties import ReticleType, ReticleLinkages
from dispersionreticle.utils.reticle_types.custom_reticle import CustomReticle
from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle


class ReticleRegistry(object):

    STANDARD_FOCUSED_CLIENT = VanillaReticle(name="ClientStandardFocused", gunMarkerType=4,
                                             reticleType=ReticleType.CLIENT,
                                             reticleLinkages=ReticleLinkages.GREEN)

    STANDARD_FOCUSED_SERVER = VanillaReticle(name="ServerStandardFocused", gunMarkerType=5,
                                             reticleType=ReticleType.SERVER,
                                             reticleLinkages=ReticleLinkages.GREEN)

    STANDARD_HYBRID_CLIENT = VanillaReticle(name="ClientStandardHybrid", gunMarkerType=6,
                                            reticleType=ReticleType.CLIENT,
                                            reticleLinkages=ReticleLinkages.GREEN)

    CUSTOM_FOCUSED_CLIENT = CustomReticle(name="ClientCustomFocused", gunMarkerType=7,
                                          reticleType=ReticleType.CLIENT,
                                          reticleLinkages=ReticleLinkages.GREEN)

    CUSTOM_FOCUSED_SERVER = CustomReticle(name="ServerCustomFocused", gunMarkerType=8,
                                          reticleType=ReticleType.SERVER,
                                          reticleLinkages=ReticleLinkages.GREEN)

    CUSTOM_HYBRID_CLIENT = CustomReticle(name="ClientCustomHybrid", gunMarkerType=9,
                                         reticleType=ReticleType.CLIENT,
                                         reticleLinkages=ReticleLinkages.GREEN)

    # I know it sounds dumb, but it is server "custom-server-reticle", so ...
    CUSTOM_SERVER_SERVER = CustomReticle(name="ServerCustomServer", gunMarkerType=10,
                                         reticleType=ReticleType.SERVER,
                                         reticleLinkages=ReticleLinkages.PURPLE)

    RETICLES = [STANDARD_FOCUSED_CLIENT, STANDARD_FOCUSED_SERVER, STANDARD_HYBRID_CLIENT,
                CUSTOM_FOCUSED_CLIENT, CUSTOM_FOCUSED_SERVER, CUSTOM_HYBRID_CLIENT,
                CUSTOM_SERVER_SERVER]

    FLASH_RETICLES = [CUSTOM_FOCUSED_CLIENT, CUSTOM_FOCUSED_SERVER, CUSTOM_HYBRID_CLIENT,
                      CUSTOM_SERVER_SERVER]

    @staticmethod
    def getReticleByFlashMarkerName(markerName):
        for reticle in ReticleRegistry.FLASH_RETICLES:
            if markerName in reticle.getFlashMarkerNames():
                return reticle

        return None
