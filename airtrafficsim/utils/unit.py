from numba import njit

class Unit:
    @staticmethod
    @njit()
    def kts2mps(knots):
        """Convert knots (1nm/h) to m/s"""
        return knots * 0.514444444

    @staticmethod
    @njit()
    def mps2kts(mps):
        """Convert m/s to knots (1nm/h)"""
        return mps / 0.514444444

    @staticmethod
    @njit()
    def nm2m(nm):
        """Convert nautical mile (1 minute of lat/long) to meter"""
        return nm * 1852.0

    @staticmethod
    @njit()
    def m2nm(meter):
        """Convert meter to nautical mile (1 minute of lat/long)"""
        return meter / 1852.0

    @staticmethod
    @njit()
    def ft2m(feet):
        """Convert feet to meter"""
        return feet / 3.280839895

    @staticmethod
    @njit()
    def m2ft(meter):
        """Convert meter to feet"""
        return meter * 3.280839895

    @staticmethod
    def ftpm2mps(ftpm):
        """Convert feet/min to meter/second"""
        return ftpm / 196.8503937

    @staticmethod
    @njit()
    def mps2ftpm(mps):
        """Convert meter/second to feet/min"""
        return mps * 196.8503937