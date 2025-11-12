# syn_burst_loopback.py
from scapy.all import IP, TCP, send
for i in range(30):               # 30 SYNs -> likely trigger
    pkt = IP(src="127.0.0.1", dst="127.0.0.1")/TCP(sport=40000+i, dport=80, flags="S")
    send(pkt, verbose=0)
print("sent syn burst")

