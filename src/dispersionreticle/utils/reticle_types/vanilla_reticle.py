from typing import Callable

from AvatarInputHandler import aih_global_binding
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory
from aih_constants import GUN_MARKER_TYPE
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory

from dispersionreticle.utils.reticle_properties import MarkerNames, ReticleType


class VanillaReticle(object):

    _gunMarkerType = None  # type: int
    _reticleType = None  # type: int

    _markerNames = None  # type: MarkerNames
    _markerLinkagesProvider = None  # type: Callable[[MarkerNames], dict]

    _standardDataProviderID = None  # type: int
    _spgDataProviderID = None  # type: int

    def __init__(self, markerNames, gunMarkerType,
                 reticleType,
                 markerLinkagesProvider,
                 standardDataProviderID, spgDataProviderID):
        self._markerNames = markerNames
        self._gunMarkerType = gunMarkerType

        self._reticleType = reticleType
        self._markerLinkagesProvider = markerLinkagesProvider

        self.refreshLinkages()

        self._standardDataProviderID = standardDataProviderID
        self._spgDataProviderID = spgDataProviderID

        # gun_marker_ctrl
        # beware, those are descriptors
        self._standardDataProviderRW = aih_global_binding.bindRW(self._standardDataProviderID)
        self._spgDataProviderRW = aih_global_binding.bindRW(self._spgDataProviderID)

    def refreshLinkages(self):
        reticleLinkages = self._markerLinkagesProvider(self._markerNames)

        # gm_factory
        gm_factory._GUN_MARKER_LINKAGES.update(reticleLinkages)

    def getGunMarkerType(self):
        return self._gunMarkerType

    def getMarkerNames(self):
        return self._markerNames.getMarkerNames()

    def getMarkerLinkagesProvider(self):
        return self._markerLinkagesProvider

    def getFlashMarkerNames(self):
        return ()

    def isServerReticle(self):
        return self._reticleType == ReticleType.SERVER

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

    # gm_factory
    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self._markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self._gunMarkerType, self._markerNames.sniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.sniperGunMarkerName))

    # gm_factory
    def createSPGMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self._markerNames.arcadeGunMarkerName),
                    gunMarkerFactory._createSPGMarker(self._gunMarkerType, self._markerNames.spgGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.spgGunMarkerName))

    # gm_factory
    def createDualGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self._markerNames.dualGunArcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self._gunMarkerType, self._markerNames.dualGunSniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.dualGunArcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self._markerNames.dualGunSniperGunMarkerName))
