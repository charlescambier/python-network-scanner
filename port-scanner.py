import socket
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

target = os.getenv("TARGET_IP")
start_port = int(os.getenv("START_PORT"))
end_port = int(os.getenv("END_PORT"))

open_ports = 0  # counter

print(f"Scanning {target}...")

for port in range(start_port, end_port + 1):
    # Create a TCP IPv4 socket for network communication.
    # AF_INET → IPv4
    # SOCK_STREAM → TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # to scan IPv6, use AF_INET6, to s an UDP, use SOCK_DGRAM
    s.settimeout(0.1)

    result = s.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is OPEN")
        open_ports += 1  # increase counter

    s.close()

print("Scan complete.")
print(f"Total open ports found: {open_ports}")