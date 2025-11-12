# port_scan_loopback.py
from scapy.all import IP, TCP, send
dst = "127.0.0.1"
for port in range(80, 120):   # 40 ports (tune as needed)
    pkt = IP(src="127.0.0.1", dst=dst)/TCP(sport=60000+port, dport=port, flags="S")
    send(pkt, verbose=0)
print("sent local port scan (80-119)")

