from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.utils import isClientWG


class ReticleSide(object):
    CLIENT = 0
    SERVER = 1


class ReticleLinkages(object):

    @staticmethod
    def greenLinkagesProvider(markerNames):
        # WG specific
        # handle absent marker linkages gracefully in Lesta
        twinGunArcadeGunMarkerLinkage = _CONSTANTS.TWIN_GUN_MARKER_LINKAGE if isClientWG() else None
        twinGunSniperGunMarkerLinkage = _CONSTANTS.TWIN_GUN_MARKER_LINKAGE if isClientWG() else None

        accuracyGunArcadeGunMarkerLinkage = _CONSTANTS.ACCURACY_GUN_MARKER_LINKAGE if isClientWG() else None
        accuracyGunSniperGunMarkerLinkage = _CONSTANTS.ACCURACY_GUN_MARKER_LINKAGE if isClientWG() else None

        chargeGunArcadeGunMarkerLinkage = _CONSTANTS.CHARGE_GUN_MARKER_LINKAGE if isClientWG() else None
        chargeGunSniperGunMarkerLinkage = _CONSTANTS.CHARGE_GUN_MARKER_LINKAGE if isClientWG() else None

        return {
            markerNames.arcadeGunMarkerName: _CONSTANTS.GUN_MARKER_LINKAGE,
            markerNames.sniperGunMarkerName: _CONSTANTS.GUN_MARKER_LINKAGE,
            markerNames.dualGunArcadeGunMarkerName: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_LINKAGE,
            markerNames.dualGunSniperGunMarkerName: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_LINKAGE,
            markerNames.twinGunArcadeGunMarkerName: twinGunArcadeGunMarkerLinkage,
            markerNames.twinGunSniperGunMarkerName: twinGunSniperGunMarkerLinkage,
            markerNames.accuracyGunArcadeGunMarkerName: accuracyGunArcadeGunMarkerLinkage,
            markerNames.accuracyGunSniperGunMarkerName: accuracyGunSniperGunMarkerLinkage,
            markerNames.chargeGunArcadeGunMarkerName: chargeGunArcadeGunMarkerLinkage,
            markerNames.chargeGunSniperGunMarkerName: chargeGunSniperGunMarkerLinkage,
            markerNames.spgGunMarkerName: _CONSTANTS.GUN_MARKER_SPG_LINKAGE
        }

    @staticmethod
    def purpleLinkagesProvider(markerNames):
        # WG specific
        # handle absent marker linkages gracefully in Lesta
        twinGunArcadeGunMarkerLinkage = _CONSTANTS.TWIN_GUN_MARKER_DEBUG_LINKAGE if isClientWG() else None
        twinGunSniperGunMarkerLinkage = _CONSTANTS.TWIN_GUN_MARKER_DEBUG_LINKAGE if isClientWG() else None

        accuracyGunArcadeGunMarkerLinkage = _CONSTANTS.ACCURACY_GUN_MARKER_DEBUG_LINKAGE if isClientWG() else None
        accuracyGunSniperGunMarkerLinkage = _CONSTANTS.ACCURACY_GUN_MARKER_DEBUG_LINKAGE if isClientWG() else None

        chargeGunArcadeGunMarkerLinkage = _CONSTANTS.CHARGE_GUN_MARKER_DEBUG_LINKAGE if isClientWG() else None
        chargeGunSniperGunMarkerLinkage = _CONSTANTS.CHARGE_GUN_MARKER_DEBUG_LINKAGE if isClientWG() else None

        return {
            markerNames.arcadeGunMarkerName: _CONSTANTS.GUN_MARKER_DEBUG_LINKAGE,
            markerNames.sniperGunMarkerName: _CONSTANTS.GUN_MARKER_DEBUG_LINKAGE,
            markerNames.dualGunArcadeGunMarkerName: _CONSTANTS.DUAL_GUN_ARCADE_MARKER_DEBUG_LINKAGE,
            markerNames.dualGunSniperGunMarkerName: _CONSTANTS.DUAL_GUN_SNIPER_MARKER_DEBUG_LINKAGE,
            markerNames.twinGunArcadeGunMarkerName: twinGunArcadeGunMarkerLinkage,
            markerNames.twinGunSniperGunMarkerName: twinGunSniperGunMarkerLinkage,
            markerNames.accuracyGunArcadeGunMarkerName: accuracyGunArcadeGunMarkerLinkage,
            markerNames.accuracyGunSniperGunMarkerName: accuracyGunSniperGunMarkerLinkage,
            markerNames.chargeGunArcadeGunMarkerName: chargeGunArcadeGunMarkerLinkage,
            markerNames.chargeGunSniperGunMarkerName: chargeGunSniperGunMarkerLinkage,
            markerNames.spgGunMarkerName: _CONSTANTS.GUN_MARKER_SPG_DEBUG_LINKAGE
        }

    @classmethod
    def createParamLinkagesProvider(cls, param):
        def _linkagesProvider(reticleNames):
            if param() == "purple":
                return cls.purpleLinkagesProvider(reticleNames)

            # return green anyway
            return cls.greenLinkagesProvider(reticleNames)

        return _linkagesProvider


class MarkerNames(object):

    def __init__(self, arcadeGunMarkerName, sniperGunMarkerName,
                 dualGunArcadeGunMarkerName, dualGunSniperGunMarkerName,
                 twinGunArcadeGunMarkerName, twinGunSniperGunMarkerName,
                 accuracyGunArcadeGunMarkerName, accuracyGunSniperGunMarkerName,
                 chargeGunArcadeGunMarkerName, chargeGunSniperGunMarkerName,
                 spgGunMarkerName):
        self.arcadeGunMarkerName = arcadeGunMarkerName
        self.sniperGunMarkerName = sniperGunMarkerName

        self.dualGunArcadeGunMarkerName = dualGunArcadeGunMarkerName
        self.dualGunSniperGunMarkerName = dualGunSniperGunMarkerName

        self.twinGunArcadeGunMarkerName = twinGunArcadeGunMarkerName
        self.twinGunSniperGunMarkerName = twinGunSniperGunMarkerName

        self.accuracyGunArcadeGunMarkerName = accuracyGunArcadeGunMarkerName
        self.accuracyGunSniperGunMarkerName = accuracyGunSniperGunMarkerName

        self.chargeGunArcadeGunMarkerName = chargeGunArcadeGunMarkerName
        self.chargeGunSniperGunMarkerName = chargeGunSniperGunMarkerName

        self.spgGunMarkerName = spgGunMarkerName

    def getMarkerNames(self):
        return (
            self.arcadeGunMarkerName,
            self.sniperGunMarkerName,
            self.dualGunArcadeGunMarkerName,
            self.dualGunSniperGunMarkerName,
            self.twinGunArcadeGunMarkerName,
            self.twinGunSniperGunMarkerName,
            self.accuracyGunArcadeGunMarkerName,
            self.accuracyGunSniperGunMarkerName,
            self.chargeGunArcadeGunMarkerName,
            self.chargeGunSniperGunMarkerName,
            self.spgGunMarkerName
        )

    @staticmethod
    def createStandardMarkerNames():
        # WG specific
        # handle absent marker names gracefully in Lesta
        twinGunArcadeGunMarkerName = _CONSTANTS.TWIN_GUN_ARCADE_MARKER_NAME if isClientWG() else None
        twinGunSniperGunMarkerName = _CONSTANTS.TWIN_GUN_SNIPER_MARKER_NAME if isClientWG() else None

        accuracyGunArcadeGunMarkerName = _CONSTANTS.ACCURACY_GUN_ARCADE_MARKER_NAME if isClientWG() else None
        accuracyGunSniperGunMarkerName = _CONSTANTS.ACCURACY_GUN_SNIPER_MARKER_NAME if isClientWG() else None

        chargeGunArcadeGunMarkerName = _CONSTANTS.CHARGE_GUN_ARCADE_MARKER_NAME if isClientWG() else None
        chargeGunSniperGunMarkerName = _CONSTANTS.CHARGE_GUN_SNIPER_MARKER_NAME if isClientWG() else None

        return MarkerNames(
            arcadeGunMarkerName=_CONSTANTS.ARCADE_GUN_MARKER_NAME,
            sniperGunMarkerName=_CONSTANTS.SNIPER_GUN_MARKER_NAME,
            dualGunArcadeGunMarkerName=_CONSTANTS.DUAL_GUN_ARCADE_MARKER_NAME,
            dualGunSniperGunMarkerName=_CONSTANTS.DUAL_GUN_SNIPER_MARKER_NAME,
            twinGunArcadeGunMarkerName=twinGunArcadeGunMarkerName,
            twinGunSniperGunMarkerName=twinGunSniperGunMarkerName,
            accuracyGunArcadeGunMarkerName=accuracyGunArcadeGunMarkerName,
            accuracyGunSniperGunMarkerName=accuracyGunSniperGunMarkerName,
            chargeGunArcadeGunMarkerName=chargeGunArcadeGunMarkerName,
            chargeGunSniperGunMarkerName=chargeGunSniperGunMarkerName,
            spgGunMarkerName=_CONSTANTS.SPG_GUN_MARKER_NAME
        )

    # this method is not used anywhere
    # but it feels like a waste to delete it, because it might be useful in future
    # lmao
    @staticmethod
    def createDebugMarkerNames():
        # WG specific
        # handle absent marker names gracefully in Lesta
        twinGunArcadeGunMarkerName = _CONSTANTS.DEBUG_TWIN_GUN_ARCADE_MARKER_NAME if isClientWG() else None
        twinGunSniperGunMarkerName = _CONSTANTS.DEBUG_TWIN_GUN_SNIPER_MARKER_NAME if isClientWG() else None

        accuracyGunArcadeGunMarkerName = _CONSTANTS.DEBUG_ACCURACY_GUN_ARCADE_MARKER_NAME if isClientWG() else None
        accuracyGunSniperGunMarkerName = _CONSTANTS.DEBUG_ACCURACY_GUN_SNIPER_MARKER_NAME if isClientWG() else None

        chargeGunArcadeGunMarkerName = _CONSTANTS.DEBUG_CHARGE_GUN_ARCADE_MARKER_NAME if isClientWG() else None
        chargeGunSniperGunMarkerName = _CONSTANTS.DEBUG_CHARGE_GUN_SNIPER_MARKER_NAME if isClientWG() else None

        return MarkerNames(
            arcadeGunMarkerName=_CONSTANTS.DEBUG_ARCADE_GUN_MARKER_NAME,
            sniperGunMarkerName=_CONSTANTS.DEBUG_SNIPER_GUN_MARKER_NAME,
            dualGunArcadeGunMarkerName=_CONSTANTS.DEBUG_DUAL_GUN_ARCADE_MARKER_NAME,
            dualGunSniperGunMarkerName=_CONSTANTS.DEBUG_DUAL_GUN_SNIPER_MARKER_NAME,
            twinGunArcadeGunMarkerName=twinGunArcadeGunMarkerName,
            twinGunSniperGunMarkerName=twinGunSniperGunMarkerName,
            accuracyGunArcadeGunMarkerName=accuracyGunArcadeGunMarkerName,
            accuracyGunSniperGunMarkerName=accuracyGunSniperGunMarkerName,
            chargeGunArcadeGunMarkerName=chargeGunArcadeGunMarkerName,
            chargeGunSniperGunMarkerName=chargeGunSniperGunMarkerName,
            spgGunMarkerName=_CONSTANTS.DEBUG_SPG_GUN_MARKER_NAME
        )

    @staticmethod
    def createMarkerNames(suffix):
        return MarkerNames(
            arcadeGunMarkerName='arcadeGunMarker' + suffix,
            sniperGunMarkerName='sniperGunMarker' + suffix,
            dualGunArcadeGunMarkerName='arcadeDualGunMarker' + suffix,
            dualGunSniperGunMarkerName='sniperDualGunMarker' + suffix,
            twinGunArcadeGunMarkerName='arcadeTwinGunMarker' + suffix,
            twinGunSniperGunMarkerName='sniperTwinGunMarker' + suffix,
            accuracyGunArcadeGunMarkerName='arcadeAccuracyGunMarker' + suffix,
            accuracyGunSniperGunMarkerName='sniperAccuracyGunMarker' + suffix,
            chargeGunArcadeGunMarkerName='arcadeChargeGunMarker' + suffix,
            chargeGunSniperGunMarkerName='sniperChargeGunMarker' + suffix,
            spgGunMarkerName='spgGunMarker' + suffix
        )


class ReticleType(object):

    def __init__(self, reticleId, markerNames, markerLinkagesProvider):
        self._reticleId = reticleId
        self._markerNames = markerNames
        self._markerLinkagesProvider = markerLinkagesProvider

        self.refreshLinkages()

    def refreshLinkages(self):
        reticleLinkages = self._markerLinkagesProvider(self._markerNames)

        # gm_factory
        gm_factory._GUN_MARKER_LINKAGES.update(reticleLinkages)

    @property
    def reticleId(self):
        return self._reticleId

    @property
    def markerNames(self):
        return self._markerNames

    @property
    def markerLinkagesProvider(self):
        return self._markerLinkagesProvider


class ExtendedReticleType(ReticleType):

    def __init__(self, reticleId, markerNames, markerLinkagesProvider, layerProvider):
        super(ExtendedReticleType, self).__init__(reticleId=reticleId,
                                                  markerNames=markerNames,
                                                  markerLinkagesProvider=markerLinkagesProvider)
        self._layerProvider = layerProvider
        self._flashMarkerNames = (
            self.markerNames.arcadeGunMarkerName,
            self.markerNames.sniperGunMarkerName,
            self.markerNames.dualGunArcadeGunMarkerName,
            self.markerNames.dualGunSniperGunMarkerName,
            self.markerNames.twinGunArcadeGunMarkerName,
            self.markerNames.twinGunSniperGunMarkerName,
            self.markerNames.accuracyGunArcadeGunMarkerName,
            self.markerNames.accuracyGunSniperGunMarkerName,
            self.markerNames.chargeGunArcadeGunMarkerName,
            self.markerNames.chargeGunSniperGunMarkerName,
        )

    @property
    def flashMarkerNames(self):
        return self._flashMarkerNames

    @property
    def flashLayer(self):
        return self._layerProvider()


class ReticleTypes(object):
    VANILLA = ReticleType(reticleId=1,
                          markerNames=MarkerNames.createStandardMarkerNames(),
                          markerLinkagesProvider=ReticleLinkages.greenLinkagesProvider)
    DEBUG_SERVER = ReticleType(reticleId=2,
                               markerNames=MarkerNames.createMarkerNames("DebugServer"),
                               markerLinkagesProvider=ReticleLinkages.createParamLinkagesProvider(g_configParams.serverReticleType))
    FOCUSED = ReticleType(reticleId=3,
                          markerNames=MarkerNames.createMarkerNames("Focused"),
                          markerLinkagesProvider=ReticleLinkages.createParamLinkagesProvider(g_configParams.focusedReticleType))
    HYBRID = ReticleType(reticleId=4,
                         markerNames=MarkerNames.createMarkerNames("Hybrid"),
                         markerLinkagesProvider=ReticleLinkages.createParamLinkagesProvider(g_configParams.hybridReticleType))
    FOCUSED_EXTENDED = ExtendedReticleType(reticleId=5,
                                           markerNames=MarkerNames.createMarkerNames("FocusedExtended"),
                                           markerLinkagesProvider=FOCUSED.markerLinkagesProvider,
                                           layerProvider=g_configParams.focusedReticleExtendedLayer)
    HYBRID_EXTENDED = ExtendedReticleType(reticleId=6,
                                          markerNames=MarkerNames.createMarkerNames("HybridExtended"),
                                          markerLinkagesProvider=HYBRID.markerLinkagesProvider,
                                          layerProvider=g_configParams.hybridReticleExtendedLayer)
    SERVER_EXTENDED = ExtendedReticleType(reticleId=7,
                                          markerNames=MarkerNames.createMarkerNames("ServerExtended"),
                                          markerLinkagesProvider=DEBUG_SERVER.markerLinkagesProvider,
                                          layerProvider=g_configParams.serverReticleExtendedLayer)

    OVERRIDDEN_RETICLE_TYPES = [DEBUG_SERVER, FOCUSED, HYBRID]
    EXTENDED_RETICLE_TYPES = [FOCUSED_EXTENDED, HYBRID_EXTENDED, SERVER_EXTENDED]

    ADDITIONAL_RETICLE_TYPES = OVERRIDDEN_RETICLE_TYPES + EXTENDED_RETICLE_TYPES

    ALL_RETICLE_TYPES = [VANILLA] + ADDITIONAL_RETICLE_TYPES

    # this MUST NOT return reticle type for SPGs because our SWF app cannot render it,
    # so it will be redirected to standard vanilla reticle container
    @classmethod
    def getByExtendedFlashMarkerName(cls, markerName):
        for reticleType in cls.EXTENDED_RETICLE_TYPES:
            if markerName in reticleType.flashMarkerNames:
                return reticleType

        return None
