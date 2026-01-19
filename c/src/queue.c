/**
 * @file queue.c
 * @brief Implementation of queue data structure
 */

#include "data_structures.h"
#include <stdlib.h>
#include <string.h>

/* Queue structure definition */
struct queue {
    void** data;
    size_t front;
    size_t rear;
    size_t size;
    size_t capacity;
};

/* Create a new queue */
queue_t* queue_create(size_t capacity) {
    if (capacity == 0) return NULL;

    queue_t* queue = malloc(sizeof(queue_t));
    if (!queue) return NULL;

    queue->data = calloc(capacity, sizeof(void*));
    if (!queue->data) {
        free(queue);
        return NULL;
    }

    queue->front = 0;
    queue->rear = 0;
    queue->size = 0;
    queue->capacity = capacity;

    return queue;
}

/* Destroy a queue */
void queue_destroy(queue_t* queue) {
    if (!queue) return;

    free(queue->data);
    free(queue);
}

/* Enqueue element */
bool queue_enqueue(queue_t* queue, void* data) {
    if (!queue) return false;

    if (queue->size >= queue->capacity) {
        return false;  /* Queue is full */
    }

    queue->data[queue->rear] = data;
    queue->rear = (queue->rear + 1) % queue->capacity;
    queue->size++;

    return true;
}

/* Dequeue element */
void* queue_dequeue(queue_t* queue) {
    if (!queue || queue->size == 0) return NULL;

    void* data = queue->data[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    queue->size--;

    return data;
}

/* Peek at front element */
void* queue_front(const queue_t* queue) {
    if (!queue || queue->size == 0) return NULL;

    return queue->data[queue->front];
}

/* Peek at rear element */
void* queue_rear(const queue_t* queue) {
    if (!queue || queue->size == 0) return NULL;

    size_t rear_index = (queue->rear == 0) ? queue->capacity - 1 : queue->rear - 1;
    return queue->data[rear_index];
}

/* Check if queue is empty */
bool queue_is_empty(const queue_t* queue) {
    return !queue || queue->size == 0;
}

/* Check if queue is full */
bool queue_is_full(const queue_t* queue) {
    return queue && queue->size >= queue->capacity;
}

/* Get queue size */
size_t queue_size(const queue_t* queue) {
    return queue ? queue->size : 0;
}

/* Deque structure definition */
struct deque {
    void** data;
    size_t front;
    size_t rear;
    size_t size;
    size_t capacity;
};

/* Create a new deque */
deque_t* deque_create(size_t capacity) {
    if (capacity == 0) return NULL;

    deque_t* deque = malloc(sizeof(deque_t));
    if (!deque) return NULL;

    deque->data = calloc(capacity, sizeof(void*));
    if (!deque->data) {
        free(deque);
        return NULL;
    }

    deque->front = 0;
    deque->rear = 0;
    deque->size = 0;
    deque->capacity = capacity;

    return deque;
}

/* Destroy a deque */
void deque_destroy(deque_t* deque) {
    if (!deque) return;

    free(deque->data);
    free(deque);
}

/* Push element to front */
bool deque_push_front(deque_t* deque, void* data) {
    if (!deque || deque->size >= deque->capacity) return false;

    deque->front = (deque->front == 0) ? deque->capacity - 1 : deque->front - 1;
    deque->data[deque->front] = data;
    deque->size++;

    return true;
}

/* Push element to back */
bool deque_push_back(deque_t* deque, void* data) {
    if (!deque || deque->size >= deque->capacity) return false;

    deque->data[deque->rear] = data;
    deque->rear = (deque->rear + 1) % deque->capacity;
    deque->size++;

    return true;
}

/* Pop element from front */
void* deque_pop_front(deque_t* deque) {
    if (!deque || deque->size == 0) return NULL;

    void* data = deque->data[deque->front];
    deque->front = (deque->front + 1) % deque->capacity;
    deque->size--;

    return data;
}

/* Pop element from back */
void* deque_pop_back(deque_t* deque) {
    if (!deque || deque->size == 0) return NULL;

    deque->rear = (deque->rear == 0) ? deque->capacity - 1 : deque->rear - 1;
    void* data = deque->data[deque->rear];
    deque->size--;

    return data;
}

/* Peek at front element */
void* deque_front(const deque_t* deque) {
    if (!deque || deque->size == 0) return NULL;

    return deque->data[deque->front];
}

/* Peek at back element */
void* deque_back(const deque_t* deque) {
    if (!deque || deque->size == 0) return NULL;

    size_t rear_index = (deque->rear == 0) ? deque->capacity - 1 : deque->rear - 1;
    return deque->data[rear_index];
}

/* Priority Queue structure definition */
struct priority_queue {
    void** data;
    int* priorities;
    size_t size;
    size_t capacity;
    int (*compare)(const void*, const void*);
    bool is_min_heap;
};

/* Create a priority queue */
priority_queue_t* pq_create(size_t capacity,
                            int (*compare)(const void*, const void*)) {
    if (capacity == 0) return NULL;

    priority_queue_t* pq = malloc(sizeof(priority_queue_t));
    if (!pq) return NULL;

    pq->data = calloc(capacity + 1, sizeof(void*));  /* 1-indexed for easier heap operations */
    pq->priorities = calloc(capacity + 1, sizeof(int));

    if (!pq->data || !pq->priorities) {
        free(pq->data);
        free(pq->priorities);
        free(pq);
        return NULL;
    }

    pq->size = 0;
    pq->capacity = capacity;
    pq->compare = compare;
    pq->is_min_heap = true;

    return pq;
}

/* Destroy priority queue */
void pq_destroy(priority_queue_t* pq) {
    if (!pq) return;

    free(pq->data);
    free(pq->priorities);
    free(pq);
}

/* Helper function to maintain heap property upward */
static void pq_bubble_up(priority_queue_t* pq, size_t index) {
    while (index > 1) {
        size_t parent = index / 2;

        bool should_swap = pq->is_min_heap ?
            (pq->priorities[index] < pq->priorities[parent]) :
            (pq->priorities[index] > pq->priorities[parent]);

        if (should_swap) {
            /* Swap with parent */
            void* temp_data = pq->data[index];
            pq->data[index] = pq->data[parent];
            pq->data[parent] = temp_data;

            int temp_priority = pq->priorities[index];
            pq->priorities[index] = pq->priorities[parent];
            pq->priorities[parent] = temp_priority;

            index = parent;
        } else {
            break;
        }
    }
}

/* Helper function to maintain heap property downward */
static void pq_bubble_down(priority_queue_t* pq, size_t index) {
    while (2 * index <= pq->size) {
        size_t left_child = 2 * index;
        size_t right_child = 2 * index + 1;
        size_t swap_index = left_child;

        if (right_child <= pq->size) {
            bool right_is_better = pq->is_min_heap ?
                (pq->priorities[right_child] < pq->priorities[left_child]) :
                (pq->priorities[right_child] > pq->priorities[left_child]);

            if (right_is_better) {
                swap_index = right_child;
            }
        }

        bool should_swap = pq->is_min_heap ?
            (pq->priorities[swap_index] < pq->priorities[index]) :
            (pq->priorities[swap_index] > pq->priorities[index]);

        if (should_swap) {
            /* Swap with child */
            void* temp_data = pq->data[index];
            pq->data[index] = pq->data[swap_index];
            pq->data[swap_index] = temp_data;

            int temp_priority = pq->priorities[index];
            pq->priorities[index] = pq->priorities[swap_index];
            pq->priorities[swap_index] = temp_priority;

            index = swap_index;
        } else {
            break;
        }
    }
}

/* Insert element with priority */
bool pq_insert(priority_queue_t* pq, void* data, int priority) {
    if (!pq || pq->size >= pq->capacity) return false;

    pq->size++;
    pq->data[pq->size] = data;
    pq->priorities[pq->size] = priority;

    pq_bubble_up(pq, pq->size);

    return true;
}

/* Extract element with highest priority */
void* pq_extract(priority_queue_t* pq) {
    if (!pq || pq->size == 0) return NULL;

    void* result = pq->data[1];

    /* Move last element to root */
    pq->data[1] = pq->data[pq->size];
    pq->priorities[1] = pq->priorities[pq->size];
    pq->size--;

    if (pq->size > 0) {
        pq_bubble_down(pq, 1);
    }

    return result;
}

/* Peek at highest priority element */
void* pq_peek(const priority_queue_t* pq) {
    if (!pq || pq->size == 0) return NULL;

    return pq->data[1];
}

/* Check if priority queue is empty */
bool pq_is_empty(const priority_queue_t* pq) {
    return !pq || pq->size == 0;
}

/* Get priority queue size */
size_t pq_size(const priority_queue_t* pq) {
    return pq ? pq->size : 0;
}