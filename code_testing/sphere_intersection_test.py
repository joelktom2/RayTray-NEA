import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from Maths import Vector
from Maths import Ray
from objects import Sphere,Cone


class TestSphereIntersection(unittest.TestCase):
    def setUp(self):
        self.sphere = Sphere(Vector(0, 0, 0), 5)  # Sphere at origin with radius 5

    def test_ray_hits_sphere_twice(self):
        ray = Ray(Vector(-10, 0, 0), Vector(1, 0, 0))  # Moving towards sphere
        intersection = self.sphere.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, -5, places=6)
        self.assertAlmostEqual(intersection.y, 0, places=6)
        self.assertAlmostEqual(intersection.z, 0, places=6)

    def test_ray_hits_sphere_once_tangent(self):
        ray = Ray(Vector(0, 5, -10), Vector(0, 0, 1))  # Tangent hit
        intersection = self.sphere.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 0, places=6)
        self.assertAlmostEqual(intersection.y, 5, places=6)
        self.assertAlmostEqual(intersection.z, 0, places=6)

    def test_ray_misses_sphere(self):
        ray = Ray(Vector(0, 6, -10), Vector(0, 0, 1))  # Moving parallel above sphere
        intersection = self.sphere.intersects(ray)
        self.assertIsNone(intersection)

    def test_ray_starts_inside_sphere(self):
        ray = Ray(Vector(0, 0, 0), Vector(1, 0, 0))  # Inside sphere, moving outward
        intersection = self.sphere.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 5, places=6)
        self.assertAlmostEqual(intersection.y, 0, places=6)
        self.assertAlmostEqual(intersection.z, 0, places=6)

    def test_ray_originates_on_sphere_surface(self):
        ray = Ray(Vector(5, 0, 0), Vector(1, 0, 0))  # Starts on surface, moving outward
        intersection = self.sphere.intersects(ray)
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 5, places=6)
        self.assertAlmostEqual(intersection.y, 0, places=6)
        self.assertAlmostEqual(intersection.z, 0, places=6)

if __name__ == "__main__":
    unittest.main()


