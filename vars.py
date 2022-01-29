import os
import getpass
from sys import platform

SUPPORTED_EXTENSIONS = ['.mp3', '.m4a', '.flac', '.alac', '.wav']

user = getpass.getuser()

if platform == "linux" or platform == "linux2":
    # linux
    DIRS = [f'/home/{ user }/Desktop/music']
    LIBRARY_PATH = f'/home/{ user }/Music/Library'

elif platform == "darwin":
    # OS X
    DIRS = [f'/home/{ user }/Desktop/web']
    LIBRARY_PATH = f'/home/{ user }/Music/Library'

elif platform == "win32":
    # Windows
    DIRS = [f'C:\\Users\\{ user }\\Music', f'D:\\music']
    LIBRARY_PATH = f'C:\\Users\\{ user }\\Music\\Library'

COVER_PATH = os.path.join(LIBRARY_PATH, 'Covers')

DATA_PATH = os.path.join(LIBRARY_PATH, 'library.sidhu')

