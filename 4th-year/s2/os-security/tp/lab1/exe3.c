#include <stdio.h>

void vulnerable() {
    char buffer[16];
    printf("Entrez une chaine: ");
    scanf("%s", buffer);
}

int main() {
    vulnerable();
    return 0;
}
