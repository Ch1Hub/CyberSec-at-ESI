# detection/rules.py
"""
Tuned rules to reduce noise from tiny flows:
- Require a minimum number of packets for HIGH_RATE and SYN_FLOOD.
- Require at least 2 SYNs for a SYN flood to avoid 1-2-packet bursts.
"""

def rule_port_scan(f):
    # detect many distinct destination ports
    return f.get("distinct_dst_ports", 0) > 20

def rule_syn_flood(f):
    pkts = int(f.get("pkts", 0))
    syns = int(f.get("syns", 0))

    # ignore extremely small flows
    if pkts < 3:
        return False

    # require at least a couple of SYNs and a sustained rate
    if syns < 2:
        return False

    return (syns / max(pkts, 1)) > 0.6 and f.get("pkt_rate", 0) > 100

def rule_high_rate(f):
    pkts = int(f.get("pkts", 0))

    # ignore tiny flows that produce high rates due to short measured duration
    if pkts < 3:
        return False

    return f.get("pkt_rate", 0) > 500

def check_rules(f):
    if rule_port_scan(f):
        return "PORT_SCAN"
    if rule_syn_flood(f):
        return "SYN_FLOOD"
    if rule_high_rate(f):
        return "HIGH_RATE"
    return None

