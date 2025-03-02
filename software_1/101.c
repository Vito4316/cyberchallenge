#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

int main(void)
{
  uint32_t *arr_ptr;
  uint32_t arr [6];

  arr[0] = 0xabb6bcbc;
  arr[1] = 0x9d9b9884;
  arr[2] = 0xa0cf8ba0;
  arr[3] = 0xa0cc978b;
  arr[4] = 0x9cca9a8d;
  arr[5] = 0xff829a8a;
  arr_ptr = arr;
  while( true ) {
    if ((char)~*(char *)arr_ptr == 0) break;
    putchar(~*(char *)arr_ptr);
    arr_ptr = (uint32_t *)((int)arr_ptr + 1);
  }
  putchar(L'\n');
  return 0;
}

