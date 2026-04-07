global counter: table[addr] of count;

event zeek_init()
	{
	print "port_scan_detector initialized";
	}

event new_connection(c: connection)
	{
	if ( get_port_transport_proto(c$id$resp_p) != tcp )
		return;

	local src_ip = c$id$orig_h;

	if ( src_ip !in counter )
		counter[src_ip] = 0;

	counter[src_ip] += 1;

	if ( counter[src_ip] > 10 )
		print fmt("Warning: possible port scan from %s (%d connection attempts)", src_ip, counter[src_ip]);
	}
