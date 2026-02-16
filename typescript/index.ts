/**
 * Algorithms Multiverse - TypeScript Implementation
 * ==================================================
 *
 * Comprehensive algorithm library for TypeScript/JavaScript
 *
 * @packageDocumentation
 * @module algorithms-multiverse
 */

// Export Sorting Algorithms
export {
    QuickSort,
    MergeSort,
    HeapSort,
    TimSort,
    RadixSort,
    IntroSort,
    SortingUtils,
    type CompareFn,
    type SortingStats
} from './sorting';

// Export Data Structures
export {
    LinkedList,
    Stack,
    Queue,
    PriorityQueue,
    BinarySearchTree,
    HashTable,
    Trie
} from './dataStructures';

// Export Graph Algorithms
export {
    Graph,
    GraphTraversal,
    ShortestPath,
    MinimumSpanningTree,
    GraphUtils,
    type Edge,
    type IGraph
} from './graphAlgorithms';

// Export Dynamic Programming
export {
    DynamicProgramming
} from './dynamicProgramming';

// Export String Algorithms
export {
    StringAlgorithms,
    StringUtils
} from './stringAlgorithms';

// Re-export common utilities
export const VERSION = '1.0.0';

/**
 * Algorithm complexity reference
 */
export const Complexity = {
    Sorting: {
        QuickSort: { time: 'O(n log n) avg, O(n²) worst', space: 'O(log n)' },
        MergeSort: { time: 'O(n log n)', space: 'O(n)' },
        HeapSort: { time: 'O(n log n)', space: 'O(1)' },
        TimSort: { time: 'O(n log n)', space: 'O(n)' },
        RadixSort: { time: 'O(nk)', space: 'O(n)' },
        IntroSort: { time: 'O(n log n)', space: 'O(log n)' }
    },
    DataStructures: {
        LinkedList: {
            insert: 'O(1) at head/tail, O(n) at index',
            delete: 'O(1) at head, O(n) elsewhere',
            search: 'O(n)'
        },
        Stack: { push: 'O(1)', pop: 'O(1)', peek: 'O(1)' },
        Queue: { enqueue: 'O(1)', dequeue: 'O(1)' },
        BinarySearchTree: {
            insert: 'O(log n) avg, O(n) worst',
            delete: 'O(log n) avg, O(n) worst',
            search: 'O(log n) avg, O(n) worst'
        },
        HashTable: {
            insert: 'O(1) avg, O(n) worst',
            delete: 'O(1) avg, O(n) worst',
            search: 'O(1) avg, O(n) worst'
        },
        Trie: {
            insert: 'O(m)',
            search: 'O(m)',
            delete: 'O(m)'
        }
    },
    Graph: {
        BFS: { time: 'O(V + E)', space: 'O(V)' },
        DFS: { time: 'O(V + E)', space: 'O(V)' },
        Dijkstra: { time: 'O((V + E) log V)', space: 'O(V)' },
        BellmanFord: { time: 'O(VE)', space: 'O(V)' },
        FloydWarshall: { time: 'O(V³)', space: 'O(V²)' },
        Kruskal: { time: 'O(E log E)', space: 'O(V)' },
        Prim: { time: 'O(E log V)', space: 'O(V)' }
    },
    String: {
        KMP: { time: 'O(n + m)', space: 'O(m)' },
        RabinKarp: { time: 'O(nm) worst, O(n + m) avg', space: 'O(1)' },
        BoyerMoore: { time: 'O(nm) worst, O(n/m) best', space: 'O(σ)' },
        ZAlgorithm: { time: 'O(n + m)', space: 'O(n + m)' },
        Manacher: { time: 'O(n)', space: 'O(n)' }
    }
} as const;

/**
 * Algorithm categories
 */
export enum AlgorithmCategory {
    SORTING = 'Sorting',
    SEARCHING = 'Searching',
    GRAPH = 'Graph',
    DYNAMIC_PROGRAMMING = 'Dynamic Programming',
    STRING = 'String',
    MATHEMATICS = 'Mathematics',
    DATA_STRUCTURE = 'Data Structure'
}

/**
 * Utility function to measure algorithm performance
 */
export function measurePerformance<T extends any[], R>(
    fn: (...args: T) => R,
    ...args: T
): { result: R; timeMs: number; memoryUsed?: number } {
    const startMemory = process.memoryUsage?.().heapUsed;
    const startTime = performance.now();

    const result = fn(...args);

    const endTime = performance.now();
    const endMemory = process.memoryUsage?.().heapUsed;

    return {
        result,
        timeMs: endTime - startTime,
        memoryUsed: endMemory && startMemory ? endMemory - startMemory : undefined
    };
}

/**
 * Generate random test data
 */
export class TestDataGenerator {
    static randomArray(size: number, min = 0, max = 1000): number[] {
        return Array.from({ length: size }, () =>
            Math.floor(Math.random() * (max - min + 1)) + min
        );
    }

    static randomString(length: number, charset = 'abcdefghijklmnopqrstuvwxyz'): string {
        let result = '';
        for (let i = 0; i < length; i++) {
            result += charset[Math.floor(Math.random() * charset.length)];
        }
        return result;
    }

    static randomGraph<T>(vertices: T[], edgeProbability = 0.3, directed = false): Map<T, Map<T, number>> {
        const graph = new Map<T, Map<T, number>>();

        for (const vertex of vertices) {
            graph.set(vertex, new Map());
        }

        for (let i = 0; i < vertices.length; i++) {
            for (let j = directed ? 0 : i + 1; j < vertices.length; j++) {
                if (i !== j && Math.random() < edgeProbability) {
                    const weight = Math.floor(Math.random() * 10) + 1;
                    graph.get(vertices[i])!.set(vertices[j], weight);
                    if (!directed) {
                        graph.get(vertices[j])!.set(vertices[i], weight);
                    }
                }
            }
        }

        return graph;
    }
}

// Export all types
export type * from './sorting';
export type * from './graphAlgorithms';