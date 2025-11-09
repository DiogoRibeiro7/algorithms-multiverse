/**
 * Comprehensive Linked List Implementations in C
 *
 * Features:
 * - Manual memory management (malloc/free)
 * - All 4 variants: Singly, Doubly, Circular, Skip List
 * - Proper error handling
 * - Memory leak prevention
 *
 * Compilation:
 *   gcc -o linkedlist linkedlist.c -Wall -Wextra -std=c11
 *   ./linkedlist
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

// ============================================================================
// SINGLY LINKED LIST
// ============================================================================

typedef struct SinglyNode {
    int data;
    struct SinglyNode *next;
} SinglyNode;

typedef struct {
    SinglyNode *head;
    size_t size;
} SinglyLinkedList;

SinglyLinkedList* sll_create() {
    SinglyLinkedList *list = (SinglyLinkedList*)malloc(sizeof(SinglyLinkedList));
    if (!list) return NULL;
    list->head = NULL;
    list->size = 0;
    return list;
}

void sll_insert_at_head(SinglyLinkedList *list, int data) {
    SinglyNode *new_node = (SinglyNode*)malloc(sizeof(SinglyNode));
    if (!new_node) return;

    new_node->data = data;
    new_node->next = list->head;
    list->head = new_node;
    list->size++;
}

void sll_insert_at_tail(SinglyLinkedList *list, int data) {
    SinglyNode *new_node = (SinglyNode*)malloc(sizeof(SinglyNode));
    if (!new_node) return;

    new_node->data = data;
    new_node->next = NULL;

    if (!list->head) {
        list->head = new_node;
    } else {
        SinglyNode *current = list->head;
        while (current->next) {
            current = current->next;
        }
        current->next = new_node;
    }
    list->size++;
}

bool sll_delete_at_head(SinglyLinkedList *list, int *data) {
    if (!list->head) return false;

    SinglyNode *temp = list->head;
    *data = temp->data;
    list->head = list->head->next;
    free(temp);
    list->size--;
    return true;
}

bool sll_search(SinglyLinkedList *list, int value) {
    SinglyNode *current = list->head;
    while (current) {
        if (current->data == value) return true;
        current = current->next;
    }
    return false;
}

void sll_reverse(SinglyLinkedList *list) {
    SinglyNode *prev = NULL;
    SinglyNode *current = list->head;
    SinglyNode *next;

    while (current) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }

    list->head = prev;
}

int sll_get_middle(SinglyLinkedList *list) {
    if (!list->head) return -1;

    SinglyNode *slow = list->head;
    SinglyNode *fast = list->head;

    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    return slow->data;
}

void sll_print(SinglyLinkedList *list) {
    SinglyNode *current = list->head;
    while (current) {
        printf("%d", current->data);
        if (current->next) printf(" -> ");
        current = current->next;
    }
    printf(" -> NULL\n");
}

void sll_destroy(SinglyLinkedList *list) {
    SinglyNode *current = list->head;
    while (current) {
        SinglyNode *next = current->next;
        free(current);
        current = next;
    }
    free(list);
}

// ============================================================================
// DOUBLY LINKED LIST
// ============================================================================

typedef struct DoublyNode {
    int data;
    struct DoublyNode *next;
    struct DoublyNode *prev;
} DoublyNode;

typedef struct {
    DoublyNode *head;
    DoublyNode *tail;
    size_t size;
} DoublyLinkedList;

DoublyLinkedList* dll_create() {
    DoublyLinkedList *list = (DoublyLinkedList*)malloc(sizeof(DoublyLinkedList));
    if (!list) return NULL;
    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
    return list;
}

void dll_insert_at_head(DoublyLinkedList *list, int data) {
    DoublyNode *new_node = (DoublyNode*)malloc(sizeof(DoublyNode));
    if (!new_node) return;

    new_node->data = data;
    new_node->prev = NULL;
    new_node->next = list->head;

    if (list->head) {
        list->head->prev = new_node;
    } else {
        list->tail = new_node;
    }

    list->head = new_node;
    list->size++;
}

void dll_insert_at_tail(DoublyLinkedList *list, int data) {
    DoublyNode *new_node = (DoublyNode*)malloc(sizeof(DoublyNode));
    if (!new_node) return;

    new_node->data = data;
    new_node->next = NULL;
    new_node->prev = list->tail;

    if (list->tail) {
        list->tail->next = new_node;
    } else {
        list->head = new_node;
    }

    list->tail = new_node;
    list->size++;
}

bool dll_delete_at_head(DoublyLinkedList *list, int *data) {
    if (!list->head) return false;

    DoublyNode *temp = list->head;
    *data = temp->data;

    if (list->head == list->tail) {
        list->head = list->tail = NULL;
    } else {
        list->head = list->head->next;
        list->head->prev = NULL;
    }

    free(temp);
    list->size--;
    return true;
}

bool dll_delete_at_tail(DoublyLinkedList *list, int *data) {
    if (!list->tail) return false;

    DoublyNode *temp = list->tail;
    *data = temp->data;

    if (list->head == list->tail) {
        list->head = list->tail = NULL;
    } else {
        list->tail = list->tail->prev;
        list->tail->next = NULL;
    }

    free(temp);
    list->size--;
    return true;
}

void dll_print(DoublyLinkedList *list) {
    DoublyNode *current = list->head;
    while (current) {
        printf("%d", current->data);
        if (current->next) printf(" <-> ");
        current = current->next;
    }
    printf(" <-> NULL\n");
}

void dll_print_reverse(DoublyLinkedList *list) {
    DoublyNode *current = list->tail;
    while (current) {
        printf("%d", current->data);
        if (current->prev) printf(" <-> ");
        current = current->prev;
    }
    printf(" <-> NULL\n");
}

void dll_destroy(DoublyLinkedList *list) {
    DoublyNode *current = list->head;
    while (current) {
        DoublyNode *next = current->next;
        free(current);
        current = next;
    }
    free(list);
}

// ============================================================================
// CIRCULAR LINKED LIST
// ============================================================================

typedef struct {
    SinglyNode *head;
    size_t size;
} CircularLinkedList;

CircularLinkedList* cll_create() {
    CircularLinkedList *list = (CircularLinkedList*)malloc(sizeof(CircularLinkedList));
    if (!list) return NULL;
    list->head = NULL;
    list->size = 0;
    return list;
}

void cll_insert_at_tail(CircularLinkedList *list, int data) {
    SinglyNode *new_node = (SinglyNode*)malloc(sizeof(SinglyNode));
    if (!new_node) return;

    new_node->data = data;

    if (!list->head) {
        new_node->next = new_node;  // Point to itself
        list->head = new_node;
    } else {
        SinglyNode *current = list->head;
        while (current->next != list->head) {
            current = current->next;
        }
        current->next = new_node;
        new_node->next = list->head;
    }
    list->size++;
}

void cll_print(CircularLinkedList *list) {
    if (!list->head) {
        printf("Empty\n");
        return;
    }

    SinglyNode *current = list->head;
    do {
        printf("%d", current->data);
        current = current->next;
        if (current != list->head) printf(" -> ");
    } while (current != list->head);
    printf(" -> (head)\n");
}

void cll_destroy(CircularLinkedList *list) {
    if (!list->head) {
        free(list);
        return;
    }

    SinglyNode *current = list->head;
    SinglyNode *first = list->head;

    do {
        SinglyNode *next = current->next;
        free(current);
        current = next;
    } while (current != first);

    free(list);
}

// ============================================================================
// SKIP LIST
// ============================================================================

#define MAX_LEVEL 16
#define P 0.5

typedef struct SkipNode {
    int data;
    struct SkipNode **forward;
} SkipNode;

typedef struct {
    SkipNode *header;
    int level;
    size_t size;
} SkipList;

int random_level() {
    int lvl = 0;
    while ((double)rand() / RAND_MAX < P && lvl < MAX_LEVEL) {
        lvl++;
    }
    return lvl;
}

SkipList* sl_create() {
    SkipList *list = (SkipList*)malloc(sizeof(SkipList));
    if (!list) return NULL;

    list->header = (SkipNode*)malloc(sizeof(SkipNode));
    list->header->forward = (SkipNode**)calloc(MAX_LEVEL + 1, sizeof(SkipNode*));
    list->level = 0;
    list->size = 0;

    return list;
}

void sl_insert(SkipList *list, int data) {
    SkipNode *update[MAX_LEVEL + 1];
    SkipNode *current = list->header;

    for (int i = list->level; i >= 0; i--) {
        while (current->forward[i] && current->forward[i]->data < data) {
            current = current->forward[i];
        }
        update[i] = current;
    }

    int new_level = random_level();

    if (new_level > list->level) {
        for (int i = list->level + 1; i <= new_level; i++) {
            update[i] = list->header;
        }
        list->level = new_level;
    }

    SkipNode *new_node = (SkipNode*)malloc(sizeof(SkipNode));
    new_node->data = data;
    new_node->forward = (SkipNode**)calloc(new_level + 1, sizeof(SkipNode*));

    for (int i = 0; i <= new_level; i++) {
        new_node->forward[i] = update[i]->forward[i];
        update[i]->forward[i] = new_node;
    }

    list->size++;
}

bool sl_search(SkipList *list, int data) {
    SkipNode *current = list->header;

    for (int i = list->level; i >= 0; i--) {
        while (current->forward[i] && current->forward[i]->data < data) {
            current = current->forward[i];
        }
    }

    current = current->forward[0];
    return current && current->data == data;
}

void sl_print(SkipList *list) {
    printf("SkipList[");
    SkipNode *current = list->header->forward[0];
    while (current) {
        printf("%d", current->data);
        if (current->forward[0]) printf(", ");
        current = current->forward[0];
    }
    printf("]\n");
}

void sl_destroy(SkipList *list) {
    SkipNode *current = list->header->forward[0];
    while (current) {
        SkipNode *next = current->forward[0];
        free(current->forward);
        free(current);
        current = next;
    }
    free(list->header->forward);
    free(list->header);
    free(list);
}

// ============================================================================
// DEMONSTRATION
// ============================================================================

int main() {
    srand(time(NULL));

    printf("================================================================================\n");
    printf("COMPREHENSIVE LINKED LIST DEMONSTRATIONS IN C\n");
    printf("================================================================================\n");

    // Singly Linked List
    printf("\n1. SINGLY LINKED LIST\n");
    printf("--------------------------------------------------------------------------------\n");
    SinglyLinkedList *sll = sll_create();

    printf("Inserting: 1, 2, 3 at head\n");
    sll_insert_at_head(sll, 3);
    sll_insert_at_head(sll, 2);
    sll_insert_at_head(sll, 1);
    printf("List: ");
    sll_print(sll);

    printf("\nInserting: 4, 5 at tail\n");
    sll_insert_at_tail(sll, 4);
    sll_insert_at_tail(sll, 5);
    printf("List: ");
    sll_print(sll);

    printf("\nMiddle element: %d\n", sll_get_middle(sll));

    printf("\nReversing list...\n");
    sll_reverse(sll);
    printf("List: ");
    sll_print(sll);

    // Doubly Linked List
    printf("\n2. DOUBLY LINKED LIST\n");
    printf("--------------------------------------------------------------------------------\n");
    DoublyLinkedList *dll = dll_create();

    printf("Inserting: 10, 20, 30 at head\n");
    dll_insert_at_head(dll, 30);
    dll_insert_at_head(dll, 20);
    dll_insert_at_head(dll, 10);
    printf("List: ");
    dll_print(dll);

    printf("\nInserting: 40, 50 at tail\n");
    dll_insert_at_tail(dll, 40);
    dll_insert_at_tail(dll, 50);
    printf("List: ");
    dll_print(dll);

    printf("\nReverse iteration: ");
    dll_print_reverse(dll);

    // Circular Linked List
    printf("\n3. CIRCULAR LINKED LIST\n");
    printf("--------------------------------------------------------------------------------\n");
    CircularLinkedList *cll = cll_create();

    printf("Inserting: 1, 2, 3, 4, 5\n");
    for (int i = 1; i <= 5; i++) {
        cll_insert_at_tail(cll, i);
    }
    printf("List: ");
    cll_print(cll);

    // Skip List
    printf("\n4. SKIP LIST\n");
    printf("--------------------------------------------------------------------------------\n");
    SkipList *sl = sl_create();

    printf("Inserting: 3, 7, 1, 9, 5, 2, 8, 4, 6\n");
    int values[] = {3, 7, 1, 9, 5, 2, 8, 4, 6};
    for (int i = 0; i < 9; i++) {
        sl_insert(sl, values[i]);
    }

    printf("Skip list (sorted): ");
    sl_print(sl);

    printf("\nSearching for 5: %s\n", sl_search(sl, 5) ? "found" : "not found");
    printf("Searching for 10: %s\n", sl_search(sl, 10) ? "found" : "not found");

    // Cleanup
    sll_destroy(sll);
    dll_destroy(dll);
    cll_destroy(cll);
    sl_destroy(sl);

    printf("\n================================================================================\n");
    printf("✨ All demonstrations complete! Memory properly freed.\n");
    printf("================================================================================\n");

    return 0;
}
