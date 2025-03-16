import unittest
import os
from main import create_csv_function

class TestCSVCreation(unittest.TestCase):
    def test_create_csv_function(self):
        test_csv_filepath = 'test_output.csv'
        expected_content = "column1,column2\nvalue1,value2\n"
        
        # Call the function to create the CSV
        csv_content = create_csv_function(test_csv_filepath)
        
        # Check if the content is as expected
        self.assertEqual(csv_content, expected_content)
        
        # Clean up the test file
        if os.path.exists(test_csv_filepath):
            os.remove(test_csv_filepath)

if __name__ == '__main__':
    unittest.main()