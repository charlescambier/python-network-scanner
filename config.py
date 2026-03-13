import os
import ipaddress
from dotenv import load_dotenv


def load_config() -> dict[str, int | ipaddress.IPv4Address | str]:
    load_dotenv()
    try:
        config = {
            "start_port": int(os.getenv("START_PORT")),
            "end_port": int(os.getenv("END_PORT")),
            "timeout": int(os.getenv("TIME_OUT_AMOUNT")),
            "start_addr": ipaddress.IPv4Address(os.getenv("TARGET_IP_START")),
            "end_addr": ipaddress.IPv4Address(os.getenv("TARGET_IP_END")),
            "output_file": "scan_results.csv"
        }

        if config["start_port"] > config["end_port"]:
            raise ValueError("START_PORT > END_PORT")
            
        return config

    except (TypeError, ValueError, ipaddress.AddressValueError) as e:
        print(f" CONFIGURATION ERROR: {e}")
        exit(1)