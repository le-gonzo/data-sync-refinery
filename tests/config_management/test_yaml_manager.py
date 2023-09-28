# test_yaml_manager.py
# Run test with
# python3.6 -m unittest tests.config_management.test_yaml_manager
import warnings
import unittest
from unittest.mock import patch, mock_open
from config_management.yaml_manager import YAMLSecretManager

try:
    import yaml
except ImportError:
    warnings.warn("The pyyaml module is not installed. Some tests may not run correctly.", UserWarning)

class TestYAMLSecretManager(unittest.TestCase):

    def setUp(self):
        # Mock the content of the YAML file.
        self.mock_yaml_content = '''
Database:
  Host: 127.0.0.1
  User: root
Secrets:
  KEY1: VALUE1
'''
        self.mock_open = mock_open(read_data=self.mock_yaml_content)
        with patch('config_management.yaml_manager.open', self.mock_open):
            self.yaml_manager = YAMLSecretManager('mock_file.yaml')  # The filename doesn't matter because it's mocked.

    def test_get_valid(self):
        host = self.yaml_manager.get_secret('Database', 'Host')
        self.assertEqual(host, '127.0.0.1')

        secret = self.yaml_manager.get_secret('Secrets', 'KEY1')
        self.assertEqual(secret, 'VALUE1')

    def test_get_invalid_section(self):
        with self.assertRaises(ValueError):
            self.yaml_manager.get_secret('NonExistentSection', 'Host')

    def test_get_invalid_key(self):
        with self.assertRaises(ValueError):
            self.yaml_manager.get_secret('Database', 'NonExistentKey')

    @patch('config_management.yaml_manager.yaml.safe_dump')
    def test_set(self, mock_safe_dump):
        self.yaml_manager.set_secret('Database', 'Port', '3306')
        
        # Check if the correct value is set in the manager's config
        self.assertEqual(self.yaml_manager.config['Database']['Port'], '3306')
        
        # Check if the YAML dump method was called
        mock_safe_dump.assert_called_once()

if __name__ == '__main__':
    unittest.main()
