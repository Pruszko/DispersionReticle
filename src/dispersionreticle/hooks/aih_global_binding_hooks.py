from AvatarInputHandler import aih_global_binding

from dispersionreticle.utils import overrideIn
from dispersionreticle.utils.debug_state import g_debugStateCollector


###########################################################
# aih_global_binding hooks purely for debugging purposes
#
# Because AvatarInputHandler clears all binding subscriptions on battle completion
# we would have lost subscriptions for debugging purposes
#
# Here, after subscription erasure, we would resubscribe again for bindings changes
###########################################################

@overrideIn(aih_global_binding, onlyWhenDebugging=True)
def clear(func):
    func()

    g_debugStateCollector.subscribeAihGlobalBindings()
