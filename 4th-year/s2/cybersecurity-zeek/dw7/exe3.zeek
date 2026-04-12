@load base/frameworks/notice
@load base/protocols/ssl

redef enum Notice::Type += { Excessive_TLS_Connections };

const tls_conn_threshold = 100;
global tls_conn_count: table[addr] of count &default=0;

event ssl_established(c: connection)
    {
    local ip = c$id$orig_h;
    tls_conn_count[ip] += 1;

    if ( tls_conn_count[ip] > tls_conn_threshold )
        NOTICE([$note=Excessive_TLS_Connections,
                $conn=c,
                $msg=fmt("WARNING: excessive TLS connections from %s (%d)", ip, tls_conn_count[ip])]);
    }
