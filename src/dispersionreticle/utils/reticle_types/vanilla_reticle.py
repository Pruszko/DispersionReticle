from AvatarInputHandler import aih_global_binding
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory
from aih_constants import GUN_MARKER_TYPE

from dispersionreticle.utils import isClientLesta
from dispersionreticle.utils.reticle_types import ReticleSide


class VanillaReticle(object):

    def __init__(self, reticleType, gunMarkerType, reticleSide,
                 standardDataProviderID, spgDataProviderID, assaultSpgDataProviderID):
        self._reticleType = reticleType
        self._gunMarkerType = gunMarkerType
        self._reticleSide = reticleSide

        self._standardDataProviderID = standardDataProviderID
        self._spgDataProviderID = spgDataProviderID
        self._assaultSpgDataProviderID = assaultSpgDataProviderID

        # gun_marker_ctrl
        # beware, those are descriptors
        self._standardDataProviderRW = aih_global_binding.bindRW(self._standardDataProviderID)
        self._spgDataProviderRW = aih_global_binding.bindRW(self._spgDataProviderID)

        # Lesta specific
        # avoid RW binding to assault data provider on WG client
        if isClientLesta():
            self._assaultSpgDataProviderRW = aih_global_binding.bindRW(self._assaultSpgDataProviderID)
        else:
            self._assaultSpgDataProviderRW = None

    @property
    def gunMarkerType(self):
        return self._gunMarkerType

    @property
    def reticleType(self):
        return self._reticleType

    @property
    def markerNames(self):
        return self._reticleType.markerNames

    def isServerReticle(self):
        return self._reticleSide == ReticleSide.SERVER

    # gun_marker_ctrl
    def getStandardDataProvider(self):
        # this is awful, but we have to do this like that
        if self._standardDataProviderRW.__get__(self) is None:
            self._standardDataProviderRW.__set__(self, _GunMarkersDPFactory._makeDefaultProvider())
        return self._standardDataProviderRW.__get__(self)

    # gun_marker_ctrl
    def getSpgDataProvider(self):
        # this is awful, but we have to do this like that
        if self._spgDataProviderRW.__get__(self) is None:
            self._spgDataProviderRW.__set__(self, _GunMarkersDPFactory._makeSPGProvider())
        return self._spgDataProviderRW.__get__(self)

    # Lesta specific
    # gun_marker_ctrl
    #
    # it won't be called on WG client
    def getAssaultSpgDataProvider(self):
        # this is awful, but we have to do this like that
        if self._assaultSpgDataProviderRW.__get__(self) is None:
            self._assaultSpgDataProviderRW.__set__(self, _GunMarkersDPFactory._makeAssaultSPGProvider())
        return self._assaultSpgDataProviderRW.__get__(self)

    # gm_factory
    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self._gunMarkerType, self.markerNames.sniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.sniperGunMarkerName))

    # gm_factory
    def createSPGMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createSPGMarker(self._gunMarkerType, self.markerNames.spgGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.spgGunMarkerName))

    # Lesta specific
    # gm_factory
    #
    # it won't be called on WG client
    def createAssaultSPGMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createAssaultSPGMarker(self._gunMarkerType, self.markerNames.spgGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createAssaultSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.spgGunMarkerName))

    # gm_factory
    def createDualGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.dualGunArcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self._gunMarkerType, self.markerNames.dualGunSniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.dualGunArcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.dualGunSniperGunMarkerName))

    # WG specific
    # it won't be called on Lesta client
    # gm_factory
    def createTwinGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.twinGunArcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self._gunMarkerType, self.markerNames.twinGunSniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.twinGunArcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.twinGunSniperGunMarkerName))

    # WG specific
    # it won't be called on Lesta client
    # gm_factory
    def createAccuracyGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.accuracyGunArcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self._gunMarkerType, self.markerNames.accuracyGunSniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.accuracyGunArcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.accuracyGunSniperGunMarkerName))

    # WG specific
    # it won't be called on Lesta client
    # gm_factory
    def createChargeGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.chargeGunArcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self._gunMarkerType, self.markerNames.chargeGunSniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.chargeGunArcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.chargeGunSniperGunMarkerName))
