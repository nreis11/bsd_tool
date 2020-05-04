import unittest
from context import data
from data import input_control

string_input_data = {
    "name": "TEST_NAME",
    "label": "TEST LABEL",
    "required": True,
    "maxlength": "500",
    "defaults": ["$job.education.value", "2nd TEST DEFAULT"],
    "placeholder": "This is a placeholder."
}


class TestInput_Control(unittest.TestCase):

    def test_string_input(self):
        """Test that class creates string object with all data"""
        result = input_control.Input_Control(**string_input_data)
        self.assertEqual(string_input_data["name"], result.name)
        self.assertEqual("CONTROL_TYPE_STRING", result.type)
        self.assertEqual(string_input_data["label"], result.label)
        self.assertEqual(string_input_data["maxlength"], result.maxlength)
        mapped_job_data = string_input_data["defaults"][0]
        self.assertEqual(
            result.value, f'{result.job_data_map[mapped_job_data]} || "{string_input_data["defaults"][1]}"')


if __name__ == '__main__':
    unittest.main()
