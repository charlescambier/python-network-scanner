# Python Network Scanner

Simple Python network and port scanner that:

- Loads its scan settings from a `.env` file
- Checks whether each target host is online with `ping`
- Scans a port range with TCP socket connections
- Saves all results to `scan_results.csv`

## Features

- Scan a single host or an IPv4 range
- Detect `OPEN`, `CLOSED`, and `FILTERED` ports
- Export results to CSV
- Print live progress and a final summary in the terminal

## Project Structure

```text
.
├── main.py
├── config.py
├── utils.py
├── .env
└── scan_results.csv
```

## Requirements

- Python 3.10+
- `python-dotenv`

## Installation

1. Create and activate a virtual environment if you want isolation.
2. Install the dependency:

```bash
pip install python-dotenv
```

## Configuration

The scanner reads its settings from `.env`.

Example:

```env
TARGET_IP_START=192.168.1.28
TARGET_IP_END=192.168.1.28
START_PORT=1
END_PORT=1024
TIME_OUT_AMOUNT=1
TIME_OUT_AMOUNT_PING=5
```

### Environment Variables

- `TARGET_IP_START`: First IPv4 address to scan
- `TARGET_IP_END`: Last IPv4 address to scan
- `START_PORT`: First port in the scan range
- `END_PORT`: Last port in the scan range
- `TIME_OUT_AMOUNT`: Socket timeout used for port scanning
- `TIME_OUT_AMOUNT_PING`: Present in `.env`, but not currently used by the code

## How It Works

1. `config.py` loads and validates the environment variables.
2. `main.py` builds the IP range between `TARGET_IP_START` and `TARGET_IP_END`.
3. Each host is checked with `ping`.
4. If the host is online, each port in the configured range is scanned.
5. Results are written to `scan_results.csv`.

## Run

```bash
python main.py
```

## Output

Results are saved to `scan_results.csv` with this format:

```csv
IP Address,Port,Status
192.168.1.28,21,OPEN
192.168.1.28,22,OPEN
192.168.1.28,80,CLOSED
```

Possible statuses:

- `OPEN`
- `CLOSED`
- `FILTERED`

## Notes

- Offline hosts are skipped after the ping check.
- The output file is currently fixed as `scan_results.csv`.
- The script prints the loaded configuration before starting the scan.

## Disclaimer

Use this scanner only on systems and networks you own or are authorized to test.
