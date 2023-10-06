import os
import subprocess

from config_management.factory import get_secret_manager

class ShareDriveManager:

    secret_manager = get_secret_manager()
    
    def __init__(self, mount_point):
        self.mount_point = mount_point
        self.share_drive_path = self.secret_manager.get_secret('share_drive', 'UNC_path')
        self.auth_file_path = self.secret_manager.get_secret('share_drive', 'auth_file_path')

    
    def is_drive_mounted(self):
        # Use the mount command to check if the drive is mounted
        result = subprocess.run(['mount'], capture_output=True, text=True)
        return self.mount_point in result.stdout
    
    def _is_user_in_group(self, group_name):
        # Get the list of groups the current user is part of
        groups = subprocess.run(['groups'], capture_output=True, text=True).stdout.split()
        return group_name in groups
    
    def mount_drive(self, secrets):
        # Check if user is part of the credusers group
        if not self._is_user_in_group("credusers"):
            raise PermissionError("Current user is not part of the credusers group. Contact your system administrator.")
        
        # Get the username and password from the auth file
        try:
            with open(self.auth_file_path, 'r') as f:
                username = f.readline().strip()
                password = f.readline().strip()
        except Exception as e:
            raise PermissionError(f"Cannot access the sharedrive_auth file. Details: {e}")
        
        # Use the mount command to mount the drive
        # Assuming the share is of type cifs (Windows Share)
        cmd = [
            "sudo", "mount", "-t", "cifs", 
            "-o", f"username={username},password={password},{secrets}", 
            self.share_drive_path, self.mount_point
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to mount the drive. Error: {result.stderr}")
    
    def update_credentials(self, new_username, new_password):
        # Ensure the current user has the necessary permissions
        if not self._is_user_in_group("credusers"):
            raise PermissionError("Current user is not part of the credusers group. Contact your system administrator.")
        
        # Update the auth file with new credentials
        try:
            with open(self.auth_file_path, 'w') as f:
                f.write(new_username + "\n")
                f.write(new_password + "\n")
        except Exception as e:
            raise PermissionError(f"Cannot update the sharedrive_auth file. Details: {e}")

# Example usage
# secrets = "some_secret_parameters"
# manager = ShareDriveManager("/path/to/mount_point", "//share/drive/path")
# if not manager.is_drive_mounted():
#     manager.mount_drive(secrets)
