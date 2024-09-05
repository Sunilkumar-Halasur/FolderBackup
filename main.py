import shutil
import os
import paramiko
from datetime import datetime

def backup_folder(source_folder, backup_folder):
    # Create a timestamp for the backup file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_folder, f'backup_{timestamp}.zip')
    
    # Create a zip file of the folder
    shutil.make_archive(backup_file.replace('.zip', ''), 'zip', source_folder)
    print(f'Backup created at: {backup_file}')
    return backup_file

def upload_to_server(local_file, server_path, server_host, server_port, username, password):
    try:
        # Create an SFTP client
        transport = paramiko.Transport((server_host, server_port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Upload the backup file to the server
        sftp.put(local_file, server_path)
        print(f'File uploaded to: {server_path}')
        
        # Close the SFTP session and transport
        sftp.close()
        transport.close()
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    # Define source and backup folder paths
    source_folder = '/path/to/your/folder'  # e.g., '/home/user/mydata'
    backup_folder = '/path/to/backup/folder'  # e.g., '/home/user/backups'
    
    # Define server details
    server_host = 'your.server.com'  # e.g., '192.168.1.100'
    server_port = 22  # Default SFTP port
    username = 'your_username'  # e.g., 'user'
    password = 'your_password'  # e.g., 'password'
    server_path = '/path/on/server/backup.zip'  # e.g., '/home/user/backup.zip'
    
    # Create the backup and upload it
    backup_file = backup_folder(source_folder, backup_folder)
    upload_to_server(backup_file, server_path, server_host, server_port, username, password)
