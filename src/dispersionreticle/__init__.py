# make sure to invoke all hooks
import dispersionreticle.hooks

from dispersionreticle.settings.config import g_config


class DispersionReticleMod:

    def __init__(self):
        pass

    def init(self):
        g_config.loadConfigSafely()
        pass

    def fini(self):
        pass


g_dispersion_reticle_mod = DispersionReticleMod()
