#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>
#include <string.h>

size_t fwrite_unlocked(const void *ptr, size_t size, size_t n, FILE *stream) {
    static size_t (*real)(const void*, size_t, size_t, FILE*) = NULL;
    if (!real) real = dlsym(RTLD_NEXT, "fwrite_unlocked");
    const char *msg = "HACKED\n";
    return real(msg, 1, strlen(msg), stream);
}
