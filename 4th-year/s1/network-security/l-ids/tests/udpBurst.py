# udp_burst_loopback.py
from scapy.all import IP, UDP, send
for i in range(20):
    pkt = IP(src="127.0.0.1", dst="127.0.0.1")/UDP(sport=50000+i, dport=53)
    send(pkt, verbose=0)
print("sent UDP burst")

