===================================================================
HTTP Monitor - Zeek Script Usage Guide
===================================================================

FIXED ISSUES:
1. Added @load directive to load HTTP protocol analyzer
2. Added "ignore_checksums = T" to handle NIC checksum offloading
3. Corrected event signature with all 5 parameters

HOW TO USE:
-----------

1. Monitor wireless interface (requires sudo):
   sudo zeek -i wlp0s20f3 http_monitor.zeek

2. Monitor localhost (for testing):
   sudo zeek -i lo http_monitor.zeek

3. Read from a pcap file:
   zeek -r capture.pcap http_monitor.zeek

TESTING:
--------

In another terminal, make HTTP requests:
  curl http://neverssl.com/
  curl http://httpforever.com/
  curl http://example.com/

NOTE: Most modern sites use HTTPS, which Zeek won't show as HTTP.
      Use sites that still support plain HTTP for testing.

WHY IT WASN'T WORKING:
----------------------
- Missing @load directive (HTTP analyzer wasn't loaded)
- Checksum offloading causing packet drops
- Many sites only use HTTPS (encrypted, not visible as HTTP)

===================================================================
