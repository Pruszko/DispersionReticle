# A switch to compile few of this mod.
# Because there are no very much changes between
# them, they're merged into one file.

DISP = 0
DISP_CLIENT_SERVER = 1
CLIENT_SERVER = 2

IS_X0_6 = True

CURRENT = DISP


def isWithDispersionReticle():
    return CURRENT == DISP or \
           CURRENT == DISP_CLIENT_SERVER


def isWithServerReticle():
    return CURRENT == CLIENT_SERVER or \
           CURRENT == DISP_CLIENT_SERVER
