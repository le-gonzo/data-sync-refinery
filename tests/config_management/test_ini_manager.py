import unittest
from unittest.mock import patch, mock_open
from config_management.ini_manager import INISecretManager
import configparser

class TestINISecretManager(unittest.TestCase):

    def setUp(self):
        # Create a real configparser object that doesn't read from the file system.
        self.mock_config = configparser.ConfigParser()
        self.ini_manager = INISecretManager()
        self.ini_manager.config = self.mock_config  # Replace the instance's config with our mock one

    def test_get_secret_valid(self):
        self.mock_config.read_string('[Secrets]\nKEY1=VALUE1\n')
        secret = self.ini_manager.get_secret('KEY1')
        self.assertEqual(secret, 'VALUE1')

    def test_get_secret_invalid(self):
        with self.assertRaises(ValueError):
            self.ini_manager.get_secret('INVALID_KEY')

    @patch('config_management.ini_manager.open', new_callable=mock_open)
    def test_set_secret(self, mock_file_open):
        self.ini_manager.set_secret('NEW_KEY', 'NEW_VALUE')
        
        # Check if the correct value is set
        self.assertEqual(self.mock_config['Secrets']['NEW_KEY'], 'NEW_VALUE')

        # Check if file write has been triggered
        mock_file_open.assert_called_with('../secrets.ini', 'w')

if __name__ == '__main__':
    unittest.main()
