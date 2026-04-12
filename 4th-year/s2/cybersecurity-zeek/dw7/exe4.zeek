@load base/frameworks/notice
@load base/protocols/ssl

redef enum Notice::Type += { Suspicious_Attacker_Behavior };

const attempt_threshold = 30 &redef;
global conn_attempts: table[addr] of count &default=0;

event connection_attempt(c: connection)
    {
    conn_attempts[c$id$orig_h] += 1;
    }

event ssl_established(c: connection)
    {
    local ip = c$id$orig_h;

    if ( conn_attempts[ip] == attempt_threshold )
        {
        print fmt("ALERT: %s made %d attempts, then established TLS", ip, conn_attempts[ip]);
        NOTICE([$note=Suspicious_Attacker_Behavior,
                $conn=c,
                $msg=fmt("Suspicious behavior: %s made %d attempts before TLS", ip, conn_attempts[ip])]);
        }
    }
