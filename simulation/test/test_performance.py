"""Aircraft performance class unit test"""
import unittest
from pathlib import Path
import numpy as np

from simulation.traffic.performance import Performance

class TestPerformance(unittest.TestCase):
    """
    A unit test class for Performance class
    """

    def setUp(self):
        """
        Set up and initialize necessary variables for testing.
        """
        self.perf = Performance(1409)   # Initialize Performance class for all 1409 aircraft types in BADA 3.15
        print(self.perf.__SYNONYM('ACCODE'))

    def test_equal(self):
        self.assertEqual(1,1)
        

if __name__ == '__main__':
    unittest.main()