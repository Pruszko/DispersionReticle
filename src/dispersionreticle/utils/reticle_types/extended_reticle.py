from aih_constants import GUN_MARKER_TYPE

from dispersionreticle.utils.reticle_types.overridden_reticle import OverriddenReticle


class ExtendedReticle(OverriddenReticle):

    # gm_factory
    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createExtendedSniperMarker(self._gunMarkerType, self.markerNames.sniperGunMarkerName))
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createExtendedSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.sniperGunMarkerName))

    # gm_factory
    def createSPGMarkers(self, gunMarkerFactory, markerType):
        # important
        # here we avoid spawning AS3 marker for SPG
        # because it will simply "not work normally"
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createSPGMarker(self._gunMarkerType, self.markerNames.spgGunMarkerName))
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.spgGunMarkerName))

    # Lesta specific
    # gm_factory
    #
    # it won't be called on WG client
    def createAssaultSPGMarkers(self, gunMarkerFactory, markerType):
        # important
        # here we avoid spawning AS3 marker for assault tanks
        # because it will simply "not work normally"
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createAssaultSPGMarker(self._gunMarkerType, self.markerNames.spgGunMarkerName))
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createAssaultSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.spgGunMarkerName))

    # gm_factory
    def createArcadeOnlySPGMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),)
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),)

    # gm_factory
    def createDualGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self.markerNames.dualGunArcadeGunMarkerName),
                    gunMarkerFactory._createExtendedSniperMarker(self._gunMarkerType, self.markerNames.dualGunSniperGunMarkerName))
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.dualGunArcadeGunMarkerName),
                gunMarkerFactory._createExtendedSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.dualGunSniperGunMarkerName))
