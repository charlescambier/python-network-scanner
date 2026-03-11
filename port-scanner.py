import csv  # 1. Import the csv module
from dotenv import load_dotenv
import socket
import os
import errno

# Load .env file
load_dotenv()

# target = os.getenv("TARGET_IP")
target_ip_start = os.getenv("TARGET_IP_START")
target_ip_end = os.getenv("TARGET_IP_END")
start_port = int(os.getenv("START_PORT"))
end_port = int(os.getenv("END_PORT"))

open_ports = 0 
open_ports_collection= []

closed_ports = 0
closed_ports_collection = []

filtered_port = 0
filtered_port_collection = []

output_file = "scan_results.csv" # Define your filename

# print(f"Scanning {target}...")

# 2. Open the file in 'write' mode
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # 3. Write the header row
    writer.writerow(["IP Address", "Port", "Status"])

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)

        result = s.connect_ex((target, port))
        # print(port, result)

        if result == 0:
            print(f"Port {port} is OPEN")
            # 4. Write the data row to the CSV

            #check if the port is open
            writer.writerow([target, port, "OPEN"]) #write in file
            open_ports += 1
            open_ports_collection.append([target, port, "OPEN"]) #rec in collection


            #check if the port is closed
        elif result in (errno.ECONNREFUSED, 111,10061):
            print(f"Port {port} is CLOSED")
            writer.writerow([target, port, "CLOSED"])
            closed_ports += 1
            closed_ports_collection.append([target, port, "CLOSED"])


            #check if the port is filtered
        elif result in (errno.ETIMEDOUT, 110,10060):
            print(f"Port {port} is FILTERED")
            writer.writerow([target, port, "FILTERED"])
            filtered_port += 1
            filtered_port_collection.append([target, port, "FILTERED"])


        else:
            print(f"Port {port} UNKNOWN ({result})")
            writer.writerow([target, port, f"UNKNOWN ({result})"])



        s.close()

print("-" * 20)
print(f"Scan complete. Results saved to {output_file}")
print(f"Total open ports found: {open_ports}")
print(f"Total closed ports found: {closed_ports}")
print(f"Total filtered ports found: {filtered_port}")
print("*" *50)
print(f"Open ports collection: {open_ports_collection}")
print("*" *25)
print(f"Closed collection: {closed_ports_collection}")
print("*" *25)
print(f"Filtered collection: {filtered_port_collection}")
print("DONE     " *10)