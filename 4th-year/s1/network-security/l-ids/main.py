# main.py
import sys
from capture import live_capture, pcap_reader

if len(sys.argv) < 2:
    print("Usage: python main.py [iface|pcap_path]")
    sys.exit(1)

arg = sys.argv[1]

if arg.endswith(".pcap"):
    pcap_reader.run_pcap(arg)
else:
    live_capture.run_live(arg)

