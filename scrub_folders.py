# cleans out all folders
import os
import config
import shutil

def clean_plex():
    for folder in config.PLEX_FOLDERS:
        for f in os.listdir(folder):
            shutil.rmtree(os.path.join(folder, f))


if __name__ == '__main__':
    clean_plex()
