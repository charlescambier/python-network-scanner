import socket

target = "127.0.0.1"  # localhost
start_port = 1
end_port = 1024

open_ports = 0  # counter

print(f"Scanning {target}...")

for port in range(start_port, end_port + 1):
    # Create a TCP IPv4 socket for network communication.
    # AF_INET → IPv4
    # SOCK_STREAM → TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # to scan IPv6, use AF_INET6, to s an UDP, use SOCK_DGRAM
    s.settimeout(0.01)

    result = s.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is OPEN")
        open_ports += 1  # increase counter

    s.close()

print("Scan complete.")
print(f"Total open ports found: {open_ports}")