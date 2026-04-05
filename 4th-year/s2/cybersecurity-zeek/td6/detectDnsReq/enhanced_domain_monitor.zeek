# Load the DNS protocol analyzer
@load base/protocols/dns

# Ignore checksum errors (needed for NIC offloading)
redef ignore_checksums = T;

# Define suspicious domains
global suspicious_domains: set[string] = {
    "malicious.com",
    "phishing-site.com",
    "bad-domain.net"
};

event zeek_init() {
    print "=========================================";
    print "DNS Monitor Started!";
    print "Monitoring DNS queries for suspicious domains...";
    print "=========================================";
}

event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count) {
    # Print all DNS queries
    local query_type = "UNKNOWN";
    if (qtype == 1) query_type = "A";
    else if (qtype == 28) query_type = "AAAA";
    else if (qtype == 5) query_type = "CNAME";
    else if (qtype == 15) query_type = "MX";
    else if (qtype == 16) query_type = "TXT";
    
    print fmt("[DNS] %s -> %s (type: %s)", c$id$orig_h, query, query_type);
    
    # Check for suspicious domains
    if (query in suspicious_domains) {
        print "";
        print ">>> !!! ALERT !!! <<<";
        print fmt(">>> Suspicious domain detected: %s", query);
        print fmt(">>> Queried by: %s", c$id$orig_h);
        print ">>> ============= <<<";
        print "";
    }
}

event dns_rejected(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count) {
    print fmt("[DNS REJECTED] Query for %s was rejected", query);
}
