import unittest
import sys
sys.path.append("..") 
#from ..Maths import Vector
#from ..RayTray - NEA\Maths.py" import Vector
from RayTrayNEA.Maths import Vector

class TestVectorOperations(unittest.TestCase):


    def test_vector_addition(self):
        # Positive + Positive
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result1 = v1 + v2
        self.assertEqual(result1.x, 5)
        self.assertEqual(result1.y, 7)
        self.assertEqual(result1.z, 9)

        # Positive + Negative
        v3 = Vector(1, 2, 3)
        v4 = Vector(-4, -5, -6)
        result2 = v3 + v4
        self.assertEqual(result2.x, -3)
        self.assertEqual(result2.y, -3)
        self.assertEqual(result2.z, -3)

        # Negative + Negative
        v5 = Vector(-1, -2, -3)
        v6 = Vector(-4, -5, -6)
        result3 = v5 + v6
        self.assertEqual(result3.x, -5)
        self.assertEqual(result3.y, -7)
        self.assertEqual(result3.z, -9)

    def test_vector_subtraction(self):
        # Positive - Positive
        v1 = Vector(4, 5, 6)
        v2 = Vector(1, 2, 3)
        result1 = v1 - v2
        self.assertEqual(result1.x, 3)
        self.assertEqual(result1.y, 3)
        self.assertEqual(result1.z, 3)

        # Positive - Negative
        v3 = Vector(4, 5, 6)
        v4 = Vector(-1, -2, -3)
        result2 = v3 - v4
        self.assertEqual(result2.x, 5)
        self.assertEqual(result2.y, 7)
        self.assertEqual(result2.z, 9)

        # Negative - Negative
        v5 = Vector(-4, -5, -6)
        v6 = Vector(-1, -2, -3)
        result3 = v5 - v6
        self.assertEqual(result3.x, -3)
        self.assertEqual(result3.y, -3)
        self.assertEqual(result3.z, -3)

    def test_vector_multiplication(self):
        # Positive vector * Positive scalar
        v1 = Vector(2, 3, 4)
        result1 = v1 * 2
        self.assertEqual(result1.x, 4)
        self.assertEqual(result1.y, 6)
        self.assertEqual(result1.z, 8)

        # Positive vector * Negative scalar
        result2 = v1 * (-2)
        self.assertEqual(result2.x, -4)
        self.assertEqual(result2.y, -6)
        self.assertEqual(result2.z, -8)

        # Negative vector * Positive scalar
        v2 = Vector(-2, -3, -4)
        result3 = v2 * 2
        self.assertEqual(result3.x, -4)
        self.assertEqual(result3.y, -6)
        self.assertEqual(result3.z, -8)

        # Negative vector * Negative scalar
        result4 = v2 * (-2)
        self.assertEqual(result4.x, 4)
        self.assertEqual(result4.y, 6)
        self.assertEqual(result4.z, 8)

    def test_vector_division(self):
        # Positive vector / Positive scalar
        v1 = Vector(4, 6, 8)
        result1 = v1 / 2
        self.assertEqual(result1.x, 2)
        self.assertEqual(result1.y, 3)
        self.assertEqual(result1.z, 4)

        # Positive vector / Negative scalar
        result2 = v1 / (-2)
        self.assertEqual(result2.x, -2)
        self.assertEqual(result2.y, -3)
        self.assertEqual(result2.z, -4)

        # Negative vector / Positive scalar
        v2 = Vector(-4, -6, -8)
        result3 = v2 / 2
        self.assertEqual(result3.x, -2)
        self.assertEqual(result3.y, -3)
        self.assertEqual(result3.z, -4)

        # Negative vector / Negative scalar
        result4 = v2 / (-2)
        self.assertEqual(result4.x, 2)
        self.assertEqual(result4.y, 3)
        self.assertEqual(result4.z, 4)

    def test_dot_product(self):
        v1 = Vector(1, -2, 3)
        v2 = Vector(-4, 5, -6)
        result = v1.dp(v2)
        self.assertEqual(result, -32)
        
        # Test perpendicular vectors
        v3 = Vector(1, 0, 0)
        v4 = Vector(0, 1, 0)
        self.assertEqual(v3.dp(v4), 0)

    def test_cross_product(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        result1 = v1.cp(v2)
        result2 = v2.cp(v1)
        self.assertEqual(result1.x, 0)
        self.assertEqual(result1.y, 0)
        self.assertEqual(result1.z, 1)
        self.assertEqual(result2.x, 0)
        self.assertEqual(result2.y, 0)
        self.assertEqual(result2.z, -1)

        # Test with negative values
        v3 = Vector(-2, 3, -4)
        v4 = Vector(1, -2, 3)
        result3 = v3.cp(v4)
        self.assertEqual(result3.x, 1)
        self.assertEqual(result3.y, 2)
        self.assertEqual(result3.z, 1)

    def test_magnitude(self):
        v1 = Vector(3, -4, 0)
        v2 = Vector(-1, -2, -2)
        self.assertEqual(v1.mag(), 5)
        self.assertAlmostEqual(v2.mag(), 3)

    def test_normalize(self):
        v1 = Vector(3, -4, 0)
        normalized1 = v1.norm()
        self.assertAlmostEqual(normalized1.x, 0.6)
        self.assertAlmostEqual(normalized1.y, -0.8)
        self.assertAlmostEqual(normalized1.z, 0)
        self.assertAlmostEqual(normalized1.mag(), 1.0)

        v2 = Vector(-2, -2, -1)
        normalized2 = v2.norm()
        self.assertAlmostEqual(normalized2.mag(), 1.0)
        self.assertAlmostEqual(normalized2.x, -2/3)
        self.assertAlmostEqual(normalized2.y, -2/3)
        self.assertAlmostEqual(normalized2.z, -1/3)

    def test_vector_negation(self):
        v = Vector(1, -2, 3)
        result = -v
        self.assertEqual(result.x, -1)
        self.assertEqual(result.y, 2)
        self.assertEqual(result.z, -3)

    def test_vector_equality(self):
        v1 = Vector(1, -2, 3)
        v2 = Vector(1, -2, 3)
        v3 = Vector(1, -2, 3.000001)
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)

if __name__ == '__main__':
    unittest.main()
