import logging

logger = logging.getLogger(__name__)


class DispersionReticleMod:

    @property
    def isModsSettingsApiPresent(self):
        return self.__isModsSettingsApiPresent

    def __init__(self):
        self.__isModsSettingsApiPresent = False

    def init(self):
        try:
            logger.info("Initializing DispersionReticle mod ...")

            # it is good to know from the logs which client may have problems
            # it's not obviously logged anywhere by any client, or I am just blind
            from dispersionreticle.utils import getClientType
            logger.info("Client type: %s", getClientType())

            # make sure to invoke all hooks
            import dispersionreticle.hooks
            from dispersionreticle.settings.config import g_config

            g_config.loadConfigSafely()

            self.__resolveSoftDependencies()
            if self.isModsSettingsApiPresent:
                from dispersionreticle.support import mods_settings_api_support

                mods_settings_api_support.registerSoftDependencySupport()

            logger.info("DispersionReticle mod initialized")
        except Exception as e:
            logger.error("Error occurred while initializing DispersionReticle mod", exc_info=e)

    def __resolveSoftDependencies(self):
        try:
            from gui.modsSettingsApi import g_modsSettingsApi

            # if something crashed in ModsSettingsAPI, then singleton may be None
            self.__isModsSettingsApiPresent = g_modsSettingsApi is not None

            if not self.isModsSettingsApiPresent:
                logger.warn("Error probably occurred in ModsSettingsAPI because it is None, ignore its presence.")
        except ImportError:
            self.__isModsSettingsApiPresent = False
        except Exception as e:
            logger.warn("Error occurred in ModsSettingsAPI, ignore its presence.", exc_info=e)
            self.__isModsSettingsApiPresent = False

    def fini(self):
        pass


g_dispersion_reticle_mod = DispersionReticleMod()
