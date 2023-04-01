from AvatarInputHandler import aih_global_binding
from AvatarInputHandler.aih_global_binding import BINDING_ID, _Observable, _DEFAULT_VALUES
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory
from aih_constants import GUN_MARKER_TYPE
from gui.battle_control.controllers import crosshair_proxy
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS


class Reticle:

    NEXT_DATA_PROVIDER_ID = 6114

    def __init__(self, name, gunMarkerType, reticleType, reticleLinkages):
        self.name = name
        self.gunMarkerType = gunMarkerType
        self.reticleType = reticleType
        self.reticleLinkages = reticleLinkages

        self.standardDataProviderID = Reticle.NEXT_DATA_PROVIDER_ID
        Reticle.NEXT_DATA_PROVIDER_ID += 1
        self.spgDataProviderID = Reticle.NEXT_DATA_PROVIDER_ID
        Reticle.NEXT_DATA_PROVIDER_ID += 1

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


class ReticleType(int):
    CLIENT = 0
    SERVER = 1


class ReticleLinkages(object):
    GREEN = {
        'arcadeLinkage': _CONSTANTS.GUN_MARKER_LINKAGE,
        'sniperLinkage': _CONSTANTS.GUN_MARKER_LINKAGE,
        'dualGunArcadeLinkage': _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
        'dualGunSniperLinkage': _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE,
        'spgLinkage': _CONSTANTS.GUN_MARKER_SPG_LINKAGE
    }
    PURPLE = {
        'arcadeLinkage': _CONSTANTS.GUN_MARKER_DEBUG_LINKAGE,
        'sniperLinkage': _CONSTANTS.GUN_MARKER_DEBUG_LINKAGE,
        'dualGunArcadeLinkage': _CONSTANTS.DUAL_GUN_ARCADE_MARKER_DEBUG_LINKAGE,
        'dualGunSniperLinkage': _CONSTANTS.DUAL_GUN_SNIPER_MARKER_DEBUG_LINKAGE,
        'spgLinkage': _CONSTANTS.GUN_MARKER_SPG_DEBUG_LINKAGE
    }


class ReticleRegistry(object):

    CLIENT_FOCUS = Reticle(name="ClientFocus", gunMarkerType=3,
                           reticleType=ReticleType.CLIENT,
                           reticleLinkages=ReticleLinkages.GREEN)

    SERVER_FOCUS = Reticle(name="ServerFocus", gunMarkerType=4,
                           reticleType=ReticleType.SERVER,
                           reticleLinkages=ReticleLinkages.GREEN)

    CLIENT_LATENCY = Reticle(name="ClientLatency", gunMarkerType=5,
                             reticleType=ReticleType.CLIENT,
                             reticleLinkages=ReticleLinkages.GREEN)

    RETICLES = [CLIENT_FOCUS, SERVER_FOCUS, CLIENT_LATENCY]
