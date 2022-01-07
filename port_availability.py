import socket


def port_availability(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((host, port))
    except socket.timeout:
        result = 1
    sock.close()
    return result != 0
