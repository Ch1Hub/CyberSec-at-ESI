# Load the HTTP protocol analyzer
@load base/protocols/http

event zeek_init() {
    print "===========================================";
    print "HTTP Monitor Started!";
    print fmt("Monitoring interface: wlp0s20f3");
    print "Waiting for HTTP traffic...";
    print "===========================================";
}

event http_request(c: connection, method: string, original_URI: string, unescaped_URI: string, version: string) {
    print "";
    print ">>> HTTP REQUEST DETECTED <<<";
    print fmt("  Method: %s", method);
    print fmt("  URI: %s", original_URI);
    print fmt("  Version: %s", version);
    print fmt("  Client: %s:%s", c$id$orig_h, c$id$orig_p);
    print fmt("  Server: %s:%s", c$id$resp_h, c$id$resp_p);
    print "====================================";
}

event connection_established(c: connection) {
    print fmt("[DEBUG] Connection established: %s:%s -> %s:%s", 
               c$id$orig_h, c$id$orig_p, c$id$resp_h, c$id$resp_p);
}
