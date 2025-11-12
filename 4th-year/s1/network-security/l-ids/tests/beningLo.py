# benign_loopback.py
from scapy.all import IP, TCP, send
for i in range(5):
    pkt = IP(src="127.0.0.1", dst="127.0.0.1")/TCP(sport=50000+i, dport=8080, flags="PA")
    send(pkt, verbose=0)
print("sent benign packets")

