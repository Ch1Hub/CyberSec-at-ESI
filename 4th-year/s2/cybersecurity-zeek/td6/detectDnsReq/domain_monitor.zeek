# Load the DNS protocol analyzer
@load base/protocols/dns

# Ignore checksum errors (needed for NIC offloading)
redef ignore_checksums = T;

event zeek_init() {
    print "DNS Monitor Started!";
    print "Monitoring DNS queries...";
}

event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count) {
    print fmt("DNS Query: %s (type: %d, class: %d)", query, qtype, qclass);
    
    # Check for suspicious domains
    if (query == "malicious.com") {
        print ">>> WARNING: Suspicious domain queried!";
    }
}
