import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import math
from Maths import Vector
from light import light
from image import colour
# Test cases for the light class


class TestLightIntensity(unittest.TestCase):
    def setUp(self):
        self.light = light(Vector(0, 0, 0),colour(1,1,1))  # Initialize a light source at the origin with white color

    def test_intensity_at_point(self):
        point = Vector(1, 0, 0)
        expected_intensity = self.light.intesity / (0.01 * (1**2) + 0.1 * 1 + 1)
        actual_intensity = self.light.intensity_at_point(point)
        self.assertAlmostEqual(actual_intensity, expected_intensity, places=5)

    def test_intensity_at_different_distance(self):
        point = Vector(2, 0, 0)
        expected_intensity = self.light.intesity / (0.01 * (2**2) + 0.1 * 2 + 1)
        actual_intensity = self.light.intensity_at_point(point)
        self.assertAlmostEqual(actual_intensity, expected_intensity, places=5)

    def test_intensity_at_zero_distance(self):
        point = Vector(0, 0, 0)
        expected_intensity = 1.0
        actual_intensity = self.light.intensity_at_point(point)
        self.assertEqual(actual_intensity, expected_intensity)


if __name__ == "__main__":
    unittest.main()
