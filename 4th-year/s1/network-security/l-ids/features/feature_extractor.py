# features/feature_extractor.py
"""
Create stable, bounded numeric features for rules.
- Ensure duration never zero (min 1ms).
- Cap pkt_rate to avoid absurd values from tiny durations.
"""
def extract_features(key, rec):
    # duration in seconds (end - start)
    duration = rec.get("end", 0) - rec.get("start", 0)
    if duration <= 0:
        # minimum measurable duration: 1 millisecond
        duration = 0.001

    pkts = int(rec.get("pkts", 0))
    bytes_ = int(rec.get("bytes", 0))
    syns = int(rec.get("syns", 0))

    # raw pkt rate (pkts per second)
    pkt_rate = pkts / duration if duration > 0 else float("inf")

    # Cap rate to a reasonable upper bound to avoid tiny-duration spikes
    MAX_PKT_RATE = 10000.0
    if pkt_rate > MAX_PKT_RATE:
        pkt_rate = MAX_PKT_RATE

    # average packet length
    mean_pkt_len = bytes_ / pkts if pkts > 0 else 0.0

    return {
        "src": key[0],
        "dst": key[1],
        "proto": key[2],
        "sport": key[3],
        "dport": key[4],
        "duration": round(duration, 3),
        "pkts": pkts,
        "bytes": bytes_,
        "syns": syns,
        "distinct_dst_ports": int(len(rec.get("dst_ports", set()))),
        "pkt_rate": round(pkt_rate, 2),
        "mean_pkt_len": round(mean_pkt_len, 2)
    }

