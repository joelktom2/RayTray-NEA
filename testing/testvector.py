import unittest
import sys
sys.path.append("..") 
from ..Maths import Vector
#from ..RayTray - NEA\Maths.py" import Vector
from ... import Vector

class TestVectorOperations(unittest.TestCase):
    def test_add_vectors(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = v1 + v2
        self.assertEqual((result.x, result.y, result.z), (5, 7, 9))
    
    def test_subtract_vectors(self):
        v1 = Vector(7, 8, 9)
        v2 = Vector(4, 5, 6)
        result = v1 - v2
        self.assertEqual((result.x, result.y, result.z), (3, 3, 3))
    
    def test_add_with_negative_values(self):
        v1 = Vector(-1, -2, -3)
        v2 = Vector(4, 5, 6)
        result = v1 + v2
        self.assertEqual((result.x, result.y, result.z), (3, 3, 3))
    
    def test_subtract_with_negative_values(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(-4, -5, -6)
        result = v1 - v2
        self.assertEqual((result.x, result.y, result.z), (5, 7, 9))
    
    def test_add_zero_vector(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(0, 0, 0)
        result = v1 + v2
        self.assertEqual((result.x, result.y, result.z), (1, 2, 3))
    
    def test_subtract_zero_vector(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(0, 0, 0)
        result = v1 - v2
        self.assertEqual((result.x, result.y, result.z), (1, 2, 3))

if __name__ == '__main__':
    unittest.main()
