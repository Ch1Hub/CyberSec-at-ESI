event new_connection(c:connection){
  print fmt("New connection: %s -> %s",c$id$orig_h, c$id$resp_h);
}
