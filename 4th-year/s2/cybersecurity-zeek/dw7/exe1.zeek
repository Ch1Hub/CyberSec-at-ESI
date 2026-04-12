@load base/frameworks/notice

redef enum Notice::Type += { Long_Connection_Detected };
const long_conn_threshold = 5min;

event connection_state_remove(c: connection)
    {
    local start: time = c$start_time;
    local duration: interval = network_time() - start;

    if ( duration > long_conn_threshold )
        NOTICE([$note=Long_Connection_Detected,
                $conn=c,
                $msg=fmt("Long connection uid=%s start=%s duration=%s", c$uid, start, duration)]);
    }
