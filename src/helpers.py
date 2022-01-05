import socket
from config import test_url, test_port

def check_connection(url: str, port: int) -> bool:
    try:
        try_socket = socket.create_connection((url, port))
        try_socket.settimeout(2)
        try_socket.close()
        
        return True
    except TimeoutError:
        raise TimeoutError(f"Connection timed out on {url}")
    except OSError:
        raise OSError(f"Could not connect to socket! Do you have internet connection? url: {test_url} on port: {test_port}")
    except:
        return False


