class Unit_conversion:
    """
    A utility class for converting unit
    """

    @staticmethod
    def knots_to_mps(knots):
        """Convert knots (1nm/h) to m/s"""
        return knots * 0.514444444

    @staticmethod
    def mps_to_knots(mps):
        """Convert m/s to knots (1nm/h)"""
        return mps * 0.514444444

    @staticmethod
    def nm_to_meter(nm):
        """Convert nautical mile (1 minute of lat/long) to meter"""
        return nm * 1852.0

    @staticmethod
    def meter_to_nm(meter):
        """Convert meter to nautical mile (1 minute of lat/long)"""
        return meter / 1852.0

    @staticmethod
    def feet_to_meter(feet):
        """Convert feet to meter"""
        return feet / 3.280839895

    @staticmethod
    def meter_to_feet(meter):
        """Convert meter to feet"""
        return meter * 3.280839895

    @staticmethod
    def ftpm_to_mps(ftpm):
        """Convert feet/min to meter/second"""
        return ftpm / 196.8503937

    @staticmethod
    def mps_to_ftpm(mps):
        """Convert meter/second to feet/min"""
        return mps * 196.8503937