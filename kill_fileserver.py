import urllib.error
from urllib.request import urlopen
from start_fileserver import KILL_SERVER_COMMAND


def kill_fileserver(host='127.0.0.1', port=1984):
    try:
        urlopen(f'http://{ host }:{ port }/{ KILL_SERVER_COMMAND }')
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass
