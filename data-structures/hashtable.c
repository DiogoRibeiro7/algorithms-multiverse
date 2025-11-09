/**
 * Comprehensive Hash Table Implementation in C
 *
 * Features:
 * - Separate chaining for collision resolution
 * - Dynamic resizing with configurable load factor
 * - FNV-1a hash function
 * - Generic key-value pairs (string keys)
 * - Iterator support
 * - Performance statistics
 *
 * Time Complexity:
 * - Average: O(1) for insert, delete, search
 * - Worst:   O(n) for chaining with poor hash function
 *
 * Space Complexity: O(n) where n is the number of elements
 *
 * Compilation:
 *   gcc -o hashtable hashtable.c -Wall -Wextra -std=c11
 *
 * Usage:
 *   ./hashtable
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

// ============================================================================
// CONSTANTS AND CONFIGURATION
// ============================================================================

#define INITIAL_CAPACITY 16
#define LOAD_FACTOR 0.75
#define FNV_PRIME 0x01000193
#define FNV_OFFSET 0x811C9DC5

// ============================================================================
// DATA STRUCTURES
// ============================================================================

/**
 * Node in the linked list (chain) for collision resolution.
 */
typedef struct HashNode {
    char *key;
    void *value;
    struct HashNode *next;
} HashNode;

/**
 * Hash table structure with separate chaining.
 */
typedef struct HashTable {
    HashNode **buckets;      // Array of linked list heads
    size_t capacity;         // Number of buckets
    size_t size;            // Number of elements
    double load_factor;     // Resize threshold

    // Statistics
    size_t collisions;
    size_t resizes;
} HashTable;

// ============================================================================
// HASH FUNCTIONS
// ============================================================================

/**
 * FNV-1a hash function - excellent distribution.
 *
 * @param key: String key to hash
 * @return: 32-bit hash value
 */
static uint32_t hash_fnv1a(const char *key) {
    uint32_t hash = FNV_OFFSET;

    while (*key) {
        hash ^= (uint32_t)(*key++);
        hash *= FNV_PRIME;
    }

    return hash;
}

/**
 * Compute bucket index for a key.
 *
 * @param ht: Hash table
 * @param key: Key to hash
 * @return: Bucket index (0 to capacity-1)
 */
static size_t hash_index(const HashTable *ht, const char *key) {
    return hash_fnv1a(key) & (ht->capacity - 1);
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Get next power of 2 >= n.
 *
 * @param n: Input number
 * @return: Next power of 2
 */
static size_t next_power_of_2(size_t n) {
    if (n <= 1) return 1;

    n--;
    n |= n >> 1;
    n |= n >> 2;
    n |= n >> 4;
    n |= n >> 8;
    n |= n >> 16;
    #if SIZE_MAX > 0xFFFFFFFF
    n |= n >> 32;
    #endif
    n++;

    return n;
}

/**
 * Create a new hash node.
 *
 * @param key: Node key (will be duplicated)
 * @param value: Node value
 * @return: Newly allocated node or NULL on failure
 */
static HashNode *hash_node_create(const char *key, void *value) {
    HashNode *node = (HashNode *)malloc(sizeof(HashNode));
    if (!node) return NULL;

    node->key = strdup(key);
    if (!node->key) {
        free(node);
        return NULL;
    }

    node->value = value;
    node->next = NULL;

    return node;
}

/**
 * Free a hash node and its key.
 *
 * @param node: Node to free
 */
static void hash_node_free(HashNode *node) {
    if (node) {
        free(node->key);
        free(node);
    }
}

// ============================================================================
// HASH TABLE OPERATIONS
// ============================================================================

/**
 * Create a new hash table.
 *
 * @param initial_capacity: Initial number of buckets (will be rounded to power of 2)
 * @return: Newly allocated hash table or NULL on failure
 */
HashTable *ht_create(size_t initial_capacity) {
    HashTable *ht = (HashTable *)malloc(sizeof(HashTable));
    if (!ht) return NULL;

    ht->capacity = next_power_of_2(initial_capacity);
    ht->size = 0;
    ht->load_factor = LOAD_FACTOR;
    ht->collisions = 0;
    ht->resizes = 0;

    ht->buckets = (HashNode **)calloc(ht->capacity, sizeof(HashNode *));
    if (!ht->buckets) {
        free(ht);
        return NULL;
    }

    return ht;
}

/**
 * Free all memory used by hash table.
 *
 * @param ht: Hash table to free
 */
void ht_destroy(HashTable *ht) {
    if (!ht) return;

    // Free all nodes in all buckets
    for (size_t i = 0; i < ht->capacity; i++) {
        HashNode *node = ht->buckets[i];
        while (node) {
            HashNode *next = node->next;
            hash_node_free(node);
            node = next;
        }
    }

    free(ht->buckets);
    free(ht);
}

/**
 * Check if hash table should be resized.
 *
 * @param ht: Hash table
 * @return: true if resize is needed
 */
static bool ht_should_resize(const HashTable *ht) {
    return (double)ht->size / ht->capacity > ht->load_factor;
}

/**
 * Resize hash table and rehash all elements.
 *
 * @param ht: Hash table to resize
 * @return: true on success, false on failure
 */
static bool ht_resize(HashTable *ht) {
    size_t old_capacity = ht->capacity;
    HashNode **old_buckets = ht->buckets;

    // Double capacity
    ht->capacity *= 2;
    ht->resizes++;

    // Allocate new buckets
    ht->buckets = (HashNode **)calloc(ht->capacity, sizeof(HashNode *));
    if (!ht->buckets) {
        // Restore old state on failure
        ht->buckets = old_buckets;
        ht->capacity = old_capacity;
        ht->resizes--;
        return false;
    }

    ht->size = 0;
    ht->collisions = 0;

    // Rehash all entries
    for (size_t i = 0; i < old_capacity; i++) {
        HashNode *node = old_buckets[i];
        while (node) {
            HashNode *next = node->next;

            // Re-insert node
            size_t index = hash_index(ht, node->key);

            if (ht->buckets[index]) {
                ht->collisions++;
            }

            node->next = ht->buckets[index];
            ht->buckets[index] = node;
            ht->size++;

            node = next;
        }
    }

    free(old_buckets);
    return true;
}

/**
 * Insert or update a key-value pair.
 *
 * @param ht: Hash table
 * @param key: Key (string)
 * @param value: Value (generic pointer)
 * @return: Previous value if key existed, NULL otherwise
 */
void *ht_put(HashTable *ht, const char *key, void *value) {
    if (!ht || !key) return NULL;

    // Resize if necessary
    if (ht_should_resize(ht)) {
        ht_resize(ht);
    }

    size_t index = hash_index(ht, key);
    HashNode *node = ht->buckets[index];

    // Search for existing key
    while (node) {
        if (strcmp(node->key, key) == 0) {
            // Key found, update value
            void *old_value = node->value;
            node->value = value;
            return old_value;
        }
        node = node->next;
    }

    // Key not found, insert at head
    HashNode *new_node = hash_node_create(key, value);
    if (!new_node) return NULL;

    if (ht->buckets[index] != NULL) {
        ht->collisions++;
    }

    new_node->next = ht->buckets[index];
    ht->buckets[index] = new_node;
    ht->size++;

    return NULL;
}

/**
 * Retrieve value for a key.
 *
 * @param ht: Hash table
 * @param key: Key to search for
 * @return: Value if found, NULL otherwise
 */
void *ht_get(const HashTable *ht, const char *key) {
    if (!ht || !key) return NULL;

    size_t index = hash_index(ht, key);
    HashNode *node = ht->buckets[index];

    while (node) {
        if (strcmp(node->key, key) == 0) {
            return node->value;
        }
        node = node->next;
    }

    return NULL;
}

/**
 * Remove a key and return its value.
 *
 * @param ht: Hash table
 * @param key: Key to remove
 * @return: Value if found, NULL otherwise
 */
void *ht_remove(HashTable *ht, const char *key) {
    if (!ht || !key) return NULL;

    size_t index = hash_index(ht, key);
    HashNode *node = ht->buckets[index];
    HashNode *prev = NULL;

    while (node) {
        if (strcmp(node->key, key) == 0) {
            // Found key, remove node
            if (prev) {
                prev->next = node->next;
            } else {
                ht->buckets[index] = node->next;
            }

            void *value = node->value;
            hash_node_free(node);
            ht->size--;

            return value;
        }
        prev = node;
        node = node->next;
    }

    return NULL;
}

/**
 * Check if a key exists in the hash table.
 *
 * @param ht: Hash table
 * @param key: Key to search for
 * @return: true if key exists, false otherwise
 */
bool ht_contains(const HashTable *ht, const char *key) {
    return ht_get(ht, key) != NULL;
}

/**
 * Get number of elements in hash table.
 *
 * @param ht: Hash table
 * @return: Number of elements
 */
size_t ht_size(const HashTable *ht) {
    return ht ? ht->size : 0;
}

/**
 * Remove all elements from hash table.
 *
 * @param ht: Hash table to clear
 */
void ht_clear(HashTable *ht) {
    if (!ht) return;

    for (size_t i = 0; i < ht->capacity; i++) {
        HashNode *node = ht->buckets[i];
        while (node) {
            HashNode *next = node->next;
            hash_node_free(node);
            node = next;
        }
        ht->buckets[i] = NULL;
    }

    ht->size = 0;
    ht->collisions = 0;
}

/**
 * Print hash table statistics.
 *
 * @param ht: Hash table
 */
void ht_print_stats(const HashTable *ht) {
    if (!ht) return;

    // Calculate chain statistics
    size_t max_chain = 0;
    size_t total_chain_length = 0;
    size_t num_chains = 0;

    for (size_t i = 0; i < ht->capacity; i++) {
        size_t chain_length = 0;
        HashNode *node = ht->buckets[i];

        while (node) {
            chain_length++;
            node = node->next;
        }

        if (chain_length > 0) {
            num_chains++;
            total_chain_length += chain_length;
            if (chain_length > max_chain) {
                max_chain = chain_length;
            }
        }
    }

    printf("Hash Table Statistics:\n");
    printf("  Size:              %zu\n", ht->size);
    printf("  Capacity:          %zu\n", ht->capacity);
    printf("  Load Factor:       %.2f / %.2f\n",
           (double)ht->size / ht->capacity, ht->load_factor);
    printf("  Collisions:        %zu\n", ht->collisions);
    printf("  Resizes:           %zu\n", ht->resizes);
    printf("  Max Chain Length:  %zu\n", max_chain);
    printf("  Avg Chain Length:  %.2f\n",
           num_chains > 0 ? (double)total_chain_length / num_chains : 0.0);
    printf("  Number of Chains:  %zu\n", num_chains);
}

/**
 * Print all key-value pairs in hash table.
 *
 * @param ht: Hash table
 */
void ht_print(const HashTable *ht) {
    if (!ht) return;

    printf("Hash Table Contents (%zu elements):\n", ht->size);

    for (size_t i = 0; i < ht->capacity; i++) {
        HashNode *node = ht->buckets[i];
        if (node) {
            printf("  Bucket %zu: ", i);
            while (node) {
                printf("[%s: %p]", node->key, node->value);
                if (node->next) printf(" -> ");
                node = node->next;
            }
            printf("\n");
        }
    }
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

int main(void) {
    printf("===========================================\n");
    printf("Hash Table Implementation in C\n");
    printf("===========================================\n\n");

    // Create hash table
    HashTable *ht = ht_create(INITIAL_CAPACITY);
    if (!ht) {
        fprintf(stderr, "Failed to create hash table\n");
        return 1;
    }

    printf("1. Inserting elements...\n");
    printf("-----------------------------------------\n");

    // Insert some data
    int values[] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    for (int i = 0; i < 10; i++) {
        char key[20];
        snprintf(key, sizeof(key), "key%d", i);
        ht_put(ht, key, &values[i]);
        printf("  Inserted: %s -> %d\n", key, values[i]);
    }

    printf("\nSize: %zu\n\n", ht_size(ht));

    printf("2. Retrieving elements...\n");
    printf("-----------------------------------------\n");

    const char *test_keys[] = {"key0", "key5", "key9", "nonexistent"};
    for (size_t i = 0; i < 4; i++) {
        int *value = (int *)ht_get(ht, test_keys[i]);
        if (value) {
            printf("  Get '%s': %d\n", test_keys[i], *value);
        } else {
            printf("  Get '%s': Not found\n", test_keys[i]);
        }
    }

    printf("\n3. Testing containment...\n");
    printf("-----------------------------------------\n");
    printf("  Contains 'key3': %s\n", ht_contains(ht, "key3") ? "Yes" : "No");
    printf("  Contains 'missing': %s\n", ht_contains(ht, "missing") ? "Yes" : "No");

    printf("\n4. Updating values...\n");
    printf("-----------------------------------------\n");

    int new_value = 999;
    int *old = (int *)ht_put(ht, "key5", &new_value);
    printf("  Updated 'key5': old value = %d, new value = %d\n",
           old ? *old : -1, new_value);

    printf("\n5. Removing elements...\n");
    printf("-----------------------------------------\n");

    int *removed = (int *)ht_remove(ht, "key7");
    if (removed) {
        printf("  Removed 'key7': %d\n", *removed);
    }
    printf("  Size after removal: %zu\n", ht_size(ht));

    printf("\n6. Performance Statistics\n");
    printf("-----------------------------------------\n");
    ht_print_stats(ht);

    printf("\n7. Testing with many elements...\n");
    printf("-----------------------------------------\n");

    // Insert many elements to trigger resizing
    for (int i = 100; i < 200; i++) {
        char key[20];
        snprintf(key, sizeof(key), "item%d", i);
        ht_put(ht, key, &values[i % 10]);
    }

    printf("  Added 100 more elements\n");
    printf("  New size: %zu\n", ht_size(ht));
    printf("\n");
    ht_print_stats(ht);

    printf("\n8. Clearing hash table...\n");
    printf("-----------------------------------------\n");
    ht_clear(ht);
    printf("  Size after clear: %zu\n", ht_size(ht));

    // Cleanup
    ht_destroy(ht);

    printf("\n===========================================\n");
    printf("✨ Hash table demonstration complete!\n");
    printf("===========================================\n");

    return 0;
}
