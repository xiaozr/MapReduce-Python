import unittest
import pandas as pd
from mapper import mapper

class TestMapper(unittest.TestCase):

    def test_mapper_output(self):
        # Create a sample DataFrame
        test_data = pd.DataFrame({
            'quality': [5.0, 6.0, 5.0],
            'volatile acidity': [0.7, 0.6, 0.8],
            'other': [1, 2, 3]  # Extra column to simulate real data
        })

        expected_output = [
            (5.0, 0.7),
            (6.0, 0.6),
            (5.0, 0.8)
        ]

        result = mapper(test_data)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
