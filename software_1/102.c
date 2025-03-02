#include<stdio.h>

#define uint unsigned int
#define true 1
#define false 0

/*
extracted code from ghidra, this is the equivalent version without the sleep called after printf
*/

int main(void)
{
  uint local_c;

  char arr[32] = {0};
  
  puts("Your flag is:");
  local_c = 457;
  do {
    while( true ) {
      do {
        while( true ) {
          printf("\rCCIT{%s}",arr);
          fflush(stdout);
          if (local_c != 8192) break;
          arr[16] = 's';
          local_c = 13;
        }
      } while (8192 < local_c);
      if (local_c != 0x1000) break;
      arr[20] = arr[10];
      arr[15] = arr[10];
      local_c = 0x2000;
    }
    if (local_c < 0x1001) {
      if (local_c == 0x800) {
        arr[14] = arr[7] + -1;
        local_c = 0x1000;
      }
      else if (local_c < 0x801) {
        if (local_c == 0x3f2) {
          arr[24] = 0x70;
          local_c = 0;
        }
        else if (local_c < 0x3f3) {
          if (local_c == 999) {
            arr[2] = 0x6d;
            local_c = 300;
          }
          else if (local_c < 1000) {
            if (local_c == 0x32b) {
              arr[8] = arr[5] + -1;
              local_c = 7;
            }
            else if (local_c < 0x32c) {
              if (local_c == 0x1c9) {
                arr[0] = 0x74;
                local_c = 0x78;
              }
              else if (local_c < 0x1ca) {
                if (local_c == 300) {
                  arr[3] = '3';
                  local_c = 0x36;
                }
                else if (local_c < 0x12d) {
                  if (local_c < 0x79) {
                    switch(local_c) {
                    case 0:
                      putchar(10);
                    /* WARNING: Subroutine does not return */
                      return -1;
                    case 3:
                      arr[7] = arr[1];
                      local_c = 0x32b;
                      break;
                    case 6:
                      arr[23] = 'L';
                      local_c = 1010;
                      break;
                    case 7:
                      arr[9] = arr[3] + '\x02';
                      local_c = 0x15;
                      break;
                    case 0xc:
                      arr[5] = 'f';
                      local_c = 100;
                      break;
                    case 0xd:
                      arr[17] = arr[3] + -3;
                      local_c = 0x6f;
                      break;
                    case 0x15:
                      arr[10] = arr[4];
                      local_c = 0x32;
                      break;
                    case 0x18:
                      arr[22] = arr[8];
                      local_c = 6;
                      break;
                    case 0x32:
                      arr[11] = 0x57;
                      local_c = 0x3c;
                      break;
                    case 0x36:
                      arr[4] = 0x5f;
                      local_c = 0xc;
                      break;
                    case 0x3c:
                      arr[12] = arr[1];
                      local_c = 0x46;
                      break;
                    case 0x46:
                      arr[13] = 0x54;
                      local_c = 0x800;
                      break;
                    case 0x49:
                      arr[21] = 0x68;
                      local_c = 0x18;
                      break;
                    case 100:
                      arr[6] = 0x6c;
                      local_c = 3;
                      break;
                    case 0x6f:
                      arr[18] = arr[2];
                      local_c = 0xdf;
                      break;
                    case 0x78:
                      arr[1] = 'i';
                      local_c = 999;
                    }
                  }
                  else if (local_c == 0xdf) {
                    arr[19] = arr[17] + '\x03';
                    local_c = 0x49;
                  }
                }
              }
            }
          }
        }
      }
    }
  } while( true );
}

