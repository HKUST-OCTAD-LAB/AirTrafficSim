from ..types import ArrayOrFloat


# FIXME(abrah): get rid of staticmethod.
class Unit:
    @staticmethod
    def kts2mps(knots: ArrayOrFloat) -> ArrayOrFloat:
        """Convert knots (1nm/h) to m/s"""
        return knots * 0.514444444

    @staticmethod
    def mps2kts(mps: ArrayOrFloat) -> ArrayOrFloat:
        """Convert m/s to knots (1nm/h)"""
        return mps / 0.514444444

    @staticmethod
    def nm2m(nm: ArrayOrFloat) -> ArrayOrFloat:
        """Convert nautical mile (1 minute of lat/long) to meter"""
        return nm * 1852.0

    @staticmethod
    def m2nm(meter: ArrayOrFloat) -> ArrayOrFloat:
        """Convert meter to nautical mile (1 minute of lat/long)"""
        return meter / 1852.0

    @staticmethod
    def ft2m(feet: ArrayOrFloat) -> ArrayOrFloat:
        """Convert feet to meter"""
        return feet / 3.280839895

    @staticmethod
    def m2ft(meter: ArrayOrFloat) -> ArrayOrFloat:
        """Convert meter to feet"""
        return meter * 3.280839895

    @staticmethod
    def ftpm2mps(ftpm: ArrayOrFloat) -> ArrayOrFloat:
        """Convert feet/min to meter/second"""
        return ftpm / 196.8503937

    @staticmethod
    def mps2ftpm(mps: ArrayOrFloat) -> ArrayOrFloat:
        """Convert meter/second to feet/min"""
        return mps * 196.8503937
