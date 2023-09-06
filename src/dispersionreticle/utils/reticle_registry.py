from dispersionreticle.utils.reticle_properties import ReticleType, ReticleLinkages
from dispersionreticle.utils.reticle_types.as3_reticle import AS3Reticle
from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle


class ReticleRegistry(object):

    CLIENT_DISPERSION = VanillaReticle(name="ClientDispersion", gunMarkerType=4,
                                       reticleType=ReticleType.CLIENT,
                                       reticleLinkages=ReticleLinkages.GREEN)

    SERVER_DISPERSION = VanillaReticle(name="ServerDispersion", gunMarkerType=5,
                                       reticleType=ReticleType.SERVER,
                                       reticleLinkages=ReticleLinkages.GREEN)

    CLIENT_LATENCY = VanillaReticle(name="ClientLatency", gunMarkerType=6,
                                    reticleType=ReticleType.CLIENT,
                                    reticleLinkages=ReticleLinkages.GREEN)

    SERVER_SIMPLE = AS3Reticle(name="ServerSimple", gunMarkerType=7,
                               reticleType=ReticleType.SERVER,
                               reticleLinkages=ReticleLinkages.PURPLE)

    RETICLES = [CLIENT_DISPERSION, SERVER_DISPERSION, CLIENT_LATENCY,
                SERVER_SIMPLE]

    FLASH_RETICLES = [SERVER_SIMPLE]

    @staticmethod
    def getReticleByFlashMarkerName(markerName):
        for reticle in ReticleRegistry.FLASH_RETICLES:
            if markerName in reticle.getFlashMarkerNames():
                return reticle

        return None
