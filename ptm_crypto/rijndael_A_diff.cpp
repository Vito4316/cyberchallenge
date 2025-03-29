#include <algorithm>
#include <array>
#include <cctype>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <set>
#include <string>
#include <tuple>
#include <vector>

using namespace std;

array<uint8_t, 256> s_box = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B,
    0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26,
    0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2,
    0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED,
    0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F,
    0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC,
    0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14,
    0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D,
    0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F,
    0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11,
    0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F,
    0xB0, 0x54, 0xBB, 0x16,
};

array<uint8_t, 16> hex_to_bytes(const string &hex) {
  array<uint8_t, 16> bytes;

  for (size_t i = 0; i < 32; i += 2) {
    string byte_str = hex.substr(i, 2);
    uint8_t b = static_cast<uint8_t>(stoul(byte_str, nullptr, 16));
    bytes[i / 2] = b;
  }

  return bytes;
}

array<array<uint8_t, 4>, 4>
get_shifted_chunks(const array<uint8_t, 16> &block) {
  return {{{block[0], block[5], block[10], block[15]},
           {block[4], block[9], block[14], block[3]},
           {block[8], block[13], block[2], block[7]},
           {block[12], block[1], block[6], block[11]}}};
}

void inv_shift_rows(std::array<std::array<uint8_t, 4>, 4> &s) {
  // Row 1: right shift by 1
  uint8_t temp = s[3][1];
  s[3][1] = s[2][1];
  s[2][1] = s[1][1];
  s[1][1] = s[0][1];
  s[0][1] = temp;

  // Row 2: left shift by 2 (same as forward operation)
  temp = s[0][2];
  s[0][2] = s[2][2];
  s[2][2] = temp;
  temp = s[1][2];
  s[1][2] = s[3][2];
  s[3][2] = temp;

  // Row 3: right shift by 1 (equivalent to left shift by 3 in forward)
  temp = s[0][3];
  s[0][3] = s[1][3];
  s[1][3] = s[2][3];
  s[2][3] = s[3][3];
  s[3][3] = temp;
}

array<array<uint8_t, 4>, 4> get_chunks(const array<uint8_t, 16> &block) {
  return {{{block[0], block[1], block[2], block[3]},
           {block[4], block[5], block[6], block[7]},
           {block[8], block[9], block[10], block[11]},
           {block[12], block[13], block[14], block[15]}}};
}

uint8_t xtime(uint8_t a) { return (a & 0x80) ? ((a << 1) ^ 0x1B) : (a << 1); }

void mix_single_column(array<uint8_t, 4> &col) {
  uint8_t a = col[0], b = col[1], c = col[2], d = col[3];
  col[0] = xtime(a) ^ xtime(b) ^ b ^ c ^ d;
  col[1] = a ^ xtime(b) ^ xtime(c) ^ c ^ d;
  col[2] = a ^ b ^ xtime(c) ^ xtime(d) ^ d;
  col[3] = xtime(a) ^ a ^ b ^ c ^ xtime(d);
}

void mix_columns(std::array<std::array<uint8_t, 4>, 4> &s) {
  for (int i = 0; i < 4; i++) {
    mix_single_column(s[i]);
  }
}

void inv_mix_columns(std::array<std::array<uint8_t, 4>, 4> &s) {
  for (int i = 0; i < 4; i++) {
    uint8_t u = xtime(xtime(s[i][0] ^ s[i][2]));
    uint8_t v = xtime(xtime(s[i][1] ^ s[i][3]));
    s[i][0] ^= u;
    s[i][1] ^= v;
    s[i][2] ^= u;
    s[i][3] ^= v;
  }

  mix_columns(s);
}

array<uint8_t, 16> expand_key(const array<uint8_t, 16> &k0) {
  array<uint8_t, 16> k1;

  // Split k0 into words w0-w3
  uint32_t w[4];
  for (int i = 0; i < 4; ++i) {
    w[i] = (static_cast<uint32_t>(k0[4 * i]) << 24) |
           (static_cast<uint32_t>(k0[4 * i + 1]) << 16) |
           (static_cast<uint32_t>(k0[4 * i + 2]) << 8) |
           static_cast<uint32_t>(k0[4 * i + 3]);
  }

  // Compute w4
  uint32_t temp = w[3];
  // RotWord
  temp = (temp << 8) | (temp >> 24);
  // SubWord
  temp = (s_box[(temp >> 24) & 0xFF] << 24) |
         (s_box[(temp >> 16) & 0xFF] << 16) | (s_box[(temp >> 8) & 0xFF] << 8) |
         s_box[temp & 0xFF];
  // XOR with Rcon[1] (0x01, 0x00, 0x00, 0x00)
  temp ^= 0x01000000;

  uint32_t w4 = w[0] ^ temp;
  uint32_t w5 = w[1] ^ w4;
  uint32_t w6 = w[2] ^ w5;
  uint32_t w7 = w[3] ^ w6;

  // Convert words back to bytes
  for (int i = 0; i < 4; ++i) {
    k1[i] = (w4 >> (24 - 8 * i)) & 0xFF;
    k1[4 + i] = (w5 >> (24 - 8 * i)) & 0xFF;
    k1[8 + i] = (w6 >> (24 - 8 * i)) & 0xFF;
    k1[12 + i] = (w7 >> (24 - 8 * i)) & 0xFF;
  }

  return k1;
}

void printReadableArray(const array<uint8_t, 16> &arr) {
  for (const auto &byte : arr) {
    if (byte >= 0x20 && byte <= 0x7E) {
      cout << byte << " ";
    } else {
      cout << "? ";
    }
  }
  cout << endl;
}

array<array<vector<tuple<uint8_t, uint8_t>>, 256>, 256> get_sbox_ddt() {
  array<array<vector<tuple<uint8_t, uint8_t>>, 256>, 256> table;
  for (int i = 0; i < 256; i++) {
    for (int j = 0; j < 256; j++) {
      uint8_t diff_input = i ^ j;
      uint8_t diff_output = s_box[i] ^ s_box[j];
      table[diff_input][diff_output].emplace_back(i, j);
    }
  }
  return table;
}

void print_keys(vector<set<uint8_t>> &guesses, string &key, int pos) {
  if (pos >= 16) {
    cout << key<<"\n";
    return;
  }

  for (auto guess : guesses[pos]) {
    key[pos] = guess;
    print_keys(guesses, key, pos + 1);
  }
}

int main() {
  auto plain2 = hex_to_bytes("ae976f8d95e5bd2eaf40a0efcec97e0d");
  auto cipher2 = hex_to_bytes("ce3776b4dc0551217e856bdfb25251b3");

  auto plain1 = hex_to_bytes("e99c923581939d80e1cf25ee19c891e4");
  auto cipher1 = hex_to_bytes("70439bebea8c21e2b8eb7bad1723656b");

  array<uint8_t, 16> diff_plain, diff_cipher;

  copy_n(plain1.begin(), 16, diff_plain.begin());
  copy_n(cipher1.begin(), 16, diff_cipher.begin());

  for (int i = 0; i < 16; ++i)
    diff_plain[i] ^= plain2[i];
  for (int i = 0; i < 16; ++i)
    diff_cipher[i] ^= cipher2[i];

  auto plain1_blocks = get_chunks(plain1);
  auto plain2_blocks = get_chunks(plain2);
  auto diff_plain_blocks = get_chunks(diff_plain);
  auto diff_cipher_blocks = get_chunks(diff_cipher);
  auto sbox_differences = get_sbox_ddt();

  inv_mix_columns(diff_cipher_blocks);
  inv_shift_rows(diff_cipher_blocks);

  vector<set<uint8_t>> guesses;
  guesses.resize(16);
  string _key = "0000000000000000";

  for (int i = 0; i < 4; ++i) {
    for (int j = 0; j < 4; ++j) {
      for (auto guess_tuple : sbox_differences[diff_plain_blocks[i][j]]
                                              [diff_cipher_blocks[i][j]]) {
        auto [x, y] = guess_tuple;
        auto guess1 = x ^ plain1_blocks[i][j];
        auto guess2 = x ^ plain2_blocks[i][j];

        if (isprint(guess1))
          guesses[i * 4 + j].insert(guess1);
        if (isprint(guess2))
          guesses[i * 4 + j].insert(guess2);
      }
    }
  }

  print_keys(guesses, _key, 0);

  return 0;
}

/*
ptm{kdjb23uih39}
*/