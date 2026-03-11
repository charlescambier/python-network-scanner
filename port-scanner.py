import csv
from dotenv import load_dotenv
import socket
import os
import errno
import ipaddress
import subprocess
import platform

def is_host_alive(ip):
    # Returns True if host responds to a ping, else False.
    # Determine the parameter for ping count (-n for Windows, -c for Unix)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Build the command: ping -n 1 <ip> (Windows) or ping -c 1 <ip> (Unix)
    # param: This is a variable representing a flag, most commonly -n in Windows (or -c in Linux) to specify the number of echo requests.
    #: 1 The number of echo requests to send (used in combination with param)
    # '-w': The flag for setting the timeout in milliseconds.
    # '500': The timeout value (500 milliseconds) to wait for each reply.
    command = ['ping', param, '1', '-w', '500', ip]
   
    # Run the command and hide the output
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

# Load .env file
load_dotenv()

target_ip_start = os.getenv("TARGET_IP_START")
target_ip_end = os.getenv("TARGET_IP_END")
start_port = int(os.getenv("START_PORT"))
end_port = int(os.getenv("END_PORT"))
time_out_amount = int(os.getenv("TIME_OUT_AMOUNT"))

open_ports_collection = []
closed_ports_collection = []
filtered_port_collection = []
unknown_collection = []
output_file = "scan_results.csv"

# Convert IP to String
start_addr = ipaddress.IPv4Address(target_ip_start)
end_addr = ipaddress.IPv4Address(target_ip_end)

# Generate ip rate
ip_range = list(ipaddress.summarize_address_range(start_addr, end_addr))

# Calculate total number of IPs for display
total_ips = sum(network.num_addresses for network in ip_range)
total_ports = end_port - start_port + 1

print(f"{'='*50}")
print(f"  Start scan : {target_ip_start} → {target_ip_end}")
print(f"  Total IPs   : {total_ips}")
print(f"  Ports        : {start_port} → {end_port} ({total_ports} ports)")
print(f"{'='*50}")

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IP Address", "Port", "Status"])

# Loop through each network/IP in the range
    for network in ip_range:
        for ip in network:
            target = str(ip)
            
            # --- NEW HOST DISCOVERY CHECK ---
            print(f"\n[→] Checking if {target} is online...", end=" ")
            if not is_host_alive(target):
                print("OFFLINE (Skipping)")
                continue
            
            print("ONLINE (Scanning ports...)")
            # --------------------------------

            for port in range(start_port, end_port + 1):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(time_out_amount)

                    result = s.connect_ex((target, port))
                    status = ""

                    if result == 0:
                        status = "OPEN"
                        open_ports_collection.append([target, port, status])
                        print(f"    Port {port}: ✔ OPEN")

                    if result in (errno.ECONNREFUSED, 111, 10061):
                        status = "CLOSED"
                        closed_ports_collection.append([target, port, status])
                        print(f"    Port {port}: X Closed")

                    if result in (errno.ETIMEDOUT, 110, 10060):
                        status = "FILTERED"
                        filtered_port_collection.append([target, port, status])
                        print(f"    Port {port}: ⚠ FILTERED")

                    # else:
                    #     status = f"UNKNOWN ({result})"
                    #     unknown_collection.append([target, port, status])
                    #     print(f"    Port {port}: ? {status}")
                    #     pass

                    writer.writerow([target, port, status])
                    s.close()

# Final resume
print(f"\n{'='*50}")
print(f"  Scan finished — Saved results : {output_file}")
print(f"{'='*50}")
print(f"  ✔ Open     : {len(open_ports_collection)}")
print(f"  ✘ Closed   : {len(closed_ports_collection)}")
print(f"  ⚠ Filtered : {len(filtered_port_collection)}")
print(f"  ? Unknown  : {len(unknown_collection)}")
print(f"{'='*50}")

if open_ports_collection:
    print("\n[Open ports detail]")
    for entry in open_ports_collection:
        print(f"  {entry[0]}:{entry[1]}")

if filtered_port_collection:
    print("\n[Filtered ports detail]")
    for entry in filtered_port_collection:
        print(f"  {entry[0]}:{entry[1]}")

print("\nDONE")