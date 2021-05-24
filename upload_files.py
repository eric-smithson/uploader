import os
import config
import paramiko
import getpass
from scp import SCPClient

def createSSHClient():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    password = config.REMOTE_PASS
    if password == '':
        password = getpass.getpass()

    client.connect(
        config.REMOTE_ADDR,
        config.REMOTE_PORT,
        config.REMOTE_USER,
        password)
    return client

ssh = createSSHClient()
scp = SCPClient(ssh.get_transport())


def upload_plex(scp):
    for folder in config.PLEX_FOLDERS:
        last_path = os.path.basename(os.path.normpath(folder))
        remote_path = f'{config.PLEX_REMOTE_BASE}/{last_path}'
        local_files = os.listdir(os.path.join(os.getcwd(), folder))
        for i, file in enumerate(local_files):
            local_files[i] = os.path.join(os.getcwd(), folder, file)
        scp.put(local_files, remote_path=remote_path, recursive=True)


def upload_next_cloud():
    pass


if __name__ == '__main__':
    upload_plex()
    upload_next_cloud()
