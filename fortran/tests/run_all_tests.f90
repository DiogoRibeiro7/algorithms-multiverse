! Master test runner for all Fortran algorithm modules
program run_all_tests
    use iso_fortran_env, only: int32
    implicit none

    integer :: total_modules = 8
    integer :: passed_modules = 0
    integer :: exit_code

    print '(A)', ""
    print '(A)', "============================================"
    print '(A)', "   Algorithms Multiverse - Fortran"
    print '(A)', "        Complete Test Suite"
    print '(A)', "============================================"
    print '(A)', ""

    ! Run each module's test suite
    call run_test("Graph Module", "./graph_module_test", passed_modules)
    call run_test("String Module", "./string_module_test", passed_modules)
    call run_test("Crypto Module", "./crypto_module_test", passed_modules)
    call run_test("Geometry Module", "./geometry_module_test", passed_modules)
    call run_test("Data Structures Module", "./data_structures_module_test", passed_modules)
    call run_test("Statistics Module", "./statistics_module_test", passed_modules)
    call run_test("Optimization Module", "./optimization_module_test", passed_modules)
    call run_test("Streaming Module", "./streaming_module_test", passed_modules)

    ! Print summary
    print '(A)', ""
    print '(A)', "============================================"
    print '(A)', "           TEST SUITE SUMMARY"
    print '(A)', "============================================"
    print '(A,I0,A,I0,A)', "Modules Passed: ", passed_modules, "/", total_modules

    if (passed_modules == total_modules) then
        print '(A)', ""
        print '(A)', "   ✓✓✓ ALL TESTS PASSED ✓✓✓"
        print '(A)', ""
    else
        print '(A)', ""
        print '(A)', "   ✗✗✗ SOME TESTS FAILED ✗✗✗"
        print '(A)', ""
    end if
    print '(A)', "============================================"

contains

    subroutine run_test(module_name, executable, passed_count)
        character(len=*), intent(in) :: module_name, executable
        integer, intent(inout) :: passed_count
        integer :: exit_status
        character(len=256) :: command

        print '(A,A,A)', "Running ", module_name, " tests..."

        command = trim(executable)
        call execute_command_line(command, exitstat=exit_status)

        if (exit_status == 0) then
            print '(A,A,A)', "✓ ", module_name, " tests completed successfully"
            passed_count = passed_count + 1
        else
            print '(A,A,A)', "✗ ", module_name, " tests failed or could not run"
        end if

        print '(A)', ""

    end subroutine run_test

end program run_all_tests