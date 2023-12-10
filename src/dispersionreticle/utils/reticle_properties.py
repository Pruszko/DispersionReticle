from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS


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
