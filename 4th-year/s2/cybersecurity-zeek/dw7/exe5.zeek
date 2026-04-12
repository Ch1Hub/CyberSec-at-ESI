@load base/frameworks/notice

redef enum Notice::Type += { Rapid_Connection_Attempts };

const rapid_attempt_threshold = 200 ;
const rapid_attempt_window = 30sec ;

global attempt_count: table[addr] of count &default=0;
global window_start: table[addr] of time;

event connection_attempt(c: connection)
    {
    local ip = c$id$orig_h;
    local now = network_time();

    if ( ip !in window_start || now - window_start[ip] > rapid_attempt_window )
        {
        window_start[ip] = now;
        attempt_count[ip] = 1;
        return;
        }

    attempt_count[ip] += 1;

    if ( attempt_count[ip] > rapid_attempt_threshold )
        {
        print fmt("WARNING: rapid connection attempts from %s (%d in %s)", ip, attempt_count[ip], rapid_attempt_window);
        NOTICE([$note=Rapid_Connection_Attempts,
                $conn=c,
                $msg=fmt("Rapid connection attempts from %s (%d in %s)", ip, attempt_count[ip], rapid_attempt_window)]);

        delete attempt_count[ip];
        delete window_start[ip];
        }
    }
