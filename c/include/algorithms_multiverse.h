/**
 * @file algorithms_multiverse.h
 * @brief Main header file for Algorithms Multiverse C implementation
 * @author Algorithms Multiverse
 * @version 1.0.0
 *
 * This header provides the complete interface to all algorithm implementations
 * including sorting, searching, data structures, graph algorithms, and more.
 */

#ifndef ALGORITHMS_MULTIVERSE_H
#define ALGORITHMS_MULTIVERSE_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Module version information */
#define ALGORITHMS_MULTIVERSE_VERSION "1.0.0"
#define ALGORITHMS_MULTIVERSE_VERSION_MAJOR 1
#define ALGORITHMS_MULTIVERSE_VERSION_MINOR 0
#define ALGORITHMS_MULTIVERSE_VERSION_PATCH 0

/* Common type definitions */
typedef int (*compare_func)(const void*, const void*);
typedef uint32_t (*hash_func)(const void*);
typedef void (*free_func)(void*);
typedef void* (*copy_func)(const void*);

/* Result codes */
typedef enum {
    AM_SUCCESS = 0,
    AM_ERROR_NULL_PARAM = -1,
    AM_ERROR_INVALID_PARAM = -2,
    AM_ERROR_OUT_OF_MEMORY = -3,
    AM_ERROR_NOT_FOUND = -4,
    AM_ERROR_OVERFLOW = -5,
    AM_ERROR_UNDERFLOW = -6,
    AM_ERROR_EMPTY = -7,
    AM_ERROR_FULL = -8
} am_result_t;

/* Include all module headers */
#include "sorting.h"
#include "searching.h"
#include "data_structures.h"
#include "graph.h"
#include "string_algorithms.h"
#include "numerical.h"
#include "dynamic_programming.h"
#include "geometry.h"
#include "cryptography.h"
#include "matrix.h"
#include "statistics.h"
#include "optimization.h"
#include "streaming.h"

/* Utility functions */

/**
 * @brief Initialize the library
 * @return AM_SUCCESS on success
 */
am_result_t am_init(void);

/**
 * @brief Clean up library resources
 * @return AM_SUCCESS on success
 */
am_result_t am_cleanup(void);

/**
 * @brief Get library version string
 * @return Version string
 */
const char* am_get_version(void);

/**
 * @brief Set random seed for algorithms that use randomization
 * @param seed Random seed value
 */
void am_set_random_seed(unsigned int seed);

/**
 * @brief Allocate aligned memory
 * @param size Size in bytes
 * @param alignment Alignment requirement
 * @return Pointer to allocated memory or NULL
 */
void* am_aligned_alloc(size_t size, size_t alignment);

/**
 * @brief Free aligned memory
 * @param ptr Pointer to free
 */
void am_aligned_free(void* ptr);

/**
 * @brief Get current time in microseconds (for benchmarking)
 * @return Time in microseconds
 */
uint64_t am_get_time_us(void);

/**
 * @brief Print memory usage statistics
 */
void am_print_memory_stats(void);

#ifdef __cplusplus
}
#endif

#endif /* ALGORITHMS_MULTIVERSE_H */