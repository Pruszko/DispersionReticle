from AvatarInputHandler.aih_global_binding import BINDING_ID, _Observable, _DEFAULT_VALUES
from gui.battle_control.controllers import crosshair_proxy

from dispersionreticle.utils import isClientLesta
from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle


class OverriddenReticle(VanillaReticle):

    NEXT_DATA_PROVIDER_ID = 6114

    def __init__(self, reticleType, gunMarkerType, reticleSide):
        nextStandardDataProviderID = OverriddenReticle.NEXT_DATA_PROVIDER_ID
        OverriddenReticle.NEXT_DATA_PROVIDER_ID += 1

        nextSpgDataProviderID = OverriddenReticle.NEXT_DATA_PROVIDER_ID
        OverriddenReticle.NEXT_DATA_PROVIDER_ID += 1

        # Lesta specific
        # we can safely generate next data provider ID and pass it to super class
        # superclass is ready to ignore it on WG client
        nextAssaultSpgDataProviderID = OverriddenReticle.NEXT_DATA_PROVIDER_ID
        OverriddenReticle.NEXT_DATA_PROVIDER_ID += 1

        # aih_global_binding
        BINDING_ID.RANGE += (nextStandardDataProviderID,
                             nextSpgDataProviderID)

        # Lesta specific
        if isClientLesta():
            BINDING_ID.RANGE += (nextAssaultSpgDataProviderID,)

        # aih_global_binding
        _DEFAULT_VALUES.update({
            nextStandardDataProviderID: lambda: _Observable(None),
            nextSpgDataProviderID: lambda: _Observable(None),
        })

        # Lesta specific
        if isClientLesta():
            _DEFAULT_VALUES.update({
                nextAssaultSpgDataProviderID: lambda: _Observable(None)
            })

        # crosshair_proxy
        crosshair_proxy._GUN_MARKERS_SET_IDS += (nextStandardDataProviderID,
                                                 nextSpgDataProviderID)

        # Lesta specific
        if isClientLesta():
            crosshair_proxy._GUN_MARKERS_SET_IDS += (nextAssaultSpgDataProviderID,)

        super(OverriddenReticle, self).__init__(reticleType=reticleType,
                                                gunMarkerType=gunMarkerType,
                                                reticleSide=reticleSide,
                                                standardDataProviderID=nextStandardDataProviderID,
                                                spgDataProviderID=nextSpgDataProviderID,
                                                assaultSpgDataProviderID=nextAssaultSpgDataProviderID)  # Lesta specific
