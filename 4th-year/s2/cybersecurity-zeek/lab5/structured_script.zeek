module StructuredScript;

export {
}

global connection_counter: count = 0;
const INIT_MESSAGE = "structured_script initialized";

type ConnInfo: record {
	src: addr;
	dst: addr;
};

function format_connection(info: ConnInfo): string
	{
	return fmt("New connection detected: %s -> %s", info$src, info$dst);
	}

event zeek_init()
	{
	print INIT_MESSAGE;
	}

event new_connection(c: connection)
	{
	local info: ConnInfo = [$src=c$id$orig_h, $dst=c$id$resp_h];

	connection_counter += 1;
	print format_connection(info);
	}
