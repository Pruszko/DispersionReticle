from AvatarInputHandler.aih_global_binding import BINDING_ID

from dispersionreticle.settings.config_param import g_configParams
from dispersionreticle.utils import isClientLesta
from dispersionreticle.utils.reticle_types import ReticleSide, ReticleTypes
from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle
from dispersionreticle.utils.reticle_types.extended_reticle import ExtendedReticle
from dispersionreticle.utils.reticle_types.overridden_reticle import OverriddenReticle


# Lesta specific
# avoid accessing Lesta bindings on WG client
# also, reticle classes are prepared to ignore them in such case
if isClientLesta():
    clientAssaultSpgDataProviderID = BINDING_ID.CLIENT_ASSAULT_SPG_GUN_MARKER_DATA_PROVIDER
    serverAssaultSpgDataProviderID = BINDING_ID.SERVER_ASSAULT_SPG_GUN_MARKER_DATA_PROVIDER
else:
    clientAssaultSpgDataProviderID = None
    serverAssaultSpgDataProviderID = None


# Relations between reticles, reticle types, gun marker types, gun marker names, marker linkages and data providers are:
# - each reticle type has one or two reticles (gun marker type): client and/or server ones
# - each gun marker type has one data provider
# - client and server gun marker types of one reticle type have one shared set of gun marker names (in vanilla game)
# - each gun marker name is bound to one marker linkage
# - marker linkage can be used multiple times and determines properties of vanilla reticle
#
# For us, there must be 2 reticles (or at least one client-side) for each reticle type (one gun marker names set),
# because vanilla reticles does this trick:
# - when we start auto-aiming, vanilla server reticle (if "Use server aim" is checked) becomes client reticle
#     but still uses same gun marker names
#     in result, it "inherits" server reticle markers, without recreating it
# - vanilla simple _DevControlMarkersFactory (the one displaying both client and server reticles) violates this
#     by assigning its one set of gun marker names to client reticle
#     and use separate gun marker names for vanilla server reticle
#     but this results in server reticle being destroyed/created on auto-aiming
#     due to gunMarkerFlag.serverMode becoming False
#     which is undesirable for us
#     this also causes server reticle to be placed on top of standard reticles, making it harder to read
#
# We don't want to destroy/create markers for several reasons (written at the end)
# so to avoid this, following code contract is made:
# - all server reticles (vanilla or our custom ones) must have client reticle counterpart
#     and become those client reticles on auto-aiming by sharing same gun marker names
#     so when auto-aiming (gunMarkerFlags.serverMode becomes False), they will "inherit" those gun markers
#     from server reticle, without recreating it
#     this is done by _DispersionControlMarkersFactory and DispersionGunMarkersDecorator
# - all necessary reticle instances selected in config MUST be present all the time
#     to maintain exact rendering order, even if gunMarkerFlags.serverMode becomes False to avoid destroying them
# - when config is changed, all markers MUST be fully destroyed and created again in our defined rendering order
# - standard gun marker invalidation process MUST NOT be changed
#     but also MUST result in unchanged gun markers set (at least for reticles that are important for us)
#
# Marker destroy/create approach has several drawbacks:
# - (noticeable, unfixable) when playing Czech light tanks, yellow cross marker would be temporarily displayed
#     on marker creation with alpha 1.0
#     and we CANNOT fix this, because WG.CrosshairFlash has its script object (BW::ScriptObject)
#     inside BigWorld engine and that yellow cross marker fading logic is somewhere there, inaccessible
#     if we try to instantly fade its alpha externally (by using DAAPI's MovieClip and accessing it via public props)
#     then BW::ScriptObject for some reason loses control over it, resulting in absent yellow marker permanently
# - (big, awkward to fix) when auto-aiming is finished, server reticle would be destroyed, created,
#     and by this placed on top of client reticles, making them harder to read
# - (small, partially fixable) when aiming at vehicle and clicking auto-aim, penetration indicator becomes red
#     it is fixable by invalidating its cache, but will still result in one rendering frame of invalid state
# - (small, unfixable) when auto-aiming, full destroy/create of markers would blink for one rendering frame
#     because during one frame they wouldn't be present yet
# - (small, unfixable) game rarely randomly invalidates gun marker set (saw that sometimes, but don't know the reason)
#     which would result in random destroy/create of markers what can be perceived as blinking reticle

class ReticleRegistry(object):

    # used only as reference
    VANILLA_CLIENT = VanillaReticle(reticleType=ReticleTypes.VANILLA, gunMarkerType=1,
                                    reticleSide=ReticleSide.CLIENT,
                                    standardDataProviderID=BINDING_ID.CLIENT_GUN_MARKER_DATA_PROVIDER,
                                    spgDataProviderID=BINDING_ID.CLIENT_SPG_GUN_MARKER_DATA_PROVIDER,
                                    assaultSpgDataProviderID=clientAssaultSpgDataProviderID)  # Lesta specific

    VANILLA_SERVER = VanillaReticle(reticleType=ReticleTypes.VANILLA, gunMarkerType=2,
                                    reticleSide=ReticleSide.SERVER,
                                    standardDataProviderID=BINDING_ID.SERVER_GUN_MARKER_DATA_PROVIDER,
                                    spgDataProviderID=BINDING_ID.SERVER_SPG_GUN_MARKER_DATA_PROVIDER,
                                    assaultSpgDataProviderID=serverAssaultSpgDataProviderID)  # Lesta specific

    # purposely not using DUAL_ACC here because it's ... special
    # we don't need it anyway

    # purposely declare separate server reticle to simplify linkage changes
    # otherwise, if VANILLA_SERVER were altered to debug linkages, then "Use server aim"
    # from in-game settings would be purple (it should be always green)
    #
    # by this, we also have better control over rendering order
    DEBUG_CLIENT = OverriddenReticle(reticleType=ReticleTypes.DEBUG_SERVER, gunMarkerType=4,
                                     reticleSide=ReticleSide.CLIENT)

    DEBUG_SERVER = OverriddenReticle(reticleType=ReticleTypes.DEBUG_SERVER, gunMarkerType=5,
                                     reticleSide=ReticleSide.SERVER)

    FOCUSED_CLIENT = OverriddenReticle(reticleType=ReticleTypes.FOCUSED, gunMarkerType=6,
                                       reticleSide=ReticleSide.CLIENT)

    FOCUSED_SERVER = OverriddenReticle(reticleType=ReticleTypes.FOCUSED, gunMarkerType=7,
                                       reticleSide=ReticleSide.SERVER)

    HYBRID_CLIENT = OverriddenReticle(reticleType=ReticleTypes.HYBRID, gunMarkerType=8,
                                      reticleSide=ReticleSide.CLIENT)

    FOCUSED_EXTENDED_CLIENT = ExtendedReticle(reticleType=ReticleTypes.FOCUSED_EXTENDED, gunMarkerType=9,
                                              reticleSide=ReticleSide.CLIENT)

    FOCUSED_EXTENDED_SERVER = ExtendedReticle(reticleType=ReticleTypes.FOCUSED_EXTENDED, gunMarkerType=10,
                                              reticleSide=ReticleSide.SERVER)

    HYBRID_EXTENDED_CLIENT = ExtendedReticle(reticleType=ReticleTypes.HYBRID_EXTENDED, gunMarkerType=11,
                                             reticleSide=ReticleSide.CLIENT)

    # I know it sounds dumb, but it is client/server "server-reticle-extended", so ...
    SERVER_EXTENDED_CLIENT = ExtendedReticle(reticleType=ReticleTypes.SERVER_EXTENDED, gunMarkerType=12,
                                             reticleSide=ReticleSide.CLIENT)

    SERVER_EXTENDED_SERVER = ExtendedReticle(reticleType=ReticleTypes.SERVER_EXTENDED, gunMarkerType=13,
                                             reticleSide=ReticleSide.SERVER)

    OVERRIDDEN_RETICLES = [DEBUG_CLIENT, DEBUG_SERVER, FOCUSED_CLIENT, FOCUSED_SERVER, HYBRID_CLIENT]

    EXTENDED_RETICLES = [FOCUSED_EXTENDED_CLIENT, FOCUSED_EXTENDED_SERVER, HYBRID_EXTENDED_CLIENT,
                         SERVER_EXTENDED_CLIENT, SERVER_EXTENDED_SERVER]

    ADDITIONAL_RETICLES = OVERRIDDEN_RETICLES + EXTENDED_RETICLES

    ALL_SERVER_RETICLES = [DEBUG_CLIENT, DEBUG_SERVER,
                           SERVER_EXTENDED_CLIENT, SERVER_EXTENDED_SERVER]

    ALL_RETICLES = [VANILLA_CLIENT, VANILLA_SERVER] + ADDITIONAL_RETICLES

    @classmethod
    def isAnyServerReticle(cls, gunMarkerType):
        for reticle in cls.ALL_SERVER_RETICLES:
            if reticle.gunMarkerType == gunMarkerType:
                return True

        return False

    @classmethod
    def getReticleSizeMultiplierFor(cls, gunMarkerType):
        if g_configParams.reticleSizeScaleOnlyServerReticles():
            if cls.isAnyServerReticle(gunMarkerType=gunMarkerType):
                return g_configParams.reticleSizeMultiplier()
            else:
                return 1.0
        else:
            return g_configParams.reticleSizeMultiplier()
