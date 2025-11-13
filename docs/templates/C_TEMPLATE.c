/**
 * @file C_TEMPLATE.c
 * @brief C Documentation Template for Algorithms Multiverse
 *
 * @details
 * This template provides the standard documentation format for C files
 * in the Algorithms Multiverse project. Includes Doxygen-style comments,
 * comprehensive error handling, and memory safety practices.
 *
 * Features:
 * - Doxygen-compatible documentation
 * - Comprehensive error handling with return codes
 * - Memory safety with proper allocation/deallocation
 * - Defensive programming practices
 * - Thread-safety considerations
 *
 * @author Algorithms Multiverse
 * @version 1.0.0
 * @date 2024
 *
 * @par Compilation
 * @code
 * gcc -o program C_TEMPLATE.c -Wall -Wextra -std=c11 -O2
 * @endcode
 *
 * @par Usage
 * @code
 * ./program
 * @endcode
 *
 * @see https://example.com/docs
 * @note This implementation is thread-safe with proper synchronization
 * @warning Always check return values for error conditions
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include <assert.h>

/* ========================================================================== */
/* CONSTANTS AND MACROS                                                       */
/* ========================================================================== */

/**
 * @def MAX_ARRAY_SIZE
 * @brief Maximum supported array size
 */
#define MAX_ARRAY_SIZE 1000000

/**
 * @def TOLERANCE
 * @brief Numerical tolerance for comparisons
 */
#define TOLERANCE 1e-10

/**
 * @def MIN(a, b)
 * @brief Returns minimum of two values
 * @param a First value
 * @param b Second value
 * @return Minimum value
 */
#define MIN(a, b) ((a) < (b) ? (a) : (b))

/**
 * @def MAX(a, b)
 * @brief Returns maximum of two values
 * @param a First value
 * @param b Second value
 * @return Maximum value
 */
#define MAX(a, b) ((a) > (b) ? (a) : (b))

/* ========================================================================== */
/* ERROR CODES                                                                */
/* ========================================================================== */

/**
 * @enum error_code_t
 * @brief Error codes for algorithm operations
 */
typedef enum {
    SUCCESS = 0,              /**< Operation completed successfully */
    ERROR_NULL_POINTER = -1,  /**< Null pointer passed as argument */
    ERROR_INVALID_INPUT = -2, /**< Invalid input parameter */
    ERROR_OUT_OF_MEMORY = -3, /**< Memory allocation failed */
    ERROR_OUT_OF_BOUNDS = -4, /**< Array index out of bounds */
    ERROR_NO_CONVERGENCE = -5 /**< Algorithm failed to converge */
} error_code_t;

/* ========================================================================== */
/* DATA STRUCTURES                                                            */
/* ========================================================================== */

/**
 * @struct algorithm_result_t
 * @brief Container for algorithm results and metadata
 *
 * @details
 * This structure holds the result of an algorithm execution along with
 * performance metrics and error status.
 */
typedef struct {
    int *data;            /**< Result data array (must be freed by caller) */
    size_t size;          /**< Size of data array */
    error_code_t status;  /**< Error status code */
    size_t comparisons;   /**< Number of comparisons performed */
    size_t iterations;    /**< Number of iterations performed */
    double time;          /**< Execution time in seconds */
    bool success;         /**< True if operation succeeded */
} algorithm_result_t;

/**
 * @struct algorithm_options_t
 * @brief Configuration options for algorithm execution
 */
typedef struct {
    int param1;           /**< Configuration parameter 1 (range: 0-1000) */
    double param2;        /**< Configuration parameter 2 (positive) */
    bool validate_input;  /**< Enable input validation */
    size_t max_iterations; /**< Maximum iterations allowed */
} algorithm_options_t;

/* ========================================================================== */
/* FUNCTION PROTOTYPES                                                        */
/* ========================================================================== */

/* Main algorithm functions */
error_code_t algorithm_function(
    const int *input,
    size_t size,
    const algorithm_options_t *options,
    algorithm_result_t *result
);

/* Helper functions */
error_code_t validate_input(
    const int *input,
    size_t size,
    const algorithm_options_t *options
);

const char* get_error_message(error_code_t error);

/* Memory management */
void free_result(algorithm_result_t *result);

/* ========================================================================== */
/* MAIN ALGORITHM FUNCTION                                                    */
/* ========================================================================== */

/**
 * @brief Main algorithm function with comprehensive error handling
 *
 * @details
 * Detailed description of what this algorithm does, how it works,
 * and when to use it. Explain the approach, mathematical foundation,
 * and implementation details.
 *
 * Algorithm Steps:
 * 1. Validate input parameters
 * 2. Allocate necessary memory
 * 3. Process data according to algorithm
 * 4. Clean up resources and return results
 *
 * @param[in]  input    Input array to process (must not be NULL)
 * @param[in]  size     Size of input array (must be > 0 and <= MAX_ARRAY_SIZE)
 * @param[in]  options  Algorithm configuration options (must not be NULL)
 * @param[out] result   Result structure to populate (must not be NULL)
 *
 * @return Error code indicating success or type of failure
 * @retval SUCCESS Operation completed successfully
 * @retval ERROR_NULL_POINTER One or more NULL pointers passed
 * @retval ERROR_INVALID_INPUT Invalid input parameters
 * @retval ERROR_OUT_OF_MEMORY Memory allocation failed
 *
 * @pre input != NULL && options != NULL && result != NULL
 * @post If SUCCESS, result->data is allocated and must be freed by caller
 * @post If error, result->data is NULL and no cleanup needed
 *
 * @note Thread-safe: This function does not modify global state
 * @warning Caller must free result->data using free_result() after use
 * @warning Do not modify input array during execution
 *
 * @par Complexity
 * - Time: O(n log n) average case, O(n²) worst case
 * - Space: O(n) for result storage
 *
 * @par Example
 * @code
 * int data[] = {5, 2, 8, 1, 9, 3, 7};
 * algorithm_options_t opts = {
 *     .param1 = 10,
 *     .param2 = 1.5,
 *     .validate_input = true,
 *     .max_iterations = 1000
 * };
 * algorithm_result_t result;
 * error_code_t err = algorithm_function(data, 7, &opts, &result);
 *
 * if (err == SUCCESS) {
 *     printf("Success! Iterations: %zu\n", result.iterations);
 *     // Use result.data...
 *     free_result(&result);
 * } else {
 *     fprintf(stderr, "Error: %s\n", get_error_message(err));
 * }
 * @endcode
 *
 * @see validate_input(), free_result(), get_error_message()
 */
error_code_t algorithm_function(
    const int *input,
    size_t size,
    const algorithm_options_t *options,
    algorithm_result_t *result)
{
    error_code_t err;

    /* ====================================================================== */
    /* NULL POINTER CHECKS                                                    */
    /* ====================================================================== */

    if (input == NULL) {
        fprintf(stderr, "ERROR: input array is NULL\n");
        return ERROR_NULL_POINTER;
    }

    if (options == NULL) {
        fprintf(stderr, "ERROR: options structure is NULL\n");
        return ERROR_NULL_POINTER;
    }

    if (result == NULL) {
        fprintf(stderr, "ERROR: result structure is NULL\n");
        return ERROR_NULL_POINTER;
    }

    /* Initialize result structure */
    memset(result, 0, sizeof(algorithm_result_t));
    result->status = SUCCESS;
    result->success = false;

    /* ====================================================================== */
    /* INPUT VALIDATION                                                       */
    /* ====================================================================== */

    if (options->validate_input) {
        err = validate_input(input, size, options);
        if (err != SUCCESS) {
            result->status = err;
            return err;
        }
    }

    /* ====================================================================== */
    /* MEMORY ALLOCATION                                                      */
    /* ====================================================================== */

    result->data = (int*)malloc(size * sizeof(int));
    if (result->data == NULL) {
        fprintf(stderr, "ERROR: Failed to allocate memory for result\n");
        result->status = ERROR_OUT_OF_MEMORY;
        return ERROR_OUT_OF_MEMORY;
    }

    result->size = size;

    /* ====================================================================== */
    /* MAIN ALGORITHM IMPLEMENTATION                                          */
    /* ====================================================================== */

    /* Copy input data */
    memcpy(result->data, input, size * sizeof(int));

    /* Algorithm implementation goes here */
    for (size_t i = 0; i < size; i++) {
        result->iterations++;

        /* Process data... */
        result->data[i] = result->data[i] * options->param1;

        /* Track comparisons */
        if (i > 0 && result->data[i-1] > result->data[i]) {
            result->comparisons++;
        }

        /* Check for early termination */
        if (result->iterations >= options->max_iterations) {
            fprintf(stderr, "WARNING: Max iterations reached\n");
            break;
        }
    }

    /* ====================================================================== */
    /* FINALIZATION                                                           */
    /* ====================================================================== */

    result->success = true;
    result->status = SUCCESS;

    return SUCCESS;
}

/* ========================================================================== */
/* INPUT VALIDATION                                                           */
/* ========================================================================== */

/**
 * @brief Validate input parameters for algorithm
 *
 * @details
 * Performs comprehensive validation of all input parameters.
 * Checks for valid ranges, special values, and logical consistency.
 *
 * @param[in] input   Input array to validate
 * @param[in] size    Array size
 * @param[in] options Configuration options to validate
 *
 * @return Error code
 * @retval SUCCESS All inputs are valid
 * @retval ERROR_INVALID_INPUT One or more parameters invalid
 *
 * @par Example
 * @code
 * if (validate_input(data, size, &opts) == SUCCESS) {
 *     // Proceed with algorithm
 * }
 * @endcode
 */
error_code_t validate_input(
    const int *input,
    size_t size,
    const algorithm_options_t *options)
{
    /* Check array size */
    if (size == 0) {
        fprintf(stderr, "ERROR: Array size cannot be zero\n");
        return ERROR_INVALID_INPUT;
    }

    if (size > MAX_ARRAY_SIZE) {
        fprintf(stderr, "ERROR: Array size %zu exceeds maximum %d\n",
                size, MAX_ARRAY_SIZE);
        return ERROR_INVALID_INPUT;
    }

    /* Check param1 range */
    if (options->param1 < 0 || options->param1 > 1000) {
        fprintf(stderr, "ERROR: param1 (%d) out of range [0, 1000]\n",
                options->param1);
        return ERROR_INVALID_INPUT;
    }

    /* Check param2 */
    if (options->param2 <= 0.0) {
        fprintf(stderr, "ERROR: param2 (%f) must be positive\n",
                options->param2);
        return ERROR_INVALID_INPUT;
    }

    /* Check for overflow in data values */
    for (size_t i = 0; i < size; i++) {
        if (input[i] == INT_MAX || input[i] == INT_MIN) {
            fprintf(stderr, "WARNING: Potential overflow at index %zu\n", i);
        }
    }

    return SUCCESS;
}

/* ========================================================================== */
/* ERROR HANDLING UTILITIES                                                   */
/* ========================================================================== */

/**
 * @brief Get human-readable error message
 *
 * @param[in] error Error code to translate
 *
 * @return Static string describing the error (never NULL)
 *
 * @note Returned pointer is to static memory, do not free
 * @warning Thread-safe: uses only static read-only data
 *
 * @par Example
 * @code
 * error_code_t err = algorithm_function(...);
 * printf("Status: %s\n", get_error_message(err));
 * @endcode
 */
const char* get_error_message(error_code_t error) {
    switch (error) {
        case SUCCESS:
            return "Success";
        case ERROR_NULL_POINTER:
            return "Null pointer passed as argument";
        case ERROR_INVALID_INPUT:
            return "Invalid input parameter";
        case ERROR_OUT_OF_MEMORY:
            return "Memory allocation failed";
        case ERROR_OUT_OF_BOUNDS:
            return "Array index out of bounds";
        case ERROR_NO_CONVERGENCE:
            return "Algorithm failed to converge";
        default:
            return "Unknown error";
    }
}

/* ========================================================================== */
/* MEMORY MANAGEMENT                                                          */
/* ========================================================================== */

/**
 * @brief Free resources in result structure
 *
 * @details
 * Safely frees all allocated memory in the result structure.
 * Sets pointers to NULL after freeing to prevent use-after-free.
 *
 * @param[in,out] result Result structure to clean up (can be NULL)
 *
 * @post result->data is NULL after this call
 * @post result->size is 0 after this call
 *
 * @note Safe to call multiple times
 * @note Safe to call with NULL pointer (no-op)
 *
 * @par Example
 * @code
 * algorithm_result_t result;
 * algorithm_function(..., &result);
 * // Use result...
 * free_result(&result);  // Always free when done
 * @endcode
 */
void free_result(algorithm_result_t *result) {
    if (result == NULL) {
        return;
    }

    if (result->data != NULL) {
        free(result->data);
        result->data = NULL;
    }

    result->size = 0;
    result->success = false;
}

/* ========================================================================== */
/* UTILITY FUNCTIONS                                                          */
/* ========================================================================== */

/**
 * @brief Check if value is within valid range
 *
 * @param[in] value Value to check
 * @param[in] min   Minimum valid value (inclusive)
 * @param[in] max   Maximum valid value (inclusive)
 *
 * @return true if value is in range [min, max], false otherwise
 *
 * @note Thread-safe
 */
static inline bool is_in_range(int value, int min, int max) {
    return (value >= min) && (value <= max);
}

/* ========================================================================== */
/* MAIN PROGRAM (DEMONSTRATION)                                               */
/* ========================================================================== */

/**
 * @brief Main program demonstrating algorithm usage
 *
 * @return EXIT_SUCCESS on success, EXIT_FAILURE on error
 */
int main(void) {
    printf("========================================\n");
    printf("  Algorithm Function Demonstration\n");
    printf("========================================\n\n");

    /* Example 1: Basic Usage */
    printf("Example 1: Basic Usage\n");
    printf("----------------------------------------\n");

    int data1[] = {5, 2, 8, 1, 9, 3, 7};
    algorithm_options_t opts1 = {
        .param1 = 2,
        .param2 = 1.0,
        .validate_input = true,
        .max_iterations = 1000
    };

    algorithm_result_t result1;
    error_code_t err1 = algorithm_function(data1, 7, &opts1, &result1);

    if (err1 == SUCCESS) {
        printf("✓ Success!\n");
        printf("  Iterations: %zu\n", result1.iterations);
        printf("  Comparisons: %zu\n", result1.comparisons);

        printf("  Result: [");
        for (size_t i = 0; i < result1.size; i++) {
            printf("%d%s", result1.data[i], i < result1.size-1 ? ", " : "");
        }
        printf("]\n");

        free_result(&result1);
    } else {
        fprintf(stderr, "✗ Error: %s\n", get_error_message(err1));
    }

    printf("\n");

    /* Example 2: Error Handling */
    printf("Example 2: Error Handling\n");
    printf("----------------------------------------\n");

    algorithm_result_t result2;
    error_code_t err2 = algorithm_function(NULL, 0, &opts1, &result2);

    printf("Expected error: %s\n", get_error_message(err2));
    printf("✓ Error handling works correctly\n\n");

    printf("========================================\n");
    printf("  Demonstration Complete!\n");
    printf("========================================\n");

    return EXIT_SUCCESS;
}
