redef enum Notice::Type += {
	Blacklisted_IP_Connection,
};

global blacklist: set[addr] = set();

event zeek_init()
	{
	print "ip_blacklist_detector initialized";

	add blacklist[10.0.1.104];
	add blacklist[172.20.10.2];
	add blacklist[192.168.1.100];
	}

event new_connection(c: connection)
	{
	local src_ip = c$id$orig_h;

	if ( src_ip in blacklist )
		{
		print fmt("Blacklisted source IP detected: %s", src_ip);

		NOTICE(Notice::Info($note=Blacklisted_IP_Connection,
		                    $msg=fmt("Connection from blacklisted IP: %s", src_ip),
		                    $conn=c));
		}
	}
