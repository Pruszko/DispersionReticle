# Utility decorator to override function in certain class/module
def overrideIn(cls):
    def _overrideMethod(func):
        funcName = func.__name__

        if funcName.startswith("__"):
            funcName = "_" + cls.__name__ + funcName

        old = getattr(cls, funcName)

        def wrapper(*args, **kwargs):
            return func(old, *args, **kwargs)

        setattr(cls, funcName, wrapper)
        return wrapper
    return _overrideMethod


# Utility decorator to add new function in certain class/module
def addMethodTo(cls):
    def _overrideMethod(func):
        setattr(cls, func.__name__, func)
        return func
    return _overrideMethod
