import os
import config


if __name__ == '__main__':
    os.getcwd()
    for folder in config.PLEX_FOLDERS:
        path = os.path.join(os.getcwd(), folder)
        if not os.path.exists(path):
            os.makedirs(path)
