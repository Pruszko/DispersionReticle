from typing import Callable

from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS, \
    GUN_MARKER_VIEW_CONSTANTS

from dispersionreticle.settings.config_param_types import OptionsParam


class ReticleType(object):
    CLIENT = 0
    SERVER = 1


class ReticleLinkages(object):

    @staticmethod
    def greenLinkagesProvider(markerNames):
        # type: (MarkerNames) -> dict

        return {
            markerNames.arcadeGunMarkerName: _CONSTANTS.GUN_MARKER_LINKAGE,
            markerNames.sniperGunMarkerName: _CONSTANTS.GUN_MARKER_LINKAGE,
            markerNames.dualGunArcadeGunMarkerName: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
            markerNames.dualGunSniperGunMarkerName: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE,
            markerNames.spgGunMarkerName: _CONSTANTS.GUN_MARKER_SPG_LINKAGE
        }

    @staticmethod
    def purpleLinkagesProvider(markerNames):
        # type: (MarkerNames) -> dict

        return {
            markerNames.arcadeGunMarkerName: _CONSTANTS.GUN_MARKER_DEBUG_LINKAGE,
            markerNames.sniperGunMarkerName: _CONSTANTS.GUN_MARKER_DEBUG_LINKAGE,
            markerNames.dualGunArcadeGunMarkerName: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_DEBUG_LINKAGE,
            markerNames.dualGunSniperGunMarkerName: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_DEBUG_LINKAGE,
            markerNames.spgGunMarkerName: _CONSTANTS.GUN_MARKER_SPG_DEBUG_LINKAGE
        }

    @classmethod
    def createParamLinkagesProvider(cls, param):
        # type: (OptionsParam) -> Callable[[MarkerNames], dict]

        def _linkagesProvider(reticleNames):
            if param() == "purple":
                return cls.purpleLinkagesProvider(reticleNames)

            # return green anyway
            return cls.greenLinkagesProvider(reticleNames)

        return _linkagesProvider


class MarkerNames(object):

    def __init__(self, arcadeGunMarkerName, sniperGunMarkerName,
                 dualGunArcadeGunMarkerName, dualGunSniperGunMarkerName,
                 spgGunMarkerName):
        self.arcadeGunMarkerName = arcadeGunMarkerName
        self.sniperGunMarkerName = sniperGunMarkerName

        self.dualGunArcadeGunMarkerName = dualGunArcadeGunMarkerName
        self.dualGunSniperGunMarkerName = dualGunSniperGunMarkerName

        self.spgGunMarkerName = spgGunMarkerName

    def getMarkerNames(self):
        return (
            self.arcadeGunMarkerName,
            self.sniperGunMarkerName,
            self.dualGunArcadeGunMarkerName,
            self.dualGunSniperGunMarkerName,
            self.spgGunMarkerName
        )

    @staticmethod
    def createStandardMarkerNames():
        return MarkerNames(
            arcadeGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.ARCADE_GUN_MARKER_NAME,
            sniperGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.SNIPER_GUN_MARKER_NAME,
            dualGunArcadeGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME,
            dualGunSniperGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME,
            spgGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.SPG_GUN_MARKER_NAME
        )

    @staticmethod
    def createDebugMarkerNames():
        return MarkerNames(
            arcadeGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME,
            sniperGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME,
            dualGunArcadeGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME,
            dualGunSniperGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME,
            spgGunMarkerName=GUN_MARKER_VIEW_CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME
        )

    @staticmethod
    def createMarkerNames(suffix):
        return MarkerNames(
            arcadeGunMarkerName='arcadeGunMarker' + suffix,
            sniperGunMarkerName='sniperGunMarker' + suffix,
            dualGunArcadeGunMarkerName='arcadeDualGunMarker' + suffix,
            dualGunSniperGunMarkerName='sniperDualGunMarker' + suffix,
            spgGunMarkerName='spgGunMarker' + suffix
        )
