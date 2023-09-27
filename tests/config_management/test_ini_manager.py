import unittest
from unittest.mock import patch, Mock, mock_open
# Adjusted import based on your directory structure
from config_management.ini_manager import INISecretManager

class TestINISecretManager(unittest.TestCase):

    def setUp(self):
        self.ini_manager = INISecretManager()

    @patch('config_management.ini_manager.configparser.ConfigParser.read')
    @patch('config_management.ini_manager.configparser.ConfigParser.__getitem__')
    def test_get_secret_valid(self, mock_getitem, mock_read):
        # Mocking secrets.ini contents
        mock_getitem.return_value = {'KEY1': 'VALUE1'}
        
        secret = self.ini_manager.get_secret('KEY1')
        self.assertEqual(secret, 'VALUE1')

    @patch('config_management.ini_manager.configparser.ConfigParser.read')
    @patch('config_management.ini_manager.configparser.ConfigParser.__getitem__')
    def test_get_secret_invalid(self, mock_getitem, mock_read):
        # Mocking secrets.ini contents without the desired key
        mock_getitem.side_effect = KeyError

        with self.assertRaises(ValueError):
            self.ini_manager.get_secret('INVALID_KEY')

    @patch('config_management.ini_manager.configparser.ConfigParser.read')
    @patch('config_management.ini_manager.configparser.ConfigParser.__setitem__')
    @patch('config_management.ini_manager.open', new_callable=mock_open)
    def test_set_secret(self, mock_file_open, mock_setitem, mock_read):
        self.ini_manager.set_secret('NEW_KEY', 'NEW_VALUE')
        
        # Check if the correct value is set
        mock_setitem.assert_called_with('Secrets', {'NEW_KEY': 'NEW_VALUE'})

        # Check if file write has been triggered
        mock_file_open.assert_called_with('../secrets.ini', 'w')

if __name__ == '__main__':
    unittest.main()
