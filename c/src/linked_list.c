/**
 * @file linked_list.c
 * @brief Implementation of linked list data structures
 */

#include "data_structures.h"
#include <stdlib.h>
#include <string.h>

/* Node structure for singly linked list */
typedef struct list_node {
    void* data;
    struct list_node* next;
} list_node_t;

/* Singly linked list structure */
struct linked_list {
    list_node_t* head;
    list_node_t* tail;
    size_t size;
};

/* Create a new linked list */
linked_list_t* list_create(void) {
    linked_list_t* list = malloc(sizeof(linked_list_t));
    if (!list) return NULL;

    list->head = NULL;
    list->tail = NULL;
    list->size = 0;

    return list;
}

/* Destroy linked list */
void list_destroy(linked_list_t* list) {
    if (!list) return;

    list_node_t* current = list->head;
    while (current) {
        list_node_t* next = current->next;
        free(current);
        current = next;
    }

    free(list);
}

/* Insert at front */
bool list_insert_front(linked_list_t* list, void* data) {
    if (!list) return false;

    list_node_t* new_node = malloc(sizeof(list_node_t));
    if (!new_node) return false;

    new_node->data = data;
    new_node->next = list->head;

    list->head = new_node;
    if (!list->tail) {
        list->tail = new_node;
    }

    list->size++;
    return true;
}

/* Insert at back */
bool list_insert_back(linked_list_t* list, void* data) {
    if (!list) return false;

    list_node_t* new_node = malloc(sizeof(list_node_t));
    if (!new_node) return false;

    new_node->data = data;
    new_node->next = NULL;

    if (list->tail) {
        list->tail->next = new_node;
    } else {
        list->head = new_node;
    }

    list->tail = new_node;
    list->size++;
    return true;
}

/* Insert at index */
bool list_insert_at(linked_list_t* list, size_t index, void* data) {
    if (!list || index > list->size) return false;

    if (index == 0) {
        return list_insert_front(list, data);
    }

    if (index == list->size) {
        return list_insert_back(list, data);
    }

    list_node_t* new_node = malloc(sizeof(list_node_t));
    if (!new_node) return false;

    list_node_t* current = list->head;
    for (size_t i = 0; i < index - 1; i++) {
        current = current->next;
    }

    new_node->data = data;
    new_node->next = current->next;
    current->next = new_node;

    list->size++;
    return true;
}

/* Remove from front */
void* list_remove_front(linked_list_t* list) {
    if (!list || !list->head) return NULL;

    list_node_t* old_head = list->head;
    void* data = old_head->data;

    list->head = old_head->next;
    if (!list->head) {
        list->tail = NULL;
    }

    free(old_head);
    list->size--;
    return data;
}

/* Remove from back */
void* list_remove_back(linked_list_t* list) {
    if (!list || !list->head) return NULL;

    if (list->head == list->tail) {
        return list_remove_front(list);
    }

    list_node_t* current = list->head;
    while (current->next != list->tail) {
        current = current->next;
    }

    void* data = list->tail->data;
    free(list->tail);

    list->tail = current;
    list->tail->next = NULL;

    list->size--;
    return data;
}

/* Remove at index */
void* list_remove_at(linked_list_t* list, size_t index) {
    if (!list || index >= list->size) return NULL;

    if (index == 0) {
        return list_remove_front(list);
    }

    list_node_t* current = list->head;
    for (size_t i = 0; i < index - 1; i++) {
        current = current->next;
    }

    list_node_t* to_remove = current->next;
    void* data = to_remove->data;

    current->next = to_remove->next;
    if (to_remove == list->tail) {
        list->tail = current;
    }

    free(to_remove);
    list->size--;
    return data;
}

/* Get element at index */
void* list_get(const linked_list_t* list, size_t index) {
    if (!list || index >= list->size) return NULL;

    list_node_t* current = list->head;
    for (size_t i = 0; i < index; i++) {
        current = current->next;
    }

    return current->data;
}

/* Get list size */
size_t list_size(const linked_list_t* list) {
    return list ? list->size : 0;
}

/* Check if list contains element */
bool list_contains(const linked_list_t* list, const void* data,
                   int (*compare)(const void*, const void*)) {
    if (!list || !compare) return false;

    list_node_t* current = list->head;
    while (current) {
        if (compare(current->data, data) == 0) {
            return true;
        }
        current = current->next;
    }

    return false;
}

/* Node structure for doubly linked list */
typedef struct dlist_node {
    void* data;
    struct dlist_node* next;
    struct dlist_node* prev;
} dlist_node_t;

/* Doubly linked list structure */
struct doubly_linked_list {
    dlist_node_t* head;
    dlist_node_t* tail;
    size_t size;
};

/* Hash table implementation */
typedef struct hash_node {
    void* key;
    void* value;
    struct hash_node* next;
} hash_node_t;

struct hash_table {
    hash_node_t** buckets;
    size_t capacity;
    size_t size;
    uint32_t (*hash_func)(const void*);
    int (*key_compare)(const void*, const void*);
};

/* Common hash function implementations */
uint32_t hash_string_djb2(const void* key) {
    const char* str = (const char*)key;
    uint32_t hash = 5381;
    int c;

    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;  /* hash * 33 + c */
    }

    return hash;
}

uint32_t hash_string_fnv1a(const void* key) {
    const char* str = (const char*)key;
    uint32_t hash = 2166136261u;

    while (*str) {
        hash ^= (uint8_t)*str++;
        hash *= 16777619u;
    }

    return hash;
}

uint32_t hash_int(const void* key) {
    uint32_t x = *(const uint32_t*)key;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = ((x >> 16) ^ x) * 0x45d9f3b;
    x = (x >> 16) ^ x;
    return x;
}

uint32_t hash_pointer(const void* key) {
    uintptr_t ptr = (uintptr_t)key;
    return (uint32_t)(ptr ^ (ptr >> 32));
}

/* Common comparison functions */
int compare_int(const void* a, const void* b) {
    int ia = *(const int*)a;
    int ib = *(const int*)b;
    return (ia > ib) - (ia < ib);
}

int compare_string(const void* a, const void* b) {
    return strcmp((const char*)a, (const char*)b);
}

int compare_double(const void* a, const void* b) {
    double da = *(const double*)a;
    double db = *(const double*)b;
    return (da > db) - (da < db);
}

/* Create hash table */
hash_table_t* ht_create(size_t capacity,
                        uint32_t (*hash)(const void*),
                        int (*compare)(const void*, const void*)) {
    if (capacity == 0 || !hash || !compare) return NULL;

    hash_table_t* table = malloc(sizeof(hash_table_t));
    if (!table) return NULL;

    table->buckets = calloc(capacity, sizeof(hash_node_t*));
    if (!table->buckets) {
        free(table);
        return NULL;
    }

    table->capacity = capacity;
    table->size = 0;
    table->hash_func = hash;
    table->key_compare = compare;

    return table;
}

/* Destroy hash table */
void ht_destroy(hash_table_t* table) {
    if (!table) return;

    for (size_t i = 0; i < table->capacity; i++) {
        hash_node_t* current = table->buckets[i];
        while (current) {
            hash_node_t* next = current->next;
            free(current);
            current = next;
        }
    }

    free(table->buckets);
    free(table);
}

/* Insert key-value pair */
bool ht_insert(hash_table_t* table, void* key, void* value) {
    if (!table || !key) return false;

    uint32_t index = table->hash_func(key) % table->capacity;
    hash_node_t* current = table->buckets[index];

    /* Check if key already exists */
    while (current) {
        if (table->key_compare(current->key, key) == 0) {
            current->value = value;  /* Update existing value */
            return true;
        }
        current = current->next;
    }

    /* Create new node */
    hash_node_t* new_node = malloc(sizeof(hash_node_t));
    if (!new_node) return false;

    new_node->key = key;
    new_node->value = value;
    new_node->next = table->buckets[index];
    table->buckets[index] = new_node;

    table->size++;
    return true;
}

/* Get value by key */
void* ht_get(const hash_table_t* table, const void* key) {
    if (!table || !key) return NULL;

    uint32_t index = table->hash_func(key) % table->capacity;
    hash_node_t* current = table->buckets[index];

    while (current) {
        if (table->key_compare(current->key, key) == 0) {
            return current->value;
        }
        current = current->next;
    }

    return NULL;
}

/* Delete key-value pair */
bool ht_delete(hash_table_t* table, const void* key) {
    if (!table || !key) return false;

    uint32_t index = table->hash_func(key) % table->capacity;
    hash_node_t* current = table->buckets[index];
    hash_node_t* prev = NULL;

    while (current) {
        if (table->key_compare(current->key, key) == 0) {
            if (prev) {
                prev->next = current->next;
            } else {
                table->buckets[index] = current->next;
            }

            free(current);
            table->size--;
            return true;
        }

        prev = current;
        current = current->next;
    }

    return false;
}

/* Check if key exists */
bool ht_contains(const hash_table_t* table, const void* key) {
    return ht_get(table, key) != NULL;
}

/* Get hash table size */
size_t ht_size(const hash_table_t* table) {
    return table ? table->size : 0;
}

/* Calculate load factor */
double ht_load_factor(const hash_table_t* table) {
    if (!table || table->capacity == 0) return 0.0;
    return (double)table->size / table->capacity;
}

/* Rehash table with new capacity */
void ht_rehash(hash_table_t* table, size_t new_capacity) {
    if (!table || new_capacity == 0) return;

    hash_node_t** new_buckets = calloc(new_capacity, sizeof(hash_node_t*));
    if (!new_buckets) return;

    /* Rehash all existing entries */
    for (size_t i = 0; i < table->capacity; i++) {
        hash_node_t* current = table->buckets[i];
        while (current) {
            hash_node_t* next = current->next;

            uint32_t new_index = table->hash_func(current->key) % new_capacity;
            current->next = new_buckets[new_index];
            new_buckets[new_index] = current;

            current = next;
        }
    }

    free(table->buckets);
    table->buckets = new_buckets;
    table->capacity = new_capacity;
}