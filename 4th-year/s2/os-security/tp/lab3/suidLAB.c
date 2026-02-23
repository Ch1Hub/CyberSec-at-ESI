#include <stdio.h>
#include <unistd.h>
#include <sys.h>
int main() {
printf("UID réel : %d\n", getuid());
printf("UID effectif : %d\n", geteuid());
system("/bin/sh")
return 0;}
