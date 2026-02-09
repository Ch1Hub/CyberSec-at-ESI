#include <unistd.h>
#include <stdio.h>

int main(){
  write(1,"Hello\n", 6);
  return 0;
}
