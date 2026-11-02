# CodeAlpha — Basic Network Sniffer (PacketScope)

A local Flask dashboard that captures packet metadata using Scapy, shows source/destination IPs, protocols, ports, lengths and summaries, and exports CSV. It follows the internship task's core requirements while avoiding unnecessary payload collection.

## Requirements
- Python 3.10+
- `pip install -r requirements.txt`
- Windows: install **Npcap** from its official site. Capture may require an Administrator terminal. Linux: run with appropriate packet-capture capabilities/root.

## Run
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5001`.

## Use responsibly
Only capture traffic on your own machine/network or where you have explicit permission. Avoid collecting payloads or credentials. The app binds to localhost and retains up to 1,500 packet metadata rows in memory. CSV export contains metadata only.

## Troubleshooting
- `Scapy is not installed`: activate the environment and run `pip install -r requirements.txt`.
- No packets: verify Npcap, permissions, interface name, and BPF syntax. Try leaving interface/filter blank.
- Filter error: use valid BPF syntax such as `tcp`, `udp port 53`, or `host 192.168.1.10`.

## Project limitations
This is a packet metadata analyzer, not a full Wireshark replacement. Encrypted application payloads cannot generally be read as plaintext. Capture stopping may wait until another packet arrives on quiet interfaces.
