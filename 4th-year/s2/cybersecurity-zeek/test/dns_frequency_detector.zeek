@load base/frameworks/notice

const dns_query_threshold = 15 &redef;

redef enum Notice::Type += {
    DNS_Frequency_Exceeded
};

global dns_query_count: table[addr, string] of count &default=0;
global alerted: set[addr, string];

event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count)
	{
	local src = c$id$orig_h;
	dns_query_count[src, query] += 1;
	local n = dns_query_count[src, query];

	if ( n > dns_query_threshold && [src, query] !in alerted )
		{
		add alerted[src, query];
		NOTICE([$note=DNS_Frequency_Exceeded,
		        $msg=fmt("WARNING: Domain %s requested %d time by %s", query, n, src),
		        $conn=c,
		        $sub=fmt("%s|%s", src, query)]);
		}
	}
