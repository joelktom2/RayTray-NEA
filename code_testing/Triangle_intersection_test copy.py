import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import math
from Maths import Vector, Ray
from objects import Triangle

class TestTriangleIntersection(unittest.TestCase):

    def setUp(self):
        #basic triangle on XY plane
        self.v0 = Vector(0, 0, 0)
        self.v1 = Vector(1, 0, 0)
        self.v2 = Vector(0, 1, 0)
        self.triangle = Triangle(self.v0, self.v1, self.v2)

    def test_ray_hits_triangle_center(self):
        ray_origin = Vector(0.25, 0.25, -1)
        ray_direction = Vector(0, 0, 1).norm()
        ray = Ray(ray_origin, ray_direction)

        intersection = self.triangle.intersects(ray)
        expected_point = Vector(0.25, 0.25, 0)

        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, expected_point.x, places=6)
        self.assertAlmostEqual(intersection.y, expected_point.y, places=6)
        self.assertAlmostEqual(intersection.z, expected_point.z, places=6)

    def test_ray_misses_triangle(self):
        ray_origin = Vector(1.5, 1.5, -1)
        ray_direction = Vector(0, 0, 1).norm()
        ray = Ray(ray_origin, ray_direction)

        intersection = self.triangle.intersects(ray)
        self.assertIsNone(intersection)

    def test_ray_parallel_to_triangle(self):
        ray_origin = Vector(0.25, 0.25, 1)
        ray_direction = Vector(1, 0, 0).norm()
        ray = Ray(ray_origin, ray_direction)

        intersection = self.triangle.intersects(ray)
        self.assertIsNone(intersection)

    def test_ray_behind_triangle(self):
        ray_origin = Vector(0.25, 0.25, 1)
        ray_direction = Vector(0, 0, 1).norm() 
        ray = Ray(ray_origin, ray_direction)

        intersection = self.triangle.intersects(ray)
        self.assertIsNone(intersection)

if __name__ == "__main__":
    unittest.main()
