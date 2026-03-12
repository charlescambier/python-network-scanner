import subprocess
import platform
import socket
import errno

def is_host_alive(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '500', ip]
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def scan_port(ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    result = s.connect_ex((ip, port))
    
    status = "UNKNOWN"
    if result == 0:
        status = "OPEN"
    elif result in (errno.ECONNREFUSED, 111, 10061):
        status = "CLOSED"
    elif result in (errno.ETIMEDOUT, 110, 10060):
        status = "FILTERED"
    
    s.close()
    return status