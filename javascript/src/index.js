/**
 * Algorithms Multiverse - JavaScript Implementation
 * A comprehensive algorithm library providing efficient implementations
 * of fundamental algorithms and data structures.
 *
 * @module algorithms-multiverse
 */

// Import all modules
import * as sorting from './sorting.js';
import * as searching from './searching.js';
import * as dataStructures from './dataStructures.js';
import * as stringAlgorithms from './stringAlgorithms.js';
import * as numerical from './numerical.js';
import * as dynamicProgramming from './dynamicProgramming.js';
import * as graph from './graph.js';
import * as matrix from './matrix.js';
import * as machineLearning from './machineLearning.js';
import * as optimization from './optimization.js';
import * as streaming from './streaming.js';
import * as utils from './utils.js';

// Re-export all modules
export {
    sorting,
    searching,
    dataStructures,
    stringAlgorithms,
    numerical,
    dynamicProgramming,
    graph,
    matrix,
    machineLearning,
    optimization,
    streaming,
    utils
};

// Also export commonly used functions directly
export {
    // Sorting
    bubbleSort,
    insertionSort,
    selectionSort,
    mergeSort,
    quickSort,
    heapSort,
    radixSort,
    countingSort,
    bucketSort,
    timSort
} from './sorting.js';

export {
    // Searching
    linearSearch,
    binarySearch,
    jumpSearch,
    interpolationSearch,
    exponentialSearch,
    fibonacciSearch,
    ternarySearch
} from './searching.js';

export {
    // Data Structures
    Stack,
    Queue,
    Deque,
    PriorityQueue,
    LinkedList,
    DoublyLinkedList,
    BinarySearchTree,
    AVLTree,
    RedBlackTree,
    Heap,
    HashTable,
    Trie,
    DisjointSet,
    SegmentTree,
    FenwickTree
} from './dataStructures.js';

export {
    // String Algorithms
    kmpSearch,
    rabinKarpSearch,
    boyerMooreSearch,
    levenshteinDistance,
    longestCommonSubsequence,
    longestPalindromicSubstring
} from './stringAlgorithms.js';

export {
    // Numerical
    gcd,
    lcm,
    isPrime,
    sieveOfEratosthenes,
    fibonacci,
    factorial,
    binomialCoefficient,
    fastPower,
    modularExponentiation
} from './numerical.js';

export {
    // Dynamic Programming
    knapsack,
    coinChange,
    editDistance,
    longestIncreasingSubsequence,
    matrixChainMultiplication
} from './dynamicProgramming.js';

export {
    // Graph
    Graph,
    dijkstra,
    bellmanFord,
    floydWarshall,
    kruskal,
    prim,
    topologicalSort,
    stronglyConnectedComponents
} from './graph.js';

export {
    // Matrix
    Matrix,
    matrixMultiply,
    matrixTranspose,
    matrixDeterminant,
    matrixInverse,
    luDecomposition,
    qrDecomposition
} from './matrix.js';

export {
    // Machine Learning
    KNNClassifier,
    GaussianNaiveBayes,
    DecisionTreeClassifier,
    Perceptron,
    LogisticRegression,
    LinearRegression,
    KMeans,
    DBSCAN,
    PCA,
    trainTestSplit,
    accuracy,
    confusionMatrix
} from './machineLearning.js';

export {
    // Optimization
    GeneticAlgorithm,
    SimulatedAnnealing,
    ParticleSwarm,
    GradientDescent,
    DifferentialEvolution,
    HillClimbing,
    TabuSearch,
    AntColonyOptimization,
    testFunctions,
    createBounds
} from './optimization.js';

export {
    // Streaming
    ReservoirSampler,
    WeightedReservoirSampler,
    StratifiedReservoirSampler,
    StreamingStats,
    EWMA,
    StreamingQuantiles,
    HyperLogLog,
    CountMinSketch,
    MisraGries,
    SpaceSaving,
    SlidingWindowStats,
    SlidingWindowExtreme,
    SlidingWindowCounter,
    BloomFilter,
    OnlineLinearRegression,
    OnlineKMeans,
    BernoulliSampler,
    SystematicSampler
} from './streaming.js';

// Version info
export const VERSION = '1.3.0';

/**
 * Initialize the library (if needed for any setup)
 */
export function init() {
    console.log(`Algorithms Multiverse v${VERSION} - JavaScript Implementation`);
    console.log('Ready to use!');
}

// Default export
export default {
    sorting,
    searching,
    dataStructures,
    stringAlgorithms,
    numerical,
    dynamicProgramming,
    graph,
    matrix,
    machineLearning,
    optimization,
    streaming,
    utils,
    VERSION,
    init
};