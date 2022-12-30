import pytest
from airtrafficsim.utils.calculation import Cal
import numpy as np

def test_great_circle_dist():
    """
        Test with a online haversine distance solver
        url: https://www.vcalc.com/wiki/vCalc/Haversine%20-%20Distance
        -------
    """
    assert round(Cal.cal_great_circle_dist(10,10,20,20),2) == 1544.76
    assert isinstance(Cal.cal_great_circle_dist(10,10,20,20) , float)

def test_great_circle_bearing():
    """
        Test with a online haversine bearing (azimuth) solver
        url: https://mw.gg/gc/
        -------
    """
    assert round(Cal.cal_great_circle_bearing(10,10,20,20),1) == 42.8
    assert isinstance(Cal.cal_great_circle_bearing(10,10,20,20) , float)

def test_great_dest_given_dist_bearing():
    """
        Test with the previous results 
        url: https://mw.gg/gc/
        https://www.vcalc.com/wiki/vCalc/Haversine%20-%20Distance
        -------
    """
    assert round(Cal.cal_dest_given_dist_bearing(10,10,42.8,1544.76)[0],2) == 20.00
    assert round(Cal.cal_dest_given_dist_bearing(10,10,42.8,1544.76)[1],2) == 20.00
    assert isinstance(Cal.cal_dest_given_dist_bearing(10,10,42.8,1544.76)[0], float)
    assert isinstance(Cal.cal_dest_given_dist_bearing(10,10,42.8,1544.76)[0], float)

def test_cal_angle_diff():
    assert round(Cal.cal_angle_diff(95,270),1) == 175.00
    assert isinstance(Cal.cal_angle_diff(95,270), float)