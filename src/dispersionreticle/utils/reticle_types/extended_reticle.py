from aih_constants import GUN_MARKER_TYPE

from dispersionreticle.utils.reticle_types.overridden_reticle import OverriddenReticle


class ExtendedReticle(OverriddenReticle):

    def getFlashMarkerNames(self):
        return (
            self._markerNames.arcadeGunMarkerName,
            self._markerNames.sniperGunMarkerName,
            self._markerNames.dualGunArcadeGunMarkerName,
            self._markerNames.dualGunSniperGunMarkerName
        )

    # gm_factory
    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self._markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createExtendedSniperMarker(self._gunMarkerType, self._markerNames.sniperGunMarkerName))
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createExtendedSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.sniperGunMarkerName))

    # gm_factory
    def createSPGMarkers(self, gunMarkerFactory, markerType):
        # important
        # here we avoid spawning AS3 marker for SPG
        # because it will simply "not work normally"
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self._markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createSPGMarker(self._gunMarkerType, self._markerNames.spgGunMarkerName))
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.spgGunMarkerName))

    # gm_factory
    def createArcadeOnlySPGMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self._markerNames.arcadeGunMarkerName),)
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.arcadeGunMarkerName),)

    # gm_factory
    def createDualGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createExtendedArcadeMarker(self._gunMarkerType, self._markerNames.dualGunArcadeGunMarkerName),
                    gunMarkerFactory._createExtendedSniperMarker(self._gunMarkerType, self._markerNames.dualGunSniperGunMarkerName))
        return (gunMarkerFactory._createExtendedArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.dualGunArcadeGunMarkerName),
                gunMarkerFactory._createExtendedSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.dualGunSniperGunMarkerName))
