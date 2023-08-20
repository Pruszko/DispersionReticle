import logging

logger = logging.getLogger(__name__)


class DispersionReticleMod:

    @property
    def isModsSettingsApiPresent(self):
        return self.__isModsSettingsApiPresent

    def __init__(self):
        self.__isModsSettingsApiPresent = False

    def init(self):
        # make sure to invoke all hooks
        import dispersionreticle.hooks
        from dispersionreticle.settings.config import g_config

        g_config.loadConfigSafely()

        self.__resolveSoftDependencies()
        if self.isModsSettingsApiPresent:
            from dispersionreticle.support import mods_settings_api_support

            mods_settings_api_support.registerSoftDependencySupport()

    def __resolveSoftDependencies(self):
        try:
            from gui.modsSettingsApi import g_modsSettingsApi
            self.__isModsSettingsApiPresent = True
        except ImportError:
            self.__isModsSettingsApiPresent = False
        except Exception as e:
            logger.warn("Error occurred in ModsSettingsAPI, ignore its presence.", exc_info=e)
            self.__isModsSettingsApiPresent = False

    def fini(self):
        pass


g_dispersion_reticle_mod = DispersionReticleMod()
