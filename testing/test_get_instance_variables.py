from tools.tonic_generic import get_instance_variables as get_instance_variables
from models.drink import Drink as Drink
import unittest
from unittest.mock import patch as patch, Mock as Mock

class TestGetInstanceVariables(unittest.TestCase):
    @patch("tools.tonic_generic.get_instance_variables")
    def test_add_drink_given_empty_string(self, mock_get_instance_variables):
        #Arrange
        mock_drink = Mock(Drink)
        mock_drink.name = "test_tea"
        mock_drink_list = [mock_drink]
        mock_drink = Mock(Drink)
        mock_drink.name = "test_water"
        mock_drink_list.append(mock_drink)

        #Act
        actual = get_instance_variables(mock_drink_list, "name")

        #Assert
        self.assertEqual(actual, ["test_tea", "test_water"])

if __name__ == "__main__":
    unittest.main()