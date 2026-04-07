module ConnectionAnalysis;

export {
}


function event_timestamp(): string
	{
	return strftime("%Y-%m-%d %H:%M:%S", network_time());
	}

function print_connection_event(label: string, c: connection)
	{
	print fmt("[%s] %s | src_ip=%s src_port=%s dst_ip=%s dst_port=%s",
	          event_timestamp(), label, c$id$orig_h, c$id$orig_p, c$id$resp_h, c$id$resp_p);
	}

event zeek_init()
	{
	print "connection_analysis initialized";
	}

event connection_attempt(c: connection)
	{
	print_connection_event("Connection attempt detected", c);
	}

event connection_established(c: connection)
	{
	print_connection_event("Successful TCP connection", c);
	}

event connection_state_remove(c: connection)
	{
	print_connection_event("Connection ended", c);
	}
