from dispersionreticle.utils.reticle_properties import ReticleType, ReticleLinkages
from dispersionreticle.utils.reticle_types.extended_reticle import ExtendedReticle
from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle


class ReticleRegistry(object):

    FOCUSED_CLIENT = VanillaReticle(name="ClientFocused", gunMarkerType=4,
                                    reticleType=ReticleType.CLIENT,
                                    reticleLinkages=ReticleLinkages.GREEN)

    FOCUSED_SERVER = VanillaReticle(name="ServerFocused", gunMarkerType=5,
                                    reticleType=ReticleType.SERVER,
                                    reticleLinkages=ReticleLinkages.GREEN)

    HYBRID_CLIENT = VanillaReticle(name="ClientHybrid", gunMarkerType=6,
                                   reticleType=ReticleType.CLIENT,
                                   reticleLinkages=ReticleLinkages.GREEN)

    FOCUSED_EXTENDED_CLIENT = ExtendedReticle(name="ClientFocusedExtended", gunMarkerType=7,
                                              reticleType=ReticleType.CLIENT,
                                              reticleLinkages=ReticleLinkages.GREEN)

    FOCUSED_EXTENDED_SERVER = ExtendedReticle(name="ServerFocusedExtended", gunMarkerType=8,
                                              reticleType=ReticleType.SERVER,
                                              reticleLinkages=ReticleLinkages.GREEN)

    HYBRID_EXTENDED_CLIENT = ExtendedReticle(name="ClientHybridExtended", gunMarkerType=9,
                                             reticleType=ReticleType.CLIENT,
                                             reticleLinkages=ReticleLinkages.GREEN)

    # I know it sounds dumb, but it is server "server-reticle-extended", so ...
    SERVER_EXTENDED_SERVER = ExtendedReticle(name="ServerServerExtended", gunMarkerType=10,
                                             reticleType=ReticleType.SERVER,
                                             reticleLinkages=ReticleLinkages.PURPLE)

    RETICLES = [FOCUSED_CLIENT, FOCUSED_SERVER, HYBRID_CLIENT,
                FOCUSED_EXTENDED_CLIENT, FOCUSED_EXTENDED_SERVER, HYBRID_EXTENDED_CLIENT,
                SERVER_EXTENDED_SERVER]

    FLASH_RETICLES = [FOCUSED_EXTENDED_CLIENT, FOCUSED_EXTENDED_SERVER, HYBRID_EXTENDED_CLIENT,
                      SERVER_EXTENDED_SERVER]

    @staticmethod
    def getReticleByFlashMarkerName(markerName):
        for reticle in ReticleRegistry.FLASH_RETICLES:
            if markerName in reticle.getFlashMarkerNames():
                return reticle

        return None
