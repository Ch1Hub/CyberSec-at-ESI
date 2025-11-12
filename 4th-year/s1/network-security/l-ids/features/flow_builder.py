# features/flow_builder.py
import time

flows = {}

def get_flow_key(pkt):
    if not pkt.haslayer("IP"):
        return None
    ip = pkt["IP"]
    proto_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
    proto = proto_map.get(ip.proto, str(ip.proto))
    sport = 0
    dport = 0
    if pkt.haslayer("TCP"):
        sport = pkt["TCP"].sport
        dport = pkt["TCP"].dport
        proto = "TCP"
    elif pkt.haslayer("UDP"):
        sport = pkt["UDP"].sport
        dport = pkt["UDP"].dport
        proto = "UDP"
    return (ip.src, ip.dst, proto, int(sport), int(dport))

def new_flow(ts):
    return {
        "start": ts,
        "end": ts,
        "pkts": 0,
        "bytes": 0,
        "syns": 0,
        "dst_ports": set()
    }

def update_flow(pkt, ts=None):
    ts = ts or time.time()
    key = get_flow_key(pkt)
    if key is None:
        return None
    if key not in flows:
        flows[key] = new_flow(ts)
    rec = flows[key]
    rec["end"] = ts
    rec["pkts"] += 1
    rec["bytes"] += len(bytes(pkt))
    if pkt.haslayer("TCP"):
        flags = pkt["TCP"].flags
        if int(flags & 0x02):  # SYN flag
            rec["syns"] += 1
        rec["dst_ports"].add(int(pkt["TCP"].dport))
    return key

