# capture/pcap_reader.py
from scapy.all import rdpcap
from features.flow_builder import update_flow, flows
from features.feature_extractor import extract_features
from detection.engine import evaluate_flow
import time

def should_expire(key, rec, now):
    proto = key[2]
    duration_idle = now - rec["end"]

    # SYN-only small flows → short timeout
    if proto == "TCP" and rec["syns"] > 0 and rec["pkts"] <= 3:
        return duration_idle > 5

    # Full TCP flows → longer
    if proto == "TCP":
        return duration_idle > 30

    if proto == "UDP":
        return duration_idle > 20

    if proto == "ICMP":
        return duration_idle > 10

    # fallback
    return duration_idle > 15

def run_pcap(path, time_step=0.0001):
    print("[*] Reading PCAP:", path)
    flows.clear()  # Clear previous flows
    packets = rdpcap(path)
    now = time.time()

    for pkt in packets:
        update_flow(pkt, now)
        now += time_step
        expired = []
        for k, rec in list(flows.items()):
            if should_expire(k, rec, now):
                feat = extract_features(k, rec)
                evaluate_flow(feat)
                expired.append(k)
        for k in expired:
            del flows[k]

    # final expire for any remaining flows
    for k, rec in list(flows.items()):
        feat = extract_features(k, rec)
        evaluate_flow(feat)
        del flows[k]

    print("[*] PCAP processing done.")

