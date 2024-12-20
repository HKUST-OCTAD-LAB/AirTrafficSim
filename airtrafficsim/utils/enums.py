from enum import IntEnum

# FIXME(abrah): move them into the appropriate modules.


class EngineType(IntEnum):
    """
    Aircraft engine type
    """

    JET = 1
    TURBOPROP = 2
    PISTON = 3


class WakeCat(IntEnum):
    """
    Aircraft wake category
    """

    J = 1
    """Jumbo"""
    H = 2
    """Heavy"""
    M = 3
    """Medium"""
    L = 4


class FlightPhase(IntEnum):
    """
    Aircraft flight phase
    """

    AT_GATE_ORIGIN = 1
    TAXI_ORIGIN = 2
    TAKEOFF = 3
    INITIAL_CLIMB = 4
    CLIMB = 5
    CRUISE = 6
    DESCENT = 7
    APPROACH = 8
    LANDING = 9
    TAXI_DEST = 10
    AT_GATE_DEST = 11


class Config(IntEnum):
    """
    Wing and landing gear configuration
    """

    TAKEOFF = 1
    INITIAL_CLIMB = 2
    CLEAN = 3
    APPROACH = 4
    LANDING = 5


class SpeedMode(IntEnum):
    """
    Aircraft actual speed mode
    """

    CAS = 1
    MACH = 2


class VerticalMode(IntEnum):
    """
    Aircraft actual vertical mode
    """

    LEVEL = 1
    CLIMB = 2
    DESCENT = 3


class APSpeedMode(IntEnum):
    """
    Aircraft autopilot target speed mode
    """

    CONSTANT_MACH = 1
    CONSTANT_CAS = 2
    ACCELERATE = 3
    DECELERATE = 4


class APThrottleMode(IntEnum):
    """
    Aircraft autopilot target throttle mode
    """

    AUTO = 1
    SPEED = 2


class APVerticalMode(IntEnum):
    """
    Aircraft autopilot target vertical mode
    """

    ALT_HOLD = 1
    VS = 2
    FLC = 3


class APLateralMode(IntEnum):
    """
    Aircraft Lateral Mode
    """

    HEADING = 1
    LNAV = 2
