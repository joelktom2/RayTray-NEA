import unittest
from scene import Vector


class TestVector(unittest.TestCase):
    def test_add(self):
        x = Vector(1,2,3)
        y = Vector(4,5,6)
        z = x + y
        print(z)
        self.assertEqual(z.x, getattr(Vector(5,7,9), ""), 'The add function failed')
        self.assertEqual(z.y, Vector(5,7,9), 'The add function failed')
        self.assertEqual(z.z, Vector(5,7,9), 'The add function failed')

if __name__ == '__main__':
    unittest.main()