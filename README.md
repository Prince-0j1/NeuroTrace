<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=190&color=0:07111f,45:123b62,100:19c6d2&text=NEUROTRACE&fontColor=ffffff&fontSize=54&fontAlignY=38&desc=Network%20Packet%20Analysis%20%7C%20CodeAlpha%20Cyber%20Security&descAlignY=60&descSize=14" width="100%" alt="NeuroTrace banner" />






See beyond the packets.
A lightweight, browser-based network packet viewer built with Python, Scapy, and Flask.

Features · How it works · Installation · Testing · Safety

</div>

◈ What is NeuroTrace?

NeuroTrace captures packets visible to a selected network interface and presents useful packet metadata in a local web dashboard. It is designed as a learning project for understanding network communication, protocol layers, and basic traffic inspection.

Project context: Developed for Task 1 — Basic Network Sniffer, as part of the CodeAlpha Cyber Security Internship.

✦ Features

Capability

What it does

Live capture

Captures packets using Scapy on a selected interface (or the default interface).

Packet metadata

Displays timestamp, source/destination IP, protocol, ports, length, and summary when available.

BPF filtering

Supports a capture filter such as tcp, udp, or icmp.

Capture controls

Start, stop, and clear the in-memory packet list.

CSV export

Download captured metadata as packetscope_capture.csv.

Local dashboard

Flask interface bound to 127.0.0.1:5001.

🧭 How it works

flowchart TD
    A[Authorized network interface] --> B[Scapy capture loop]
    B --> C[Packet layer inspection]
    C --> D[Extract IP / protocol / ports / length]
    D --> E[In-memory packet list]
    E --> F[Flask dashboard]
    E --> G[CSV export]

Scapy listens on the chosen interface.

Each captured packet is inspected for supported layers such as IPv4/IPv6, TCP, UDP, ICMP, and DNS.

The app converts available details into a compact record.

The dashboard displays records and can export them to CSV.

🖥️ Getting started

Requirements

Python 3.10 or newer recommended.

Windows: Npcap installed; run the terminal with the permissions required for packet capture.

Linux/macOS: packet-capture permissions and libpcap support may be required.

Capture only traffic you own or are explicitly authorized to inspect.

Windows quick start

git clone https://github.com/<your-username>/NeuroTrace.git
cd NeuroTrace
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py

Or double-click run_windows.bat (it creates .venv, installs requirements, and starts the app).

Open http://127.0.0.1:5001.

Linux / macOS

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py

The included run_linux_mac.sh is also available; execute it with chmod +x run_linux_mac.sh first if needed.

🧪 Quick test

Start NeuroTrace and open the dashboard.

Leave the interface and BPF filter blank for an initial test.

Start capture, then generate ordinary traffic in another terminal (for example, ping 1.1.1.1, if ICMP is permitted) or browse to a site.

Confirm packet rows appear; stop capture and export CSV.

Try a BPF filter such as icmp and generate matching traffic.

Expected result: captured packet metadata appears in the table and the CSV contains the displayed records. A quiet interface, incorrect interface selection, missing permissions, firewall/network restrictions, or a restrictive filter can result in no visible packets.

📁 Project structure

NeuroTrace/
├── app.py                 # Flask routes and Scapy capture worker
├── requirements.txt       # Flask and Scapy dependencies
├── run_windows.bat        # Windows setup and launch helper
├── run_linux_mac.sh       # Linux/macOS setup and launch helper
└── templates/
    ├── base.html          # Shared dashboard layout and styling
    └── index.html         # Capture controls and packet table

⚙️ Configuration notes

Default local URL: http://127.0.0.1:5001

The interface field may be left blank to use Scapy's default interface.

BPF filters are applied at capture time; invalid filters can prevent capture from starting.

Packet records are held in memory for the running process. Export important results before stopping the application.

⚠️ Scope & limitations

NeuroTrace is a learning-oriented packet metadata viewer, not a full protocol dissector or forensic suite.

HTTPS/TLS application data is encrypted; this tool does not decrypt it or reveal passwords.

Capture visibility depends on the selected interface, OS, permissions, network topology, and adapter capabilities. It does not automatically see every device's traffic on a switched network.

Packet capture may expose sensitive information. Use only in an authorized lab or network and handle exports securely.

🧑‍💻 Built for learning

Topics explored: packet capture, protocol identification, IP addressing, TCP/UDP ports, BPF filters, and traffic metadata analysis.

<div align="center">

NEUROTRACE · Observe responsibly. Understand deeply.

<sub>CodeAlpha Cyber Security Internship · Basic Network Sniffer</sub>

</div>
