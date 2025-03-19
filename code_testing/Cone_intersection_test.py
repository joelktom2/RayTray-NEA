import sys
import os
import unittest
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Maths import Vector, Ray
from objects import Cone


class TestConeIntersection(unittest.TestCase):
    def setUp(self):
        self.cone = Cone(Vector(0, 0, 0), Vector(0, 1, 0), math.radians(45))  # Cone with 45-degree angle, axis along Y

    def test_ray_hits_cone_twice(self):
        ray = Ray(Vector(1, -5, 0), Vector(0, 1, 0))  # Moving upward through cone
        intersection = self.cone.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertTrue(intersection.y > 0)

    def test_ray_hits_cone_once_tangent(self):
        ray = Ray(Vector(1, 0, 0), Vector(0, 1, 1).norm())  # Tangent ray along cone surface
        intersection = self.cone.intersects(ray)
        self.assertIsNone(intersection)

    def test_ray_hits_cone(self):
        ray = Ray(Vector(10, 0, 0), Vector(0, 1, 0))  # Far from cone
        intersection = self.cone.intersects(ray)
        self.assertIsNotNone(intersection)

    def test_ray_starts_inside_cone(self):
        ray = Ray(Vector(0, 0.5, 0), Vector(0, 1, 0))  # Inside cone, moving upward
        intersection = self.cone.intersects(ray)
        self.assertIsNone(intersection)

    def test_ray_originates_on_cone_surface(self):
        ray = Ray(Vector(1, 1, 0), Vector(0, 1, 0))  # On surface, moving along axis
        intersection = self.cone.intersects(ray)
        self.assertIsNotNone(intersection)

if __name__ == "__main__":
    unittest.main()
