/*
Something is really wrong with this file but i spent really too much time trying
to make something with this, so i will just keep it as is for the time being.
the main issue is that for some reason the expand key function doesn't seem to
work, so after finding candidate keys it's impossible to say which is the
correct key, other than trying them all one by one.
*/

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <iostream>
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

vector<uint8_t> hex_to_bytes(const string &hex) {
  vector<uint8_t> bytes;
  bytes.reserve(hex.length() / 2);

  for (size_t i = 0; i < hex.length(); i += 2) {
    string byte_str = hex.substr(i, 2);
    uint8_t b = static_cast<uint8_t>(stoul(byte_str, nullptr, 16));
    bytes.push_back(b);
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

vector<tuple<uint32_t, uint32_t>>
find_key_chunk(const array<uint8_t, 4> &plain_chunk1,
               const array<uint8_t, 4> &cipher_chunk1,
               const array<uint8_t, 4> &plain_chunk2,
               const array<uint8_t, 4> &cipher_chunk2) {

  vector<tuple<uint32_t, uint32_t>> results;

  for (uint32_t k0_guess = 0; k0_guess < 0xFFFFFFFF; ++k0_guess) {
    bool is_printable = true;
    for (int i = 0; i < 4; ++i) {
      uint8_t byte = (k0_guess >> (8 * i)) & 0xFF;
      if (byte < 0x20 || byte > 0x7E) {
        is_printable = false;
        break;
      }
    }
    if (!is_printable)
      continue;
    // FIRST STATE
    array<uint8_t, 4> state1;
    for (int i = 0; i < 4; ++i) {
      state1[i] = plain_chunk1[i] ^ static_cast<uint8_t>(k0_guess >> (8 * i));
    }

    for (auto &b : state1) {
      b = s_box[b];
    }

    mix_single_column(state1);

    uint32_t k1_candidate = 0;
    for (int i = 0; i < 4; ++i) {
      k1_candidate |= (cipher_chunk1[i] ^ state1[i]) << (8 * i);
    }

    // SECOND STATE
    array<uint8_t, 4> state2;
    for (int i = 0; i < 4; ++i) {
      state2[i] = plain_chunk2[i] ^ static_cast<uint8_t>(k0_guess >> (8 * i));
    }

    for (auto &b : state2) {
      b = s_box[b];
    }

    mix_single_column(state2);

    bool valid = true;
    for (int i = 0; i < 4; ++i) {
      uint8_t encrypted_byte =
          state2[i] ^ static_cast<uint8_t>(k1_candidate >> (8 * i));
      if (encrypted_byte != cipher_chunk2[i]) {
        valid = false;
        break;
      }
    }

    if (valid) {
      results.emplace_back(k0_guess, k1_candidate);
    }
  }

  return results;
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

int main() {
  auto plain2 = hex_to_bytes("ae976f8d95e5bd2eaf40a0efcec97e0d");
  auto cipher2 = hex_to_bytes("ce3776b4dc0551217e856bdfb25251b3");

  auto plain1 = hex_to_bytes("e99c923581939d80e1cf25ee19c891e4");
  auto cipher1 = hex_to_bytes("70439bebea8c21e2b8eb7bad1723656b");

  array<uint8_t, 16> plain_block1, cipher_block1, plain_block2, cipher_block2;
  copy_n(plain1.begin(), 16, plain_block1.begin());
  copy_n(cipher1.begin(), 16, cipher_block1.begin());
  copy_n(plain2.begin(), 16, plain_block2.begin());
  copy_n(cipher2.begin(), 16, cipher_block2.begin());

  auto plain_chunks1 = get_shifted_chunks(plain_block1);
  auto cipher_chunks1 = get_chunks(cipher_block1);
  auto plain_chunks2 = get_shifted_chunks(plain_block2);
  auto cipher_chunks2 = get_chunks(cipher_block2);

  vector<vector<tuple<uint32_t, uint32_t>>> all_possibilities(4);

  all_possibilities[0] = find_key_chunk(plain_chunks1[0], cipher_chunks1[0],
                                        plain_chunks2[0], cipher_chunks2[0]);
  all_possibilities[1] = find_key_chunk(plain_chunks1[1], cipher_chunks1[1],
                                        plain_chunks2[1], cipher_chunks2[1]);
  all_possibilities[2] = find_key_chunk(plain_chunks1[2], cipher_chunks1[2],
                                        plain_chunks2[2], cipher_chunks2[2]);
  all_possibilities[3] = find_key_chunk(plain_chunks1[3], cipher_chunks1[3],
                                        plain_chunks2[3], cipher_chunks2[3]);

  array<array<int, 4>, 4> shifted_positions = {
      {{{0, 5, 10, 15}}, {{4, 9, 14, 3}}, {{8, 13, 2, 7}}, {{12, 1, 6, 11}}}};

  int total = 0;

  for (const auto &chunk0 : all_possibilities[0]) {
    for (const auto &chunk1 : all_possibilities[1]) {
      for (const auto &chunk2 : all_possibilities[2]) {
        for (const auto &chunk3 : all_possibilities[3]) {
          array<uint8_t, 16> k0_full = {};
          array<uint8_t, 16> k1_full = {};

          vector<tuple<uint32_t, uint32_t>> chunks = {chunk0, chunk1, chunk2,
                                                      chunk3};

          for (int chunk_idx = 0; chunk_idx < 4; ++chunk_idx) {
            auto [k0_part, k1_part] = chunks[chunk_idx];

            for (int byte_idx = 0; byte_idx < 4; ++byte_idx) {
              int pos = shifted_positions[chunk_idx][byte_idx];
              k0_full[pos] = static_cast<uint8_t>(k0_part >> (8 * byte_idx));
              k1_full[pos] = static_cast<uint8_t>(k1_part >> (8 * byte_idx));
            }
          }

          array<uint8_t, 16> k1_expanded = expand_key(k0_full);
          if (std::equal(k1_full.begin(), k1_full.end(), k1_expanded.begin())) {
            cout << "Valid Key Pair #" << ++total << ":\n";
            cout << "k0: ";
            printReadableArray(k0_full);
          } else {
            printReadableArray(k0_full);
          }
        }
      }
    }
  }

  if (total == 0) {
    cerr << "No valid keys found!\n";
    return 1;
  }

  return 0;
}