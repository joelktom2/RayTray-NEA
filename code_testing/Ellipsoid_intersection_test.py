import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import math
from Maths import Vector , Ray
from objects import Ellipsoid

class TestEllipsoidIntersection(unittest.TestCase):
    def setUp(self):
        self.ellipsoid = Ellipsoid(Vector(0, 0, 0), Vector(2, 1, 1))

    def test_ray_hits_ellipsoid(self):
        ray = Ray(Vector(-3, 0, 0), Vector(1, 0, 0))
        intersection = self.ellipsoid.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, -2)

    def test_ray_misses_ellipsoid(self):
        ray = Ray(Vector(0, 3, 0), Vector(0, 1, 0))
        intersection = self.ellipsoid.intersects(ray)
        self.assertIsNone(intersection)

    def test_ray_originates_inside_ellipsoid(self):
        ray = Ray(Vector(0.5, 0, 0), Vector(1, 0, 0))
        intersection = self.ellipsoid.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertGreater(intersection.x, 0.5)

    def test_ray_tangent_to_ellipsoid(self):
        ray = Ray(Vector(2, 1, 0), Vector(0, -1, 0))
        intersection = self.ellipsoid.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.y, 0)

    def test_ray_parallel_to_axis(self):
        ray = Ray(Vector(-3, 0, 0), Vector(0, 1, 0))
        intersection = self.ellipsoid.intersects(ray)
        self.assertIsNone(intersection)

if __name__ == '__main__':
    unittest.main()
