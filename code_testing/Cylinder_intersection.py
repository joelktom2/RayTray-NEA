import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from Maths import Vector, Ray
from objects import Cylinder

class TestCylinderIntersection(unittest.TestCase):
    def setUp(self):
        self.cylinder = Cylinder(Vector(0, 0, 0), 'z', 4, 1)

    def test_ray_hits_cylinder_side(self):
        ray = Ray(Vector(2, 0, 0), Vector(-1, 0, 0))
        intersection = self.cylinder.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1)

    def test_ray_misses_cylinder(self):
        ray = Ray(Vector(3, 3, 0), Vector(1, 1, 0).norm())
        intersection = self.cylinder.intersects(ray)
        self.assertIsNone(intersection)

    def test_ray_intersects_cylinder_cap(self):
        ray = Ray(Vector(0, 0, 3), Vector(0, 0, -1))
        intersection = self.cylinder.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.z, 2)

    def test_ray_parallel_to_cylinder_axis(self):
        ray = Ray(Vector(0.5, 0, -3), Vector(0, 0, 1))
        intersection = self.cylinder.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.z, 2)

    def test_ray_originates_inside_cylinder(self):
        ray = Ray(Vector(0, 0, 0), Vector(1, 0, 0))
        intersection = self.cylinder.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1)

if __name__ == '__main__':
    unittest.main()
