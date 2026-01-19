/**
 * @file algorithms_multiverse.c
 * @brief Main library implementation and utility functions
 */

#include "algorithms_multiverse.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/time.h>
#endif

/* Library version information */
static const char* library_version = ALGORITHMS_MULTIVERSE_VERSION;
static bool library_initialized = false;

/* Memory tracking for debugging */
static struct {
    size_t allocations;
    size_t deallocations;
    size_t total_bytes;
    size_t peak_bytes;
    size_t current_bytes;
} memory_stats = {0};

/* Initialize the library */
am_result_t am_init(void) {
    if (library_initialized) {
        return AM_SUCCESS;
    }

    /* Initialize random number generator */
    srand(time(NULL));

    /* Reset memory statistics */
    memset(&memory_stats, 0, sizeof(memory_stats));

    library_initialized = true;

    return AM_SUCCESS;
}

/* Clean up library resources */
am_result_t am_cleanup(void) {
    if (!library_initialized) {
        return AM_SUCCESS;
    }

    library_initialized = false;

    return AM_SUCCESS;
}

/* Get library version string */
const char* am_get_version(void) {
    return library_version;
}

/* Set random seed */
void am_set_random_seed(unsigned int seed) {
    srand(seed);
    random_seed(seed);
}

/* Allocate aligned memory */
void* am_aligned_alloc(size_t size, size_t alignment) {
    if (size == 0 || alignment == 0) {
        return NULL;
    }

    /* Ensure alignment is a power of 2 */
    if ((alignment & (alignment - 1)) != 0) {
        return NULL;
    }

    void* ptr = NULL;

#ifdef _WIN32
    ptr = _aligned_malloc(size, alignment);
#elif defined(__APPLE__) || defined(__FreeBSD__)
    /* macOS and FreeBSD don't have aligned_alloc in older versions */
    if (posix_memalign(&ptr, alignment, size) != 0) {
        return NULL;
    }
#else
    /* Linux and other systems with C11 support */
    ptr = aligned_alloc(alignment, size);
#endif

    if (ptr) {
        memory_stats.allocations++;
        memory_stats.total_bytes += size;
        memory_stats.current_bytes += size;
        if (memory_stats.current_bytes > memory_stats.peak_bytes) {
            memory_stats.peak_bytes = memory_stats.current_bytes;
        }
    }

    return ptr;
}

/* Free aligned memory */
void am_aligned_free(void* ptr) {
    if (!ptr) {
        return;
    }

#ifdef _WIN32
    _aligned_free(ptr);
#else
    free(ptr);
#endif

    memory_stats.deallocations++;
}

/* Get current time in microseconds */
uint64_t am_get_time_us(void) {
#ifdef _WIN32
    LARGE_INTEGER frequency, counter;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&counter);
    return (uint64_t)((counter.QuadPart * 1000000) / frequency.QuadPart);
#else
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (uint64_t)tv.tv_sec * 1000000 + tv.tv_usec;
#endif
}

/* Print memory usage statistics */
void am_print_memory_stats(void) {
    printf("=== Memory Statistics ===\n");
    printf("Allocations:     %zu\n", memory_stats.allocations);
    printf("Deallocations:   %zu\n", memory_stats.deallocations);
    printf("Total allocated: %zu bytes\n", memory_stats.total_bytes);
    printf("Peak usage:      %zu bytes\n", memory_stats.peak_bytes);
    printf("Current usage:   %zu bytes\n", memory_stats.current_bytes);

    if (memory_stats.allocations != memory_stats.deallocations) {
        printf("WARNING: Possible memory leak detected!\n");
        printf("         %zu unfreed allocations\n",
               memory_stats.allocations - memory_stats.deallocations);
    }
}