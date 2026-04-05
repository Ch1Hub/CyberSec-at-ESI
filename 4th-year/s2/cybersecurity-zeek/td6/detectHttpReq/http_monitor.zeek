# Load the HTTP protocol analyzer
@load base/protocols/http

# Ignore checksum errors (needed for monitoring localhost and NIC offloading)
redef ignore_checksums = T;

event zeek_init() {
    print "HTTP Monitor Started!";
    print "Listening for HTTP requests...";
}

event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string) {
    print "";
    print ">>> HTTP REQUEST DETECTED <<<";
    print fmt("  Method: %s", method);
    print fmt("  URI: %s", original_URI);
    print fmt("  Version: %s", version);
    print fmt("  From: %s:%s", c$id$orig_h, c$id$orig_p);
    print fmt("  To: %s:%s", c$id$resp_h, c$id$resp_p);
    print "==================================";
}
