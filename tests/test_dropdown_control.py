import unittest
from context import data
from data import dropdown_control

multi_tier_dropdown_input = {
    "name": "TEST_NAME",
    "label": "TEST LABEL",
    "required": True,
    "filename": "some_filename",
    "parents": ["grandparent", "parent"],
    "defaults": ["$job.function.value", "300"],
}

multi_selection_dropdown_input = {
    "name": "TEST_NAME",
    "label": "TEST LABEL",
    "filename": "some_filename",
    "size": 4
}


class TestInput_Control(unittest.TestCase):

    def test_multi_tier_dropdown(self):
        """Test that class creates dropdown object with all data"""
        result = dropdown_control.Dropdown_Control(**multi_tier_dropdown_input)
        self.assertEqual(multi_tier_dropdown_input["name"], result.name)
        self.assertEqual(multi_tier_dropdown_input["label"], result.label)
        self.assertEqual(
            multi_tier_dropdown_input["filename"], result.filename)
        self.assertEqual(multi_tier_dropdown_input["parents"], result.parents)
        mapped_job_data = multi_tier_dropdown_input["defaults"][0]
        self.assertEqual(
            result.value, f'{result.job_data_map[mapped_job_data]} || "{multi_tier_dropdown_input["defaults"][1]}"')

    def test_multi_selection_dropdown(self):
        """Test that class creates dropdown object with all data"""
        result = dropdown_control.Dropdown_Control(
            **multi_selection_dropdown_input)
        self.assertEqual(multi_selection_dropdown_input["name"], result.name)
        self.assertEqual(multi_selection_dropdown_input["label"], result.label)
        self.assertEqual(
            multi_selection_dropdown_input["filename"], result.filename)


if __name__ == '__main__':
    unittest.main()
