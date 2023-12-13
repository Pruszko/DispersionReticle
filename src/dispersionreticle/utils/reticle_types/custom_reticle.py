from aih_constants import GUN_MARKER_TYPE

from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle


class CustomReticle(VanillaReticle):

    def getFlashMarkerNames(self):
        return (
            self.arcadeGunMarkerName,
            self.sniperGunMarkerName,
            self.dualGunArcadeGunMarkerName,
            self.dualGunSniperGunMarkerName
        )

    # gm_factory
    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createCustomArcadeMarker(self.gunMarkerType, self.arcadeGunMarkerName),
                    gunMarkerFactory._createCustomSniperMarker(self.gunMarkerType, self.sniperGunMarkerName))
        return (gunMarkerFactory._createCustomArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.arcadeGunMarkerName),
                gunMarkerFactory._createCustomSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.sniperGunMarkerName))

    # gm_factory
    def createSPGMarkers(self, gunMarkerFactory, markerType):
        # important
        # here we avoid spawning AS3 marker for SPG
        # because it will simply "not work normally"
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createCustomArcadeMarker(self.gunMarkerType, self.arcadeGunMarkerName),
                    gunMarkerFactory._createSPGMarker(self.gunMarkerType, self.spgGunMarkerName))
        return (gunMarkerFactory._createCustomArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.arcadeGunMarkerName),
                gunMarkerFactory._createSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self.spgGunMarkerName))

    # gm_factory
    def createArcadeOnlySPGMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createCustomArcadeMarker(self.gunMarkerType, self.arcadeGunMarkerName),)
        return (gunMarkerFactory._createCustomArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.arcadeGunMarkerName),)

    # gm_factory
    def createDualGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createCustomArcadeMarker(self.gunMarkerType, self.dualGunArcadeGunMarkerName),
                    gunMarkerFactory._createCustomSniperMarker(self.gunMarkerType, self.dualGunSniperGunMarkerName))
        return (gunMarkerFactory._createCustomArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.dualGunArcadeGunMarkerName),
                gunMarkerFactory._createCustomSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.dualGunSniperGunMarkerName))