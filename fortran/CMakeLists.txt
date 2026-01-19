# CMakeLists.txt for Algorithms Multiverse - Fortran Implementation
cmake_minimum_required(VERSION 3.10)
project(AlgorithmsMultiverseFortran
    VERSION 1.0.0
    LANGUAGES Fortran
    DESCRIPTION "Comprehensive collection of algorithms in Fortran"
)

# Set default build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

# Fortran compiler settings
enable_language(Fortran)

# Set Fortran standard
set(CMAKE_Fortran_STANDARD 2018)
set(CMAKE_Fortran_STANDARD_REQUIRED ON)

# Compiler-specific flags
if(CMAKE_Fortran_COMPILER_ID MATCHES "GNU")
    set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -Wall -Wextra -fcheck=all")
    set(CMAKE_Fortran_FLAGS_DEBUG "-g -O0 -fbacktrace")
    set(CMAKE_Fortran_FLAGS_RELEASE "-O3 -march=native -funroll-loops")
elseif(CMAKE_Fortran_COMPILER_ID MATCHES "Intel")
    set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -warn all -check all")
    set(CMAKE_Fortran_FLAGS_DEBUG "-g -O0 -traceback")
    set(CMAKE_Fortran_FLAGS_RELEASE "-O3 -xHost -ipo")
endif()

# Find OpenMP
find_package(OpenMP)
if(OpenMP_Fortran_FOUND)
    set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} ${OpenMP_Fortran_FLAGS}")
endif()

# Set module directory
set(CMAKE_Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/modules)

# Source files
set(LIBRARY_SOURCES
    src/sorting_module.f90
    src/searching_module.f90
    src/numerical_module.f90
    src/matrix_module.f90
    src/dynamic_programming_module.f90
    src/algorithms_multiverse.f90
)

# Create static library
add_library(algorithms_multiverse_static STATIC ${LIBRARY_SOURCES})
set_target_properties(algorithms_multiverse_static PROPERTIES
    OUTPUT_NAME algorithms_multiverse
    Fortran_MODULE_DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY}
)

# Create shared library
add_library(algorithms_multiverse_shared SHARED ${LIBRARY_SOURCES})
set_target_properties(algorithms_multiverse_shared PROPERTIES
    OUTPUT_NAME algorithms_multiverse
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    Fortran_MODULE_DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY}
)

# Link OpenMP if found
if(OpenMP_Fortran_FOUND)
    target_link_libraries(algorithms_multiverse_static PUBLIC OpenMP::OpenMP_Fortran)
    target_link_libraries(algorithms_multiverse_shared PUBLIC OpenMP::OpenMP_Fortran)
endif()

# Testing support
option(BUILD_TESTS "Build test programs" ON)
if(BUILD_TESTS)
    enable_testing()

    # Test sources
    set(TEST_SOURCES
        tests/test_sorting.f90
        tests/test_searching.f90
        tests/test_numerical.f90
        tests/test_matrix.f90
        tests/test_dynamic_programming.f90
        tests/test_runner.f90
    )

    # Create test executable
    add_executable(test_runner ${TEST_SOURCES})
    target_link_libraries(test_runner algorithms_multiverse_static)
    target_include_directories(test_runner PRIVATE ${CMAKE_Fortran_MODULE_DIRECTORY})

    # Add tests
    add_test(NAME SortingTests COMMAND test_runner sorting)
    add_test(NAME SearchingTests COMMAND test_runner searching)
    add_test(NAME NumericalTests COMMAND test_runner numerical)
    add_test(NAME MatrixTests COMMAND test_runner matrix)
    add_test(NAME DynamicProgrammingTests COMMAND test_runner dp)

    # Add a custom target to run all tests
    add_custom_target(run_tests
        COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure
        DEPENDS test_runner
    )
endif()

# Benchmark support
option(BUILD_BENCHMARKS "Build benchmark programs" ON)
if(BUILD_BENCHMARKS)
    # Create benchmark executable
    add_executable(benchmark tests/benchmark.f90)
    target_link_libraries(benchmark algorithms_multiverse_static)
    target_include_directories(benchmark PRIVATE ${CMAKE_Fortran_MODULE_DIRECTORY})
    set_target_properties(benchmark PROPERTIES
        COMPILE_FLAGS "${CMAKE_Fortran_FLAGS_RELEASE}"
    )

    # Add custom target to run benchmarks
    add_custom_target(run_benchmarks
        COMMAND benchmark
        DEPENDS benchmark
    )
endif()

# Examples
option(BUILD_EXAMPLES "Build example programs" ON)
if(BUILD_EXAMPLES)
    # Create examples directory
    file(GLOB EXAMPLE_SOURCES examples/*.f90)
    foreach(EXAMPLE_SOURCE ${EXAMPLE_SOURCES})
        get_filename_component(EXAMPLE_NAME ${EXAMPLE_SOURCE} NAME_WE)
        add_executable(${EXAMPLE_NAME} ${EXAMPLE_SOURCE})
        target_link_libraries(${EXAMPLE_NAME} algorithms_multiverse_static)
        target_include_directories(${EXAMPLE_NAME} PRIVATE ${CMAKE_Fortran_MODULE_DIRECTORY})
    endforeach()
endif()

# Documentation
option(BUILD_DOCS "Build documentation" OFF)
if(BUILD_DOCS)
    find_program(FORD ford)
    if(FORD)
        add_custom_target(docs
            COMMAND ${FORD} ${CMAKE_SOURCE_DIR}/ford.md
            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
            COMMENT "Generating API documentation with FORD"
        )
    else()
        message(WARNING "FORD not found, documentation will not be built")
    endif()
endif()

# Installation
include(GNUInstallDirs)

# Install libraries
install(TARGETS algorithms_multiverse_static algorithms_multiverse_shared
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

# Install module files
install(DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY}/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/algorithms_multiverse
    FILES_MATCHING PATTERN "*.mod"
)

# Create and install pkg-config file
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/algorithms_multiverse.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/algorithms_multiverse.pc
    @ONLY
)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/algorithms_multiverse.pc
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig
)

# Export targets
install(EXPORT AlgorithmsMultiverseTargets
    FILE AlgorithmsMultiverseTargets.cmake
    NAMESPACE AlgorithmsMultiverse::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/AlgorithmsMultiverse
)

# Create config files
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    AlgorithmsMultiverseConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/AlgorithmsMultiverseConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/AlgorithmsMultiverseConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/AlgorithmsMultiverse
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/AlgorithmsMultiverseConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/AlgorithmsMultiverseConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/AlgorithmsMultiverse
)

# CPack configuration
set(CPACK_PACKAGE_VENDOR "Algorithms Multiverse")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Comprehensive algorithm library in Fortran")
set(CPACK_PACKAGE_VERSION_MAJOR ${PROJECT_VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR ${PROJECT_VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH ${PROJECT_VERSION_PATCH})
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/../LICENSE")
set(CPACK_RESOURCE_FILE_README "${CMAKE_CURRENT_SOURCE_DIR}/README.md")
include(CPack)

# Print configuration summary
message(STATUS "")
message(STATUS "=== Configuration Summary ===")
message(STATUS "Build type:        ${CMAKE_BUILD_TYPE}")
message(STATUS "Fortran compiler:  ${CMAKE_Fortran_COMPILER}")
message(STATUS "Fortran flags:     ${CMAKE_Fortran_FLAGS}")
message(STATUS "OpenMP support:    ${OpenMP_Fortran_FOUND}")
message(STATUS "Build tests:       ${BUILD_TESTS}")
message(STATUS "Build benchmarks:  ${BUILD_BENCHMARKS}")
message(STATUS "Build examples:    ${BUILD_EXAMPLES}")
message(STATUS "Build docs:        ${BUILD_DOCS}")
message(STATUS "Install prefix:    ${CMAKE_INSTALL_PREFIX}")
message(STATUS "=============================")
message(STATUS "")