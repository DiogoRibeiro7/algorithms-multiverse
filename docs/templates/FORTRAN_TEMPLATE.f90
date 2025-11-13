!> @file FORTRAN_TEMPLATE.f90
!> @brief Fortran Documentation Template for Algorithms Multiverse
!>
!> This template provides the standard documentation format for Fortran files
!> in the Algorithms Multiverse project. Modern Fortran (90+) with proper
!> documentation and error handling.
!>
!> @details
!> Detailed description of what this module does. Explain the algorithms,
!> data structures, and any important implementation details.
!>
!> Features:
!> - Feature 1: Description
!> - Feature 2: Description
!> - Feature 3: Description
!>
!> @author Algorithms Multiverse
!> @date 2024
!> @version 1.0
!>
!> @par Compilation
!> @code
!> gfortran -o program FORTRAN_TEMPLATE.f90 -Wall -Wextra -O2
!> @endcode
!>
!> @par Usage
!> @code
!> ./program
!> @endcode
!>
!> @see Related module or documentation
!> @note Important notes about the implementation
!> @warning Warnings about usage or limitations

! ============================================================================
! MODULE DEFINITION
! ============================================================================

!> @brief Algorithm Module
!>
!> Module containing algorithm implementations with proper error handling
!> and documentation.
!>
!> @details
!> This module provides implementations of various algorithms with:
!> - Input validation
!> - Error status reporting
!> - Performance metrics tracking
!> - Clear documentation
module algorithm_module
    implicit none
    private  ! Default to private

    ! Public interface
    public :: algorithm_function, algorithm_function_safe
    public :: validate_input, get_error_message
    public :: ERROR_SUCCESS, ERROR_INVALID_INPUT, ERROR_OUT_OF_BOUNDS

    ! ========================================================================
    ! CONSTANTS
    ! ========================================================================

    !> Maximum array size supported
    integer, parameter, public :: MAX_ARRAY_SIZE = 1000000

    !> Numerical tolerance for comparisons
    real(8), parameter, public :: TOLERANCE = 1.0e-10

    !> Mathematical constant Pi
    real(8), parameter, public :: PI = 3.14159265358979323846

    ! ========================================================================
    ! ERROR CODES
    ! ========================================================================

    !> Success - no error
    integer, parameter :: ERROR_SUCCESS = 0

    !> Invalid input parameter
    integer, parameter :: ERROR_INVALID_INPUT = -1

    !> Array index out of bounds
    integer, parameter :: ERROR_OUT_OF_BOUNDS = -2

    !> Numerical convergence failure
    integer, parameter :: ERROR_NO_CONVERGENCE = -3

    !> Memory allocation failure
    integer, parameter :: ERROR_ALLOCATION = -4

    !> File I/O error
    integer, parameter :: ERROR_IO = -5

    ! ========================================================================
    ! DERIVED TYPES
    ! ========================================================================

    !> @brief Result type for algorithm outputs
    !>
    !> @details
    !> Container for algorithm results with error status and metrics
    type, public :: algorithm_result_t
        !> Error status code
        integer :: status

        !> Result data array
        real(8), allocatable :: data(:)

        !> Number of iterations performed
        integer :: iterations

        !> Number of comparisons made
        integer :: comparisons

        !> Execution time in seconds
        real(8) :: time

        !> Success flag
        logical :: success
    end type algorithm_result_t

contains

    ! ========================================================================
    ! MAIN ALGORITHM FUNCTION
    ! ========================================================================

    !> @brief Main algorithm function with comprehensive error handling
    !>
    !> @details
    !> Detailed description of what this algorithm does, how it works,
    !> and when to use it. Explain the mathematical foundation and
    !> implementation approach.
    !>
    !> Algorithm Steps:
    !> 1. Validate input parameters
    !> 2. Allocate necessary memory
    !> 3. Process data according to algorithm
    !> 4. Clean up and return results
    !>
    !> @param[in]     input_data   Input array to process (size n)
    !> @param[in]     n            Size of input array (must be > 0)
    !> @param[in]     param1       Algorithm parameter 1 (range: [0, 1000])
    !> @param[in]     param2       Algorithm parameter 2 (positive real)
    !> @param[out]    result       Result structure with output and metrics
    !> @param[out]    status       Error status code
    !>
    !> @return None (results returned via result parameter)
    !>
    !> @note Thread-safe if compiled with OpenMP support
    !> @warning Input array must be allocated before calling
    !> @warning Caller must deallocate result%data after use
    !>
    !> @par Error Codes
    !> - ERROR_SUCCESS: Operation completed successfully
    !> - ERROR_INVALID_INPUT: Invalid input parameters
    !> - ERROR_OUT_OF_BOUNDS: Array index out of range
    !> - ERROR_ALLOCATION: Memory allocation failed
    !>
    !> @par Complexity
    !> - Time: O(n log n) average case, O(n²) worst case
    !> - Space: O(n) for auxiliary storage
    !>
    !> @par Example
    !> @code
    !> program test
    !>     use algorithm_module
    !>     implicit none
    !>     real(8) :: data(10)
    !>     type(algorithm_result_t) :: result
    !>     integer :: status, i
    !>
    !>     ! Initialize data
    !>     do i = 1, 10
    !>         data(i) = real(i, 8)
    !>     end do
    !>
    !>     ! Call algorithm
    !>     call algorithm_function(data, 10, 5, 1.0d0, result, status)
    !>
    !>     ! Check status
    !>     if (status == ERROR_SUCCESS) then
    !>         print *, 'Success!'
    !>         print *, 'Iterations:', result%iterations
    !>     else
    !>         print *, 'Error:', get_error_message(status)
    !>     end if
    !>
    !>     ! Clean up
    !>     if (allocated(result%data)) deallocate(result%data)
    !> end program test
    !> @endcode
    !>
    !> @see algorithm_function_safe, validate_input
    subroutine algorithm_function(input_data, n, param1, param2, result, status)
        ! Argument declarations
        integer, intent(in) :: n
        real(8), intent(in) :: input_data(n)
        integer, intent(in) :: param1
        real(8), intent(in) :: param2
        type(algorithm_result_t), intent(out) :: result
        integer, intent(out) :: status

        ! Local variables
        integer :: i, alloc_status
        real(8) :: start_time, end_time

        ! Initialize result structure
        result%status = ERROR_SUCCESS
        result%iterations = 0
        result%comparisons = 0
        result%time = 0.0d0
        result%success = .false.

        ! Start timing
        call cpu_time(start_time)

        ! ====================================================================
        ! INPUT VALIDATION
        ! ====================================================================

        ! Validate array size
        if (n <= 0) then
            status = ERROR_INVALID_INPUT
            result%status = status
            call log_error('algorithm_function', 'Array size must be positive')
            return
        end if

        if (n > MAX_ARRAY_SIZE) then
            status = ERROR_INVALID_INPUT
            result%status = status
            call log_error('algorithm_function', 'Array size exceeds maximum')
            return
        end if

        ! Validate param1
        if (param1 < 0 .or. param1 > 1000) then
            status = ERROR_INVALID_INPUT
            result%status = status
            write(*,'(A,I0)') 'ERROR: param1 out of range [0,1000]: ', param1
            return
        end if

        ! Validate param2
        if (param2 <= 0.0d0) then
            status = ERROR_INVALID_INPUT
            result%status = status
            write(*,'(A,ES12.4)') 'ERROR: param2 must be positive: ', param2
            return
        end if

        ! Validate input data (check for NaN, Inf)
        do i = 1, n
            if (isnan(input_data(i)) .or. abs(input_data(i)) > huge(1.0d0)) then
                status = ERROR_INVALID_INPUT
                result%status = status
                write(*,'(A,I0)') 'ERROR: Invalid value at index ', i
                return
            end if
        end do

        ! ====================================================================
        ! MEMORY ALLOCATION
        ! ====================================================================

        ! Allocate result data array
        allocate(result%data(n), stat=alloc_status)
        if (alloc_status /= 0) then
            status = ERROR_ALLOCATION
            result%status = status
            call log_error('algorithm_function', 'Failed to allocate result array')
            return
        end if

        ! ====================================================================
        ! MAIN ALGORITHM IMPLEMENTATION
        ! ====================================================================

        ! Copy input data
        result%data = input_data

        ! Algorithm implementation goes here
        do i = 1, n
            result%iterations = result%iterations + 1

            ! Process data...
            result%data(i) = result%data(i) * param2

            ! Track comparisons
            if (i < n) then
                if (result%data(i) > result%data(i+1)) then
                    result%comparisons = result%comparisons + 1
                end if
            end if
        end do

        ! ====================================================================
        ! FINALIZATION
        ! ====================================================================

        ! Calculate execution time
        call cpu_time(end_time)
        result%time = end_time - start_time

        ! Set success status
        status = ERROR_SUCCESS
        result%status = status
        result%success = .true.

        ! Log completion
        call log_info('algorithm_function', 'Completed successfully')

    end subroutine algorithm_function

    ! ========================================================================
    ! SAFE WRAPPER FUNCTION
    ! ========================================================================

    !> @brief Safe wrapper for algorithm_function with automatic cleanup
    !>
    !> @details
    !> Convenience function that handles error checking and cleanup
    !> automatically. Recommended for most use cases.
    !>
    !> @param[in]     input_data   Input array
    !> @param[in]     n            Array size
    !> @param[in]     param1       Parameter 1
    !> @param[in]     param2       Parameter 2
    !> @param[out]    output_data  Output array (allocated by function)
    !> @param[out]    status       Error status
    !>
    !> @note output_data is allocated by this function and must be
    !>       deallocated by caller
    subroutine algorithm_function_safe(input_data, n, param1, param2, &
                                      output_data, status)
        integer, intent(in) :: n
        real(8), intent(in) :: input_data(n)
        integer, intent(in) :: param1
        real(8), intent(in) :: param2
        real(8), allocatable, intent(out) :: output_data(:)
        integer, intent(out) :: status

        type(algorithm_result_t) :: result

        ! Call main function
        call algorithm_function(input_data, n, param1, param2, result, status)

        ! Handle result
        if (status == ERROR_SUCCESS) then
            ! Transfer ownership of data array
            call move_alloc(result%data, output_data)
        else
            ! Ensure output is not allocated on error
            if (allocated(output_data)) deallocate(output_data)
        end if

    end subroutine algorithm_function_safe

    ! ========================================================================
    ! INPUT VALIDATION FUNCTIONS
    ! ========================================================================

    !> @brief Validate input parameters
    !>
    !> @details
    !> Comprehensive input validation without performing the algorithm.
    !> Useful for checking inputs before expensive operations.
    !>
    !> @param[in]  n       Array size
    !> @param[in]  param1  Parameter 1
    !> @param[in]  param2  Parameter 2
    !>
    !> @return .true. if inputs are valid, .false. otherwise
    !>
    !> @par Example
    !> @code
    !> if (validate_input(n, param1, param2)) then
    !>     call algorithm_function(...)
    !> else
    !>     print *, 'Invalid input parameters'
    !> end if
    !> @endcode
    function validate_input(n, param1, param2) result(is_valid)
        integer, intent(in) :: n
        integer, intent(in) :: param1
        real(8), intent(in) :: param2
        logical :: is_valid

        is_valid = .true.

        ! Check array size
        if (n <= 0 .or. n > MAX_ARRAY_SIZE) then
            is_valid = .false.
            return
        end if

        ! Check param1 range
        if (param1 < 0 .or. param1 > 1000) then
            is_valid = .false.
            return
        end if

        ! Check param2
        if (param2 <= 0.0d0 .or. isnan(param2)) then
            is_valid = .false.
            return
        end if

    end function validate_input

    ! ========================================================================
    ! ERROR HANDLING UTILITIES
    ! ========================================================================

    !> @brief Get human-readable error message
    !>
    !> @param[in]  error_code  Error status code
    !>
    !> @return Character string describing the error
    function get_error_message(error_code) result(message)
        integer, intent(in) :: error_code
        character(len=100) :: message

        select case (error_code)
            case (ERROR_SUCCESS)
                message = 'Success'
            case (ERROR_INVALID_INPUT)
                message = 'Invalid input parameters'
            case (ERROR_OUT_OF_BOUNDS)
                message = 'Array index out of bounds'
            case (ERROR_NO_CONVERGENCE)
                message = 'Algorithm failed to converge'
            case (ERROR_ALLOCATION)
                message = 'Memory allocation failed'
            case (ERROR_IO)
                message = 'File I/O error'
            case default
                write(message, '(A,I0)') 'Unknown error code: ', error_code
        end select

    end function get_error_message

    !> @brief Log error message
    !>
    !> @param[in]  routine  Name of routine where error occurred
    !> @param[in]  message  Error message
    subroutine log_error(routine, message)
        character(len=*), intent(in) :: routine
        character(len=*), intent(in) :: message

        write(*,'(A,A,A,A)') 'ERROR in ', trim(routine), ': ', trim(message)

    end subroutine log_error

    !> @brief Log informational message
    !>
    !> @param[in]  routine  Name of routine
    !> @param[in]  message  Information message
    subroutine log_info(routine, message)
        character(len=*), intent(in) :: routine
        character(len=*), intent(in) :: message

        ! Uncomment for debugging
        ! write(*,'(A,A,A,A)') 'INFO: ', trim(routine), ': ', trim(message)

    end subroutine log_info

    ! ========================================================================
    ! UTILITY FUNCTIONS
    ! ========================================================================

    !> @brief Check if a real number is NaN
    !>
    !> @param[in]  x  Number to check
    !>
    !> @return .true. if x is NaN, .false. otherwise
    pure function isnan(x) result(res)
        real(8), intent(in) :: x
        logical :: res

        ! NaN is the only value that doesn't equal itself
        res = (x /= x)

    end function isnan

end module algorithm_module

! ============================================================================
! MAIN PROGRAM (DEMONSTRATION)
! ============================================================================

!> @brief Main program demonstrating algorithm usage
!>
!> @details
!> Comprehensive examples showing proper usage, error handling,
!> and best practices.
program main
    use algorithm_module
    implicit none

    ! Variables
    real(8), allocatable :: input_data(:), output_data(:)
    type(algorithm_result_t) :: result
    integer :: n, status, i

    print '(A)', repeat('=', 75)
    print '(A)', '          ALGORITHM MODULE DEMONSTRATION'
    print '(A)', repeat('=', 75)
    print *

    ! ========================================================================
    ! Example 1: Basic Usage
    ! ========================================================================

    print '(A)', 'Example 1: Basic Usage'
    print '(A)', repeat('-', 75)

    n = 10
    allocate(input_data(n))

    ! Initialize test data
    do i = 1, n
        input_data(i) = real(i, 8)
    end do

    print '(A)', 'Input data: '
    write(*, '(10F8.2)') input_data

    ! Call algorithm
    call algorithm_function(input_data, n, 5, 2.0d0, result, status)

    if (status == ERROR_SUCCESS) then
        print '(A)', 'Output data:'
        write(*, '(10F8.2)') result%data
        print '(A,I0)', 'Iterations: ', result%iterations
        print '(A,F10.6)', 'Time: ', result%time
        print '(A)', '✓ Success'

        ! Clean up
        if (allocated(result%data)) deallocate(result%data)
    else
        print '(A,A)', 'Error: ', trim(get_error_message(status))
    end if

    deallocate(input_data)
    print *

    ! ========================================================================
    ! Example 2: Error Handling
    ! ========================================================================

    print '(A)', 'Example 2: Error Handling'
    print '(A)', repeat('-', 75)

    n = 0  ! Invalid size
    allocate(input_data(1))

    call algorithm_function(input_data, n, 5, 2.0d0, result, status)

    if (status /= ERROR_SUCCESS) then
        print '(A,A)', 'Expected error caught: ', trim(get_error_message(status))
        print '(A)', '✓ Error handling works correctly'
    end if

    deallocate(input_data)
    print *

    ! ========================================================================
    ! Example 3: Input Validation
    ! ========================================================================

    print '(A)', 'Example 3: Input Validation'
    print '(A)', repeat('-', 75)

    if (validate_input(10, 50, 1.5d0)) then
        print '(A)', '✓ Valid input parameters'
    else
        print '(A)', '✗ Invalid input parameters'
    end if

    if (validate_input(-5, 50, 1.5d0)) then
        print '(A)', '✓ Valid input parameters'
    else
        print '(A)', '✗ Invalid input parameters (expected)'
    end if

    print *

    ! ========================================================================
    ! Example 4: Safe Wrapper
    ! ========================================================================

    print '(A)', 'Example 4: Safe Wrapper Function'
    print '(A)', repeat('-', 75)

    n = 5
    allocate(input_data(n))
    input_data = [1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0]

    call algorithm_function_safe(input_data, n, 10, 1.5d0, output_data, status)

    if (status == ERROR_SUCCESS) then
        print '(A)', 'Output from safe wrapper:'
        write(*, '(5F8.2)') output_data
        print '(A)', '✓ Success'
        deallocate(output_data)
    end if

    deallocate(input_data)
    print *

    ! ========================================================================
    ! Summary
    ! ========================================================================

    print '(A)', repeat('=', 75)
    print '(A)', 'Summary:'
    print '(A)', '✓ All examples completed successfully'
    print '(A)', '✓ Error handling works correctly'
    print '(A)', '✓ Input validation functional'
    print '(A)', '✓ Memory properly managed'
    print '(A)', repeat('=', 75)

end program main
