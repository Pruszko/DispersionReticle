from AvatarInputHandler import aih_global_binding
from AvatarInputHandler.aih_global_binding import BINDING_ID, _Observable, _DEFAULT_VALUES
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory
from aih_constants import GUN_MARKER_TYPE
from gui.battle_control.controllers import crosshair_proxy
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory

from dispersionreticle.utils.reticle_properties import ReticleType


class VanillaReticle(object):

    NEXT_DATA_PROVIDER_ID = 6114

    def __init__(self, name, gunMarkerType, reticleType, reticleLinkages):
        self.name = name
        self.gunMarkerType = gunMarkerType
        self.reticleType = reticleType
        self.reticleLinkages = reticleLinkages

        self.standardDataProviderID = VanillaReticle.NEXT_DATA_PROVIDER_ID
        VanillaReticle.NEXT_DATA_PROVIDER_ID += 1
        self.spgDataProviderID = VanillaReticle.NEXT_DATA_PROVIDER_ID
        VanillaReticle.NEXT_DATA_PROVIDER_ID += 1

        # aih_global_binding
        BINDING_ID.RANGE += (self.standardDataProviderID,
                             self.spgDataProviderID)

        # aih_global_binding
        _DEFAULT_VALUES.update({
            self.standardDataProviderID: lambda: _Observable(None),
            self.spgDataProviderID: lambda: _Observable(None),
        })

        # crosshair_proxy
        crosshair_proxy._GUN_MARKERS_SET_IDS += (self.standardDataProviderID,
                                                 self.spgDataProviderID)

        # gun_marker_ctrl
        # beware, those are descriptors
        self.standardDataProviderRW = aih_global_binding.bindRW(self.standardDataProviderID)
        self.spgDataProviderRW = aih_global_binding.bindRW(self.spgDataProviderID)

        # gm_factory
        self.arcadeGunMarkerName = 'arcadeGunMarker' + name
        self.sniperGunMarkerName = 'sniperGunMarker' + name
        self.dualGunArcadeGunMarkerName = 'arcadeDualGunMarker' + name
        self.dualGunSniperGunMarkerName = 'sniperDualGunMarker' + name
        self.spgGunMarkerName = 'spgGunMarker' + name

        # gm_factory
        gm_factory._GUN_MARKER_LINKAGES.update({
            self.arcadeGunMarkerName: reticleLinkages['arcadeLinkage'],
            self.sniperGunMarkerName: reticleLinkages['sniperLinkage'],
            self.dualGunArcadeGunMarkerName: reticleLinkages['dualGunArcadeLinkage'],
            self.dualGunSniperGunMarkerName: reticleLinkages['dualGunSniperLinkage'],
            self.spgGunMarkerName: reticleLinkages['spgLinkage']
        })

    def getMarkerNames(self):
        return (
            self.arcadeGunMarkerName,
            self.sniperGunMarkerName,
            self.dualGunArcadeGunMarkerName,
            self.dualGunSniperGunMarkerName,
            self.spgGunMarkerName
        )

    def getFlashMarkerNames(self):
        return ()

    def isServerReticle(self):
        return self.reticleType == ReticleType.SERVER

    # gun_marker_ctrl
    def getStandardDataProvider(self):
        # this is awful, but we have to do this like that
        if self.standardDataProviderRW.__get__(self) is None:
            self.standardDataProviderRW.__set__(self, _GunMarkersDPFactory._makeDefaultProvider())
        return self.standardDataProviderRW.__get__(self)

    # gun_marker_ctrl
    def getSpgDataProvider(self):
        # this is awful, but we have to do this like that
        if self.spgDataProviderRW.__get__(self) is None:
            self.spgDataProviderRW.__set__(self, _GunMarkersDPFactory._makeSPGProvider())
        return self.spgDataProviderRW.__get__(self)

    # gm_factory
    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self.gunMarkerType, self.arcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self.gunMarkerType, self.sniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.arcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.sniperGunMarkerName))

    # gm_factory
    def createSPGMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self.gunMarkerType, self.arcadeGunMarkerName),
                    gunMarkerFactory._createSPGMarker(self.gunMarkerType, self.spgGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.arcadeGunMarkerName),
                gunMarkerFactory._createSPGMarker(GUN_MARKER_TYPE.UNDEFINED, self.spgGunMarkerName))

    # gm_factory
    def createDualGunMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (gunMarkerFactory._createArcadeMarker(self.gunMarkerType, self.dualGunArcadeGunMarkerName),
                    gunMarkerFactory._createSniperMarker(self.gunMarkerType, self.dualGunSniperGunMarkerName))
        return (gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.dualGunArcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.dualGunSniperGunMarkerName))
