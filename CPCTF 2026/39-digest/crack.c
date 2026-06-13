#include <openssl/md5.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static const char *PREFIX = "cpctf:Restricted:";
static const char *SUFFIX =
    ":+pHR2klPBgA=dea9c5d3f34f861b03f0be19a41069cf29603de5:"
    "00000001:1afdf6a5de6ae0bc:auth:71998c64aea37ae77020c49c00f73fa8";
static const char *TARGET = "b71427f528886528c5144cd259a83d97";

static atomic_int found = 0;
static char found_pwd[9] = {0};

typedef struct {
  uint32_t start;
  uint32_t end;
} Task;

static inline void md5_hex(const unsigned char *data, size_t len, char *out) {
  static const char hex[] = "0123456789abcdef";
  unsigned char digest[16];

  MD5(data, len, digest);
  for (int i = 0; i < 16; i++) {
    out[i * 2] = hex[digest[i] >> 4];
    out[i * 2 + 1] = hex[digest[i] & 0xf];
  }
  out[32] = '\0';
}

static void *worker(void *arg) {
  Task *task = (Task *)arg;
  char pwd[9];
  char ha1_input[64];
  char ha1_hex[33];
  char resp_input[256];

  strcpy(ha1_input, PREFIX);
  size_t prefix_len = strlen(PREFIX);
  strcpy(resp_input + 32, SUFFIX);
  size_t suffix_len = strlen(SUFFIX);

  for (uint32_t x = task->start; x < task->end && !atomic_load(&found); x++) {
    snprintf(pwd, sizeof(pwd), "%08u", x);

    memcpy(ha1_input + prefix_len, pwd, 8);
    ha1_input[prefix_len + 8] = '\0';
    md5_hex((const unsigned char *)ha1_input, prefix_len + 8, ha1_hex);

    memcpy(resp_input, ha1_hex, 32);
    md5_hex((const unsigned char *)resp_input, 32 + suffix_len, ha1_hex);

    if (memcmp(ha1_hex, TARGET, 32) == 0) {
      if (!atomic_exchange(&found, 1)) {
        memcpy(found_pwd, pwd, 9);
      }
      break;
    }
  }

  return NULL;
}

int main(int argc, char **argv) {
  int threads = 12;
  if (argc > 1) {
    threads = atoi(argv[1]);
  }

  pthread_t *ths = calloc((size_t)threads, sizeof(pthread_t));
  Task *tasks = calloc((size_t)threads, sizeof(Task));
  uint32_t chunk = 100000000u / (uint32_t)threads;
  uint32_t cur = 0;
  struct timespec t1, t2;

  clock_gettime(CLOCK_MONOTONIC, &t1);

  for (int i = 0; i < threads; i++) {
    tasks[i].start = cur;
    tasks[i].end = (i == threads - 1) ? 100000000u : cur + chunk;
    cur = tasks[i].end;
    pthread_create(&ths[i], NULL, worker, &tasks[i]);
  }

  for (int i = 0; i < threads; i++) {
    pthread_join(ths[i], NULL);
  }

  clock_gettime(CLOCK_MONOTONIC, &t2);
  double sec =
      (double)(t2.tv_sec - t1.tv_sec) + (double)(t2.tv_nsec - t1.tv_nsec) / 1e9;

  if (found_pwd[0]) {
    printf("password=%s\n", found_pwd);
  } else {
    printf("password not found\n");
  }
  printf("elapsed=%.3f\n", sec);
  return 0;
}
