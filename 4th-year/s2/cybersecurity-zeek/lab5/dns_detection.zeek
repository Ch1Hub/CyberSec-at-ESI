redef enum Notice::Type += {
	Suspicious_Domain_Query,
};

const suspicious_domains: set[string] = {
	"malicious.com",
	"evil.com",
	"bad-domain.example"
};

event zeek_init()
	{
	print "dns_detection initialized";
	}

function print_resolved_ip(query: string, ip: addr)
	{
	local normalized_query = to_lower(rstrip(query, "."));

	if ( normalized_query in suspicious_domains )
		print fmt("Resolved suspicious domain: %s -> %s", normalized_query, ip);
	}

event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count)
	{
	local normalized_query = to_lower(rstrip(query, "."));

	if ( normalized_query in suspicious_domains )
		{
		print fmt("Suspicious DNS query detected: %s", normalized_query);

		NOTICE(Notice::Info($note=Suspicious_Domain_Query,
		                    $msg=fmt("Suspicious DNS domain queried: %s", normalized_query),
		                    $conn=c));
		}
	}

