// gcc -fno-stack-protector -o visualizer visualizer.c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

struct Task {
    char buffer[16];
    char target[8];
};

void print_flag() {
    printf("\nYou have successfully performed a buffer overflow!\n");
    system("cat flag.txt");
    exit(0);
}

void print_visualizer(struct Task *t) {
    printf("\n--- Memory ---\n");
    printf("| buffer ---------------------- | target ------ |\n");

    unsigned char *ptr = (unsigned char *)t;
    for (int i = 0; i < 24; i++) {
        char c = ptr[i];
        printf(" %c", (c >= 32 && c <= 126) ? c : '.');
    }
    printf("\n--------------\n");
}

int main() {
    struct Task t;

    memset(t.buffer, '.', sizeof(t.buffer));
    strcpy(t.target, "GUEST");

    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Goal: Overwrite target with 'ADMIN'\n");

    while (1) {
        print_visualizer(&t);

        printf("Input: ");
        int n = read(0, t.buffer, 32);
        if (n > 0 && t.buffer[n-1] == '\n') t.buffer[n-1] = '\0';

        if (strcmp(t.target, "ADMIN") == 0) {
            print_visualizer(&t);
            print_flag();
        } else {
            printf("Current target value: %s\n", t.target);
        }
    }
    return 0;
}