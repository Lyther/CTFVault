#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void init() {
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);
}

char type[] = "ai";

int main() {
  init();

  char name[0x60];
  int phone;
  
  printf("Hi! You are so lucky, you can get a free VIP membership for a year! Please tell me your name and phone number.\n");
  printf("Name: ");
  fgets(name, 0x60, stdin);
  printf("Phone: ");
  scanf("%d", &phone);

  printf("Please confirm your information:\n");
  printf("Name: ");
  printf(name);
  printf("Phone: ");
  printf("%d\n", phone);

  if (strcmp(type, "human") == 0) {
    printf("Congratulations! You can get the VIP membership!\n");
    system("cat flag.txt");
  } else {
    printf("Sorry, we can only give the VIP membership to humans.\n");
  }
}