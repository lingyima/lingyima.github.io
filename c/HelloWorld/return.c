#include <stdio.h>

void fn(int);

int main(int argc, char args[]) {
  int x,y,a,b;
  x = y = -10;
  fn(x);
  puts("你");
  printf("i=%i\n", y);

  return 0;
}

void fn(int i) {
  if (i > 0) {
    return; 
  }
  printf("%i is smaller 0\n",i);
}