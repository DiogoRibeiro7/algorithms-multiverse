/**
 * @file stack.c
 * @brief Implementation of stack data structure
 */

#include "data_structures.h"
#include <stdlib.h>
#include <string.h>

/* Stack structure definition */
struct stack {
    void** data;
    size_t top;
    size_t capacity;
};

/* Create a new stack */
stack_t* stack_create(size_t capacity) {
    if (capacity == 0) return NULL;

    stack_t* stack = malloc(sizeof(stack_t));
    if (!stack) return NULL;

    stack->data = calloc(capacity, sizeof(void*));
    if (!stack->data) {
        free(stack);
        return NULL;
    }

    stack->top = 0;
    stack->capacity = capacity;

    return stack;
}

/* Destroy a stack */
void stack_destroy(stack_t* stack) {
    if (!stack) return;

    free(stack->data);
    free(stack);
}

/* Push element onto stack */
bool stack_push(stack_t* stack, void* data) {
    if (!stack) return false;

    if (stack->top >= stack->capacity) {
        return false;  /* Stack is full */
    }

    stack->data[stack->top++] = data;
    return true;
}

/* Pop element from stack */
void* stack_pop(stack_t* stack) {
    if (!stack || stack->top == 0) return NULL;

    return stack->data[--stack->top];
}

/* Peek at top element */
void* stack_peek(const stack_t* stack) {
    if (!stack || stack->top == 0) return NULL;

    return stack->data[stack->top - 1];
}

/* Check if stack is empty */
bool stack_is_empty(const stack_t* stack) {
    return !stack || stack->top == 0;
}

/* Check if stack is full */
bool stack_is_full(const stack_t* stack) {
    return stack && stack->top >= stack->capacity;
}

/* Get stack size */
size_t stack_size(const stack_t* stack) {
    return stack ? stack->top : 0;
}

/* Clear the stack */
void stack_clear(stack_t* stack) {
    if (stack) {
        stack->top = 0;
    }
}