"""
    AlgorithmsMultiverse

A comprehensive collection of algorithms and data structures implemented in Julia.

# Modules
- `Sorting`: Sorting algorithms
- `Searching`: Search algorithms
- `DataStructures`: Fundamental data structures
- `GraphAlgorithms`: Graph algorithms
- `DynamicProgramming`: Dynamic programming problems
- `StringAlgorithms`: String processing algorithms
- `NumericalAlgorithms`: Numerical and mathematical algorithms
"""
module AlgorithmsMultiverse

# Standard library imports
using LinearAlgebra
using Random
using Statistics

# Export all submodules
export Sorting, Searching, DataStructures, GraphAlgorithms,
       DynamicProgramming, StringAlgorithms, NumericalAlgorithms

# Include submodules
include("sorting.jl")
include("searching.jl")
include("data_structures.jl")
include("graph_algorithms.jl")
include("dynamic_programming.jl")
include("string_algorithms.jl")
include("numerical_algorithms.jl")

"""
    info()

Display information about the AlgorithmsMultiverse package.
"""
function info()
    println("AlgorithmsMultiverse v1.0.0")
    println("=====================================")
    println("A comprehensive algorithm collection in Julia")
    println("")
    println("Modules available:")
    println("  • Sorting - 12 algorithms")
    println("  • Searching - 10 algorithms")
    println("  • DataStructures - 10 structures")
    println("  • GraphAlgorithms - 15 algorithms")
    println("  • DynamicProgramming - 20 problems")
    println("  • StringAlgorithms - 10 algorithms")
    println("  • NumericalAlgorithms - 15 algorithms")
    println("")
    println("Total: 92+ algorithms and data structures")
end

end # module