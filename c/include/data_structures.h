/**
 * @file data_structures.h
 * @brief Data structures interface
 */

#ifndef AM_DATA_STRUCTURES_H
#define AM_DATA_STRUCTURES_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Forward declarations */
typedef struct stack stack_t;
typedef struct queue queue_t;
typedef struct deque deque_t;
typedef struct priority_queue priority_queue_t;
typedef struct linked_list linked_list_t;
typedef struct doubly_linked_list doubly_linked_list_t;
typedef struct binary_tree binary_tree_t;
typedef struct bst bst_t;
typedef struct avl_tree avl_tree_t;
typedef struct red_black_tree red_black_tree_t;
typedef struct b_tree b_tree_t;
typedef struct trie trie_t;
typedef struct hash_table hash_table_t;
typedef struct disjoint_set disjoint_set_t;
typedef struct segment_tree segment_tree_t;
typedef struct fenwick_tree fenwick_tree_t;
typedef struct heap heap_t;

/* Stack operations */
stack_t* stack_create(size_t capacity);
void stack_destroy(stack_t* stack);
bool stack_push(stack_t* stack, void* data);
void* stack_pop(stack_t* stack);
void* stack_peek(const stack_t* stack);
bool stack_is_empty(const stack_t* stack);
bool stack_is_full(const stack_t* stack);
size_t stack_size(const stack_t* stack);
void stack_clear(stack_t* stack);

/* Queue operations */
queue_t* queue_create(size_t capacity);
void queue_destroy(queue_t* queue);
bool queue_enqueue(queue_t* queue, void* data);
void* queue_dequeue(queue_t* queue);
void* queue_front(const queue_t* queue);
void* queue_rear(const queue_t* queue);
bool queue_is_empty(const queue_t* queue);
bool queue_is_full(const queue_t* queue);
size_t queue_size(const queue_t* queue);

/* Deque (Double-ended queue) operations */
deque_t* deque_create(size_t capacity);
void deque_destroy(deque_t* deque);
bool deque_push_front(deque_t* deque, void* data);
bool deque_push_back(deque_t* deque, void* data);
void* deque_pop_front(deque_t* deque);
void* deque_pop_back(deque_t* deque);
void* deque_front(const deque_t* deque);
void* deque_back(const deque_t* deque);

/* Priority Queue operations */
priority_queue_t* pq_create(size_t capacity,
                            int (*compare)(const void*, const void*));
void pq_destroy(priority_queue_t* pq);
bool pq_insert(priority_queue_t* pq, void* data, int priority);
void* pq_extract(priority_queue_t* pq);
void* pq_peek(const priority_queue_t* pq);
bool pq_is_empty(const priority_queue_t* pq);
size_t pq_size(const priority_queue_t* pq);

/* Linked List operations */
linked_list_t* list_create(void);
void list_destroy(linked_list_t* list);
bool list_insert_front(linked_list_t* list, void* data);
bool list_insert_back(linked_list_t* list, void* data);
bool list_insert_at(linked_list_t* list, size_t index, void* data);
void* list_remove_front(linked_list_t* list);
void* list_remove_back(linked_list_t* list);
void* list_remove_at(linked_list_t* list, size_t index);
void* list_get(const linked_list_t* list, size_t index);
size_t list_size(const linked_list_t* list);
bool list_contains(const linked_list_t* list, const void* data,
                   int (*compare)(const void*, const void*));

/* Binary Search Tree operations */
bst_t* bst_create(int (*compare)(const void*, const void*));
void bst_destroy(bst_t* tree);
bool bst_insert(bst_t* tree, void* key, void* value);
void* bst_search(const bst_t* tree, const void* key);
bool bst_delete(bst_t* tree, const void* key);
void* bst_minimum(const bst_t* tree);
void* bst_maximum(const bst_t* tree);
size_t bst_size(const bst_t* tree);
size_t bst_height(const bst_t* tree);
void bst_inorder(const bst_t* tree, void (*callback)(void*, void*));
void bst_preorder(const bst_t* tree, void (*callback)(void*, void*));
void bst_postorder(const bst_t* tree, void (*callback)(void*, void*));

/* AVL Tree operations */
avl_tree_t* avl_create(int (*compare)(const void*, const void*));
void avl_destroy(avl_tree_t* tree);
bool avl_insert(avl_tree_t* tree, void* key, void* value);
void* avl_search(const avl_tree_t* tree, const void* key);
bool avl_delete(avl_tree_t* tree, const void* key);
bool avl_is_balanced(const avl_tree_t* tree);

/* Red-Black Tree operations */
red_black_tree_t* rbt_create(int (*compare)(const void*, const void*));
void rbt_destroy(red_black_tree_t* tree);
bool rbt_insert(red_black_tree_t* tree, void* key, void* value);
void* rbt_search(const red_black_tree_t* tree, const void* key);
bool rbt_delete(red_black_tree_t* tree, const void* key);

/* Trie operations */
trie_t* trie_create(void);
void trie_destroy(trie_t* trie);
bool trie_insert(trie_t* trie, const char* key, void* value);
void* trie_search(const trie_t* trie, const char* key);
bool trie_delete(trie_t* trie, const char* key);
bool trie_starts_with(const trie_t* trie, const char* prefix);
void trie_get_all_with_prefix(const trie_t* trie, const char* prefix,
                              char*** results, size_t* count);

/* Hash Table operations */
hash_table_t* ht_create(size_t capacity,
                        uint32_t (*hash)(const void*),
                        int (*compare)(const void*, const void*));
void ht_destroy(hash_table_t* table);
bool ht_insert(hash_table_t* table, void* key, void* value);
void* ht_get(const hash_table_t* table, const void* key);
bool ht_delete(hash_table_t* table, const void* key);
bool ht_contains(const hash_table_t* table, const void* key);
size_t ht_size(const hash_table_t* table);
double ht_load_factor(const hash_table_t* table);
void ht_rehash(hash_table_t* table, size_t new_capacity);

/* Disjoint Set (Union-Find) operations */
disjoint_set_t* ds_create(size_t n);
void ds_destroy(disjoint_set_t* ds);
size_t ds_find(disjoint_set_t* ds, size_t x);
void ds_union(disjoint_set_t* ds, size_t x, size_t y);
bool ds_connected(disjoint_set_t* ds, size_t x, size_t y);
size_t ds_count_sets(const disjoint_set_t* ds);

/* Segment Tree operations */
segment_tree_t* segtree_create(const int* arr, size_t n);
void segtree_destroy(segment_tree_t* tree);
int segtree_query(const segment_tree_t* tree, size_t left, size_t right);
void segtree_update(segment_tree_t* tree, size_t index, int value);
int segtree_range_sum(const segment_tree_t* tree, size_t left, size_t right);
int segtree_range_min(const segment_tree_t* tree, size_t left, size_t right);
int segtree_range_max(const segment_tree_t* tree, size_t left, size_t right);

/* Fenwick Tree (Binary Indexed Tree) operations */
fenwick_tree_t* fenwick_create(const int* arr, size_t n);
void fenwick_destroy(fenwick_tree_t* tree);
void fenwick_update(fenwick_tree_t* tree, size_t index, int delta);
int fenwick_query(const fenwick_tree_t* tree, size_t index);
int fenwick_range_query(const fenwick_tree_t* tree, size_t left, size_t right);

/* Heap operations */
heap_t* heap_create(size_t capacity, bool is_min_heap,
                    int (*compare)(const void*, const void*));
void heap_destroy(heap_t* heap);
bool heap_insert(heap_t* heap, void* data);
void* heap_extract(heap_t* heap);
void* heap_peek(const heap_t* heap);
bool heap_is_empty(const heap_t* heap);
size_t heap_size(const heap_t* heap);
void heap_build(heap_t* heap, void** arr, size_t n);

/* Common hash functions */
uint32_t hash_string_djb2(const void* key);
uint32_t hash_string_fnv1a(const void* key);
uint32_t hash_int(const void* key);
uint32_t hash_pointer(const void* key);

/* Common comparison functions */
int compare_int(const void* a, const void* b);
int compare_string(const void* a, const void* b);
int compare_double(const void* a, const void* b);

#ifdef __cplusplus
}
#endif

#endif /* AM_DATA_STRUCTURES_H */