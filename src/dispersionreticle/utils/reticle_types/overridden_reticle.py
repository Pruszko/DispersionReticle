from AvatarInputHandler.aih_global_binding import BINDING_ID, _Observable, _DEFAULT_VALUES
from gui.battle_control.controllers import crosshair_proxy

from dispersionreticle.utils.reticle_properties import MarkerNames
from dispersionreticle.utils.reticle_types.vanilla_reticle import VanillaReticle


class OverriddenReticle(VanillaReticle):

    NEXT_DATA_PROVIDER_ID = 6114

    def __init__(self, nameSuffix, gunMarkerType, reticleType, markerLinkagesProvider):
        nextStandardDataProviderID = OverriddenReticle.NEXT_DATA_PROVIDER_ID
        OverriddenReticle.NEXT_DATA_PROVIDER_ID += 1

        nextSpgDataProviderID = OverriddenReticle.NEXT_DATA_PROVIDER_ID
        OverriddenReticle.NEXT_DATA_PROVIDER_ID += 1

        # aih_global_binding
        BINDING_ID.RANGE += (nextStandardDataProviderID,
                             nextSpgDataProviderID)

        # aih_global_binding
        _DEFAULT_VALUES.update({
            nextStandardDataProviderID: lambda: _Observable(None),
            nextSpgDataProviderID: lambda: _Observable(None),
        })

        # crosshair_proxy
        crosshair_proxy._GUN_MARKERS_SET_IDS += (nextStandardDataProviderID,
                                                 nextSpgDataProviderID)

        super(OverriddenReticle, self).__init__(markerNames=MarkerNames.createMarkerNames(nameSuffix),
                                                gunMarkerType=gunMarkerType,
                                                reticleType=reticleType,
                                                markerLinkagesProvider=markerLinkagesProvider,
                                                standardDataProviderID=nextStandardDataProviderID,
                                                spgDataProviderID=nextSpgDataProviderID)

        self.refreshLinkages()
