import csv  # 1. Import the csv module
from dotenv import load_dotenv
import socket
import os

# Load .env file
load_dotenv()

target = os.getenv("TARGET_IP")
start_port = int(os.getenv("START_PORT"))
end_port = int(os.getenv("END_PORT"))

open_ports = 0 
output_file = "scan_results.csv" # Define your filename

print(f"Scanning {target}...")

# 2. Open the file in 'write' mode
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # 3. Write the header row
    writer.writerow(["IP Address", "Port", "Status"])

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)

        result = s.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} is OPEN")
            # 4. Write the data row to the CSV
            writer.writerow([target, port, "OPEN"])
            open_ports += 1

        s.close()

print("-" * 20)
print(f"Scan complete. Results saved to {output_file}")
print(f"Total open ports found: {open_ports}")