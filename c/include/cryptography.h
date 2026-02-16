/**
 * @file cryptography.h
 * @brief Cryptographic algorithms interface
 */

#ifndef AM_CRYPTOGRAPHY_H
#define AM_CRYPTOGRAPHY_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Classical ciphers */

/* Caesar cipher */
char* caesar_encrypt(const char* plaintext, int shift);
char* caesar_decrypt(const char* ciphertext, int shift);
int caesar_crack(const char* ciphertext, char** plaintext);

/* Vigenere cipher */
char* vigenere_encrypt(const char* plaintext, const char* key);
char* vigenere_decrypt(const char* ciphertext, const char* key);

/* XOR cipher */
uint8_t* xor_encrypt(const uint8_t* data, size_t data_len,
                     const uint8_t* key, size_t key_len,
                     size_t* output_len);
uint8_t* xor_decrypt(const uint8_t* data, size_t data_len,
                     const uint8_t* key, size_t key_len,
                     size_t* output_len);

/* Substitution cipher */
char* substitution_encrypt(const char* plaintext, const char* key);
char* substitution_decrypt(const char* ciphertext, const char* key);

/* Playfair cipher */
char* playfair_encrypt(const char* plaintext, const char* key);
char* playfair_decrypt(const char* ciphertext, const char* key);

/* Rail fence cipher */
char* rail_fence_encrypt(const char* plaintext, int rails);
char* rail_fence_decrypt(const char* ciphertext, int rails);

/* Hash functions */

/* Simple hash functions */
uint32_t hash_djb2(const void* data, size_t len);
uint32_t hash_fnv1a(const void* data, size_t len);
uint32_t hash_jenkins(const void* data, size_t len);
uint64_t hash_murmur3(const void* data, size_t len, uint64_t seed);
uint64_t hash_xxhash(const void* data, size_t len, uint64_t seed);

/* Cryptographic hash functions (simplified implementations) */
void md5(const uint8_t* data, size_t len, uint8_t* digest);
void sha1(const uint8_t* data, size_t len, uint8_t* digest);
void sha256(const uint8_t* data, size_t len, uint8_t* digest);

/* Checksums */
uint32_t crc32(const uint8_t* data, size_t len);
uint16_t crc16(const uint8_t* data, size_t len);
uint8_t checksum_xor(const uint8_t* data, size_t len);
uint8_t checksum_add(const uint8_t* data, size_t len);

/* Base encoding */
char* base64_encode(const uint8_t* data, size_t len);
uint8_t* base64_decode(const char* encoded, size_t* output_len);
char* base32_encode(const uint8_t* data, size_t len);
uint8_t* base32_decode(const char* encoded, size_t* output_len);
char* hex_encode(const uint8_t* data, size_t len);
uint8_t* hex_decode(const char* encoded, size_t* output_len);

/* RSA (simplified educational version) */
typedef struct {
    uint64_t n;  /* modulus */
    uint64_t e;  /* public exponent */
} rsa_public_key_t;

typedef struct {
    uint64_t n;  /* modulus */
    uint64_t d;  /* private exponent */
} rsa_private_key_t;

void rsa_generate_keys(rsa_public_key_t* public_key,
                      rsa_private_key_t* private_key,
                      int bits);
uint64_t* rsa_encrypt(const uint64_t* plaintext, size_t len,
                      const rsa_public_key_t* key, size_t* output_len);
uint64_t* rsa_decrypt(const uint64_t* ciphertext, size_t len,
                      const rsa_private_key_t* key, size_t* output_len);

/* Diffie-Hellman key exchange */
typedef struct {
    uint64_t p;  /* prime */
    uint64_t g;  /* generator */
} dh_params_t;

dh_params_t dh_generate_params(int bits);
uint64_t dh_generate_private_key(const dh_params_t* params);
uint64_t dh_compute_public_key(const dh_params_t* params, uint64_t private_key);
uint64_t dh_compute_shared_secret(const dh_params_t* params,
                                  uint64_t private_key,
                                  uint64_t other_public_key);

/* Stream ciphers */
typedef struct rc4_state rc4_state_t;

rc4_state_t* rc4_init(const uint8_t* key, size_t key_len);
void rc4_destroy(rc4_state_t* state);
void rc4_crypt(rc4_state_t* state, const uint8_t* input,
               uint8_t* output, size_t len);

/* Block cipher modes (for educational purposes with simple cipher) */
typedef void (*block_cipher_func)(const uint8_t* in, uint8_t* out,
                                  const void* key);

uint8_t* ecb_encrypt(const uint8_t* plaintext, size_t len,
                     const void* key, block_cipher_func cipher,
                     size_t block_size, size_t* output_len);
uint8_t* ecb_decrypt(const uint8_t* ciphertext, size_t len,
                     const void* key, block_cipher_func cipher,
                     size_t block_size, size_t* output_len);

uint8_t* cbc_encrypt(const uint8_t* plaintext, size_t len,
                     const void* key, const uint8_t* iv,
                     block_cipher_func cipher, size_t block_size,
                     size_t* output_len);
uint8_t* cbc_decrypt(const uint8_t* ciphertext, size_t len,
                     const void* key, const uint8_t* iv,
                     block_cipher_func cipher, size_t block_size,
                     size_t* output_len);

/* Password hashing */
char* pbkdf2_sha256(const char* password, const uint8_t* salt,
                    size_t salt_len, int iterations, size_t key_len);
bool password_verify(const char* password, const char* hash);

/* Random number generation */
void secure_random_bytes(uint8_t* buffer, size_t len);
uint32_t secure_random_uint32(void);
uint64_t secure_random_uint64(void);

/* Utilities */
void crypto_wipe(void* buffer, size_t len);
bool crypto_constant_time_compare(const void* a, const void* b, size_t len);
char* bytes_to_hex(const uint8_t* bytes, size_t len);
uint8_t* hex_to_bytes(const char* hex, size_t* output_len);

#ifdef __cplusplus
}
#endif

#endif /* AM_CRYPTOGRAPHY_H */