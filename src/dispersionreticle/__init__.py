import logging

logger = logging.getLogger(__name__)


class DispersionReticleMod(object):

    @property
    def isModsSettingsApiPresent(self):
        return self.__isModsSettingsApiPresent

    def __init__(self):
        self.__isModsSettingsApiPresent = False

    def init(self):
        # try-except with logged exception here is more than important, because
        # when mod is initialized and some incompatibility occurs, it may break this (or other) mods
        # mainly because:
        # - AttributeError is silently ignored by mod loading code
        #   what can lead to very weird "lack of errors" where game state is corrupted
        #   due to unexpected module loading errors
        # - other exceptions may basically break loading of other mods
        #
        # by this, at least we will see what is broken
        try:
            logger.info("Initializing DispersionReticle mod ...")

            # it is good to know from the logs which client may have compatibility problems
            # it's not obviously logged anywhere by any client, or I am just blind
            from dispersionreticle.utils import getClientType
            logger.info("Client type: %s", getClientType())

            # load translations as early as possible
            from dispersionreticle.settings import translations
            translations.loadTranslations()

            # make sure to invoke all hooks
            import dispersionreticle.hooks

            # handle all soft dependencies
            self.__resolveSoftDependenciesSafely()
            if self.isModsSettingsApiPresent:
                from dispersionreticle.support import mods_settings_api_support

                mods_settings_api_support.registerSoftDependencySupport()

            # load config
            from dispersionreticle.settings.config import g_config
            g_config.reloadSafely()

            logger.info("DispersionReticle mod initialized")
        except Exception:
            logger.error("Error occurred while initializing DispersionReticle mod", exc_info=True)

            from dispersionreticle.utils import displayDialog
            displayDialog("Error occurred while initializing DispersionReticle mod.\n"
                          "Contact mod developer with error logs for further support.")

    def __resolveSoftDependenciesSafely(self):
        try:
            from gui.modsSettingsApi import g_modsSettingsApi

            # if something crashed in ModsSettingsAPI, then singleton may be None
            self.__isModsSettingsApiPresent = g_modsSettingsApi is not None

            if not self.isModsSettingsApiPresent:
                logger.warn("Error probably occurred in ModsSettingsAPI because it is None, ignore its presence.")
        except ImportError:
            self.__isModsSettingsApiPresent = False
        except Exception:
            logger.warn("Error occurred in ModsSettingsAPI, ignore its presence.", exc_info=True)
            self.__isModsSettingsApiPresent = False

    def fini(self):
        pass


g_dispersion_reticle_mod = DispersionReticleMod()
