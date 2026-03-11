import csv
from dotenv import load_dotenv
import socket
import os
import errno
import ipaddress

# Load .env file
load_dotenv()

target_ip_start = os.getenv("TARGET_IP_START")
target_ip_end = os.getenv("TARGET_IP_END")
start_port = int(os.getenv("START_PORT"))
end_port = int(os.getenv("END_PORT"))

open_ports_collection = []
closed_ports_collection = []
filtered_port_collection = []
unknown_collection = []

output_file = "scan_results.csv"

# Conversion des strings en objets IP
start_addr = ipaddress.IPv4Address(target_ip_start)
end_addr = ipaddress.IPv4Address(target_ip_end)

# Génération de la plage d'IPs via summarize_address_range
ip_range = list(ipaddress.summarize_address_range(start_addr, end_addr))

# Calcul du nombre total d'IPs pour affichage
total_ips = sum(network.num_addresses for network in ip_range)
total_ports = end_port - start_port + 1

print(f"{'='*50}")
print(f"  Scan démarré : {target_ip_start} → {target_ip_end}")
print(f"  IPs totales  : {total_ips}")
print(f"  Ports        : {start_port} → {end_port} ({total_ports} ports)")
print(f"{'='*50}")

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IP Address", "Port", "Status"])

    # Boucle sur chaque réseau/IP de la plage
    for network in ip_range:
        for ip in network:
            target = str(ip)
            print(f"\n[→] Scanning IP: {target}")

            for port in range(start_port, end_port + 1):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)

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

# Résumé final
print(f"\n{'='*50}")
print(f"  Scan terminé — Résultats sauvegardés : {output_file}")
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