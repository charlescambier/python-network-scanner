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

try:
    # Fetching strings from .env
    raw_start_ip = os.getenv("TARGET_IP_START")
    raw_end_ip = os.getenv("TARGET_IP_END")
    raw_start_port = os.getenv("START_PORT")
    raw_end_port = os.getenv("END_PORT")
    raw_timeout = os.getenv("TIME_OUT_AMOUNT")

    # TYPE VALIDATION: Converting to Integers
    # If raw_start_port is "abc" or None, int() will raise a ValueError
    start_port = int(raw_start_port)
    end_port = int(raw_end_port)
    time_out_amount = int(raw_timeout)

    # FORMAT VALIDATION: Converting to IP Objects
    # If raw_start_ip is "10.0.0.256" (invalid), this raises AddressValueError
    start_addr = ipaddress.IPv4Address(raw_start_ip)
    end_addr = ipaddress.IPv4Address(raw_end_ip)

    # LOGIC VALIDATION
    if not (0 <= start_port <= 65535) or not (0 <= end_port <= 65535):
        raise ValueError("TCP ports must be in the range 0-65535.")
    if start_port > end_port:
        raise ValueError(f"Start port ({start_port}) cannot be higher than end port ({end_port})")
    
except TypeError:
    # This happens if a variable is missing from .env (NoneType)
    print("ERROR: One or more variables are missing from your .env file.")
    exit()
except ValueError as e:
    # This happens if the data is the wrong type (e.g., 'abc' instead of 80)
    print(f"ERROR: Invalid data type in .env: {e}")
    exit()
except ipaddress.AddressValueError as e:
    # This happens if the IP address is malformed
    print(f"ERROR: Invalid IP address format: {e}")
    exit()

open_ports_collection = []
closed_ports_collection = []
filtered_port_collection = []
unknown_collection = []
output_file = "scan_results.csv"

# Generate ip rate
ip_range = list(ipaddress.summarize_address_range(start_addr, end_addr))

# Calculate total number of IPs for display
total_ips = sum(network.num_addresses for network in ip_range)
total_ports = end_port - start_port + 1

print(f"{'='*50}")
print(f"  Total IPs   : {total_ips}")
print(f"  Ports        : {start_port} → {end_port} ({total_ports} ports)")
print(f"{'='*50}")


try:

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
                        
except PermissionError:
    print(f"ERROR: Could not write to {output_file}. Close the file if it is open in another program.")
except Exception as e:
    print(f"An unexpected error occurred during the scan: {e}")


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