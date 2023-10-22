from realm import CURRENT_REALM


class ClientType(object):
    WG = "EU"
    LESTA = "RU"


def overrideIn(cls, clientType=None, onlyWhenDebugging=False):
    from dispersionreticle.utils import debug_state

    def _overrideMethod(func):
        if onlyWhenDebugging and not debug_state.IS_DEBUGGING:
            return func

        if clientType is not None and clientType != CURRENT_REALM:
            return func

        funcName = func.__name__

        if funcName.startswith("__"):
            funcName = "_" + cls.__name__ + funcName

        old = getattr(cls, funcName)

        def wrapper(*args, **kwargs):
            return func(old, *args, **kwargs)

        setattr(cls, funcName, wrapper)
        return wrapper
    return _overrideMethod


def getClientType():
    return CURRENT_REALM


def isClientWG():
    return CURRENT_REALM == ClientType.WG


def isClientLesta():
    return CURRENT_REALM == ClientType.LESTA


# Utility decorator to add new function in certain class/module
def addMethodTo(cls, onlyWhenDebugging=False):
    from dispersionreticle.utils import debug_state

    def _overrideMethod(func):
        if onlyWhenDebugging and not debug_state.IS_DEBUGGING:
            return func

        setattr(cls, func.__name__, func)
        return func
    return _overrideMethod
