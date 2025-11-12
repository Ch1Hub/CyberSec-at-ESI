# capture/live_capture.py
from scapy.all import sniff
from features.flow_builder import update_flow, flows
from features.feature_extractor import extract_features
from detection.engine import evaluate_flow
import time

def run_live(iface):
    print("[*] Live sniffing on", iface)
    flows.clear()  # Clear previous flows

    def handle(pkt):
        now = time.time()
        update_flow(pkt, now)
        expired = []
        for k, rec in list(flows.items()):
            if now - rec["end"] > 1:  # expire flows after 1s of idle
                feat = extract_features(k, rec)
                evaluate_flow(feat)
                expired.append(k)
        for k in expired:
            del flows[k]

    sniff(iface=iface, prn=handle, store=0, filter="ip")

