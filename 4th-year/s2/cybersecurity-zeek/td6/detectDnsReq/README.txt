===================================================================
DNS Domain Monitor - Zeek Script Usage Guide
===================================================================

FIXED ISSUES:
1. Added @load directive to load DNS protocol analyzer
2. Fixed event signature: dns_request requires 5 parameters
   - c: connection
   - msg: dns_msg
   - query: string
   - qtype: count (DNS record type)
   - qclass: count (DNS class)
3. Added ignore_checksums for NIC offloading
4. Added missing semicolons and proper formatting

DNS RECORD TYPES:
-----------------
Type 1  = A (IPv4 address)
Type 28 = AAAA (IPv6 address)
Type 5  = CNAME (Canonical name)
Type 15 = MX (Mail exchange)
Type 16 = TXT (Text records)

HOW TO USE:
-----------

1. Monitor wireless interface (requires sudo):
   sudo zeek -i wlp0s20f3 domain_monitor.zeek

2. Monitor localhost DNS:
   sudo zeek -i lo domain_monitor.zeek

3. Read from a pcap file:
   zeek -r capture.pcap domain_monitor.zeek

TESTING:
--------

In another terminal, make DNS queries:
  dig google.com
  nslookup github.com
  host facebook.com

FILES:
------
- domain_monitor.zeek: Basic DNS monitoring
- enhanced_domain_monitor.zeek: Advanced with suspicious domain detection

===================================================================
