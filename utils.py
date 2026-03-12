import subprocess
import platform
import socket
import errno

def is_host_alive(ip: str) -> bool:
    param: str = '-n' if platform.system().lower() == 'windows' else '-c'
    command: list[str] = ['ping', param, '1', '-w', '500', ip]
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def scan_port(ip: str, port: int, timeout: int) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    result: int = s.connect_ex((ip, port))
    
    status: str = "UNKNOWN"
    if result == 0:
        status = "OPEN"
    elif result in (errno.ECONNREFUSED, 111, 10061):
        status = "CLOSED"
    elif result in (errno.ETIMEDOUT, 110, 10060):
        status = "FILTERED"
    
    s.close()
    return status