class Unit_conversion:
    """
    A utility class for converting unit
    """

    def knots_to_mps(knots):
        """Convert knots (1nm/h) to m/s"""
        return knots * 1852.0/3600.0

    def mps_to_knots(mps):
        """Convert m/s to knots (1nm/h)"""
        return mps * 3600.0/1852.0

    def nm_to_meter(nm):
        """Convert nautical mile (1 minute of lat/long) to meter"""
        return nm * 1852.0

    def meter_to_nm(meter):
        """Convert meter to nautical mile (1 minute of lat/long)"""
        return meter / 1852.0

    def feet_to_meter(feet):
        """Convert feet to meter"""
        return feet / 3.2808

    def meter_to_feet(meter):
        """Convert meter to feet"""
        return meter * 3.2808