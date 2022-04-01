"""Aircraft performance class unit test"""
# import unittest
import pytest
from pathlib import Path
import numpy as np

from simulation.traffic.performance.performance import Performance

# class TestPerformance(unittest.TestCase):
#     """
#     A unit test class for Performance class
#     """

#     def setUp(self):
#         """
#         Set up and initialize necessary variables for testing.
#         """
#         self.perf = Performance(1409)   # Initialize Performance class for all 1409 aircraft types in BADA 3.15
#         print(self.perf.__SYNONYM('ACCODE'))

#     def test_equal(self):
#         self.assertEqual(1,1)
        
@pytest.fixture
def perf():
    perf_low =  Performance(1409)       # Low Aircraft Mass
    perf_medium =  Performance(1409)    # Medium Aircraft Mass
    perf_high =  Performance(1409)      # High Aircraft Mass
    return perf_low, perf_medium, perf_high


def test_method(perf: Performance):
    perf_low, perf_medium, perf_high = perf
    # for aircraft in perf_low.
    # np.genfromtxt(Path('simulation/data/BADA/',file_name+'.APF'), delimiter=[6,8,9,4,4,4,3,5,4,4,4,4,3,4,4,5,4,4,4,5,7], dtype="U2,U7,U7,U2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,U6", comments="CC", autostrip=True)
    assert 1 == 1

def test_add_aircraft():
    perf = Performance(1409)
    n = 0
    for aircraft in perf._Performance__SYNONYM['ACCODE']:
        perf.add_aircraft(aircraft, n, 2)
        n += 1
    
    assert perf._Performance__v_mo != np.zeros(1409)

def test_atmosphere():
    np.genfromtxt(Path('simulation/data/BADA/',file_name+'.APF'), delimiter=[6,8,9,4,4,4,3,5,4,4,4,4,3,4,4,5,4,4,4,5,7], dtype="U2,U7,U7,U2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,U6", comments="CC", autostrip=True)