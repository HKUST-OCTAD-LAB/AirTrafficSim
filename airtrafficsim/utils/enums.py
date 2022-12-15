from enum import IntEnum


class EngineType(IntEnum):
    """
    An enumeration for aircraft's engine type.

    Attributes
    ----------
    JET = 1
    TURBOPROP = 2
    PISTON = 3
    """
    JET = 1,
    TURBOPROP = 2,
    PISTON = 3


class WakeCat(IntEnum):
    """
    An enumeration for aircraft's wake category.

    Attributes
    ----------
    J = 1
        Jumbo
    H = 2
        Heavy
    M = 3
        Medium
    L = 4
        Light
    """
    J = 1,
    H = 2,
    M = 3,
    L = 4


class FlightPhase(IntEnum):
    """
    An enumeration for aircraft's flight phase.

    Attributes
    ----------
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
    """
    AT_GATE_ORIGIN = 1,
    TAXI_ORIGIN = 2,
    TAKEOFF = 3,
    INITIAL_CLIMB = 4,
    CLIMB = 5,
    CRUISE = 6,
    DESCENT = 7,
    APPROACH = 8,
    LANDING = 9,
    TAXI_DEST = 10,
    AT_GATE_DEST = 11


class Config(IntEnum):
    """
    An enumeration for aircraft's wing and landing gear configuration.

    Attributes
    ----------
    TAKEOFF = 1
    INITIAL_CLIMB = 2
    CLEAN = 3
    APPROACH = 4
    LANDING = 
    """
    TAKEOFF = 1,
    INITIAL_CLIMB = 2,
    CLEAN = 3,
    APPROACH = 4,
    LANDING = 5


class SpeedMode(IntEnum):
    """
    An enumeration for aircraft's actual speed mode.

    Attributes
    ----------
    CAS = 1
    MACH = 2
    """
    CAS = 1,
    MACH = 2


class VerticalMode(IntEnum):
    """
    An enumeration for aircraft's actual vertical mode.

    Attributes
    ----------
    LEVEL = 1
    CLIMB = 2
    DESCENT = 3
    """
    LEVEL = 1,
    CLIMB = 2,
    DESCENT = 3


class APSpeedMode(IntEnum):
    """
    An enumeration for aircraft's autopilot target vertical mode.

    Attributes
    ----------
    CONSTANT_MACH = 1
    CONSTANT_CAS = 2
    ACCELERATE = 3
    DECELERATE = 4
    """
    CONSTANT_MACH = 1,
    CONSTANT_CAS = 2,
    ACCELERATE = 3,
    DECELERATE = 4


class APThrottleMode(IntEnum):
    """
    An enumeration for aircraft's autopilot target throttle mode.

    Attributes
    ----------
    AUTO = 1,
    SPEED = 2
    """
    AUTO = 1,
    SPEED = 2


class APVerticalMode(IntEnum):
    """
    An enumeration for aircraft's autopilot target vertical mode.

    Attributes
    ----------
    ALT_HOLD = 1
    VS = 2
    FLC = 3
    """
    ALT_HOLD = 1,
    VS = 2,
    FLC = 3


class APLateralMode(IntEnum):
    """
    An enumeration for aircraft's autopilot target lateral mode.

    Attributes
    ----------
    HEADING = 1
    LNAV = 2
    """
    HEADING = 1,
    LNAV = 2
