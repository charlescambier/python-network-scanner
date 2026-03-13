import csv
import ipaddress
from config import load_config
from utils import is_host_alive, scan_port
from typing import Dict, List

def run_scanner() -> None:
    conf = load_config()
    
    stats: Dict[str, List[str]] = {"OPEN": [], "CLOSED": [], "FILTERED": []}
    ip_range = list(ipaddress.summarize_address_range(conf["start_addr"], conf["end_addr"]))

    print(f"{'='*50}\n Scanning...\n{'='*50}")

    try:
        with open(conf["output_file"], mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "Port", "Status"])

            for network in ip_range:
                for ip in network:
                    target = str(ip)
                    
                    if not is_host_alive(target):
                        print(f"[→] {target} is OFFLINE")
                        continue

                    print(f"[→] {target} is ONLINE (Scanning...)")

                    for port in range(conf["start_port"], conf["end_port"] + 1):
                        status: str = scan_port(target, port, conf["timeout"])
                        
                        if status in stats:
                            stats[status].append(f"{target}:{port}")
                        
                        writer.writerow([target, port, status])
                        print(f"    Port {port}: {status}")

    except PermissionError:
        print("Error : Impossible to write in CSV file.")
    
    # Résumé final
    print(f"\n{'='*50}")
    print(f"Done. Results saved in {conf['output_file']}")
    print(f"OPEN: {len(stats['OPEN'])} | CLOSED: {len(stats['CLOSED'])} | FILTERED: {len(stats['FILTERED'])}")
    print(f"{'='*50}")

if __name__ == "__main__":
    print(f"load config = {load_config()}")
    run_scanner()