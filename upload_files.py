import os
import config
import paramiko
import getpass
import time
import shutil
from scp import SCPClient

class Timer():
    start_time = None
    last_time = None
    last_sent = None

# Good ol' copy and paste from stack overflow: https://stackoverflow.com/a/49361727
def format_bytes(size, decimal_places):
    # 2**10 = 1024
    power = float(2**10)
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    size = float(size)
    while size > power:
        size /= power
        n += 1
    size = round(size, decimal_places)
    return f'{size} {power_labels[n]+"B"}'

def progress_callback(filename, size, sent):
    elapsed = "{:.2f} s".format(time.time() - Timer.start_time)
    sent_delta = sent - Timer.last_sent

    size_str = format_bytes(size, 3)
    sent_str = format_bytes(sent, 3)

    if Timer.last_time:
        time_delta = time.time() - Timer.last_time
        upload_rate = format_bytes(sent_delta / time_delta, 2) + '/s'
    else:
        upload_rate = 0
    progress_percent = "{:.3%}".format(sent/size)

    print(f'{filename}\nsize: {size_str}, sent: {sent_str}, progress: {progress_percent}, elapsed: {elapsed}, upload_rate: {upload_rate}')
    Timer.last_sent = sent
    Timer.last_time = time.time()

def createSSHClient():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {config.REMOTE_USER}@{config.REMOTE_ADDR}:{config.REMOTE_PORT}...')
    client.connect(
        config.REMOTE_ADDR,
        config.REMOTE_PORT,
        config.REMOTE_USER,
        compress=True,
    )
    print('Done.')
    return client

ssh = createSSHClient()
scp = SCPClient(ssh.get_transport(), buff_size=4194304, socket_timeout=10000.0, progress=progress_callback)


def upload_plex():
    for folder in config.PLEX_FOLDERS:
        last_path = os.path.basename(os.path.normpath(folder))
        remote_path = f'{config.PLEX_REMOTE_BASE}/{last_path}'
        local_files = os.listdir(os.path.join(os.getcwd(), folder))
        for i, file in enumerate(local_files):
            local_files[i] = os.path.join(os.getcwd(), folder, file)

        for file in local_files:
            print(f'Uploading {file}...')
            Timer.start_time = time.time()
            Timer.last_sent = 0
            scp.put(file, remote_path=remote_path, recursive=True)
            print(f'Deleting {file}...')
            try:
                shutil.rmtree(file)
            except NotADirectoryError:
                os.remove(file)
            except:
                print(f'ERROR: Could not remove {file}. Continuing...')



def upload_next_cloud():
    pass


if __name__ == '__main__':
    upload_plex()
    upload_next_cloud()
