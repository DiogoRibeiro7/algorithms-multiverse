"""
MapReduce Framework Implementation

This module implements a simple but functional MapReduce framework for
distributed/parallel processing of large datasets.

Features:
- Generic Map and Reduce interfaces
- Parallel execution using multiprocessing
- Partitioning and shuffling
- Combining for optimization
- Multiple examples (word count, inverted index, etc.)

The MapReduce model:
1. Map: Process input and emit key-value pairs
2. Shuffle: Group values by key
3. Reduce: Aggregate values for each key

Time Complexity: Depends on map and reduce functions
Scalability: Near-linear with number of workers

When to use MapReduce:
- Large dataset processing
- Embarrassingly parallel problems
- Aggregation over groups
- Data analysis and ETL

Author: Algorithms Multiverse
"""

import concurrent.futures
import multiprocessing as mp
from multiprocessing import Manager
import time
from typing import List, Tuple, Dict, Callable, Any, Iterable
from dataclasses import dataclass
from collections import defaultdict
import itertools
import os


# Type aliases
Key = Any
Value = Any
KeyValuePair = Tuple[Key, Value]


@dataclass
class MapReduceResult:
    """Results from MapReduce job with performance metrics"""
    results: Dict[Key, Value]
    time_taken: float
    map_time: float
    shuffle_time: float
    reduce_time: float
    num_mappers: int
    num_reducers: int
    keys_processed: int


class MapReduceFramework:
    """
    Simple MapReduce framework for parallel data processing.

    Follows the classic MapReduce paradigm:
    - Map phase: Transform input data to key-value pairs
    - Shuffle phase: Group values by key
    - Reduce phase: Aggregate values for each key
    """

    def __init__(self, num_mappers: int = None, num_reducers: int = None):
        """
        Initialize MapReduce framework.

        Args:
            num_mappers: Number of map workers (default: cpu_count)
            num_reducers: Number of reduce workers (default: cpu_count)
        """
        self.num_mappers = num_mappers or mp.cpu_count()
        self.num_reducers = num_reducers or mp.cpu_count()

    def map_reduce(self,
                   inputs: List[Any],
                   mapper: Callable[[Any], Iterable[KeyValuePair]],
                   reducer: Callable[[Key, Iterable[Value]], Value],
                   combiner: Callable[[Key, Iterable[Value]], Value] = None,
                   partitioner: Callable[[Key], int] = None) -> MapReduceResult:
        """
        Execute MapReduce job.

        Args:
            inputs: List of input items to process
            mapper: Function that maps input to key-value pairs
            reducer: Function that reduces values for a key
            combiner: Optional combiner for optimization (local reduce)
            partitioner: Optional custom partitioner for key distribution

        Returns:
            MapReduceResult with results and metrics
        """
        start_time = time.perf_counter()

        # ===== MAP PHASE =====
        map_start = time.perf_counter()
        mapped_results = self._map_phase(inputs, mapper, combiner)
        map_time = time.perf_counter() - map_start

        # ===== SHUFFLE PHASE =====
        shuffle_start = time.perf_counter()
        shuffled_results = self._shuffle_phase(mapped_results, partitioner)
        shuffle_time = time.perf_counter() - shuffle_start

        # ===== REDUCE PHASE =====
        reduce_start = time.perf_counter()
        final_results = self._reduce_phase(shuffled_results, reducer)
        reduce_time = time.perf_counter() - reduce_start

        total_time = time.perf_counter() - start_time

        return MapReduceResult(
            results=final_results,
            time_taken=total_time,
            map_time=map_time,
            shuffle_time=shuffle_time,
            reduce_time=reduce_time,
            num_mappers=self.num_mappers,
            num_reducers=self.num_reducers,
            keys_processed=len(final_results)
        )

    def _map_phase(self,
                   inputs: List[Any],
                   mapper: Callable[[Any], Iterable[KeyValuePair]],
                   combiner: Callable[[Key, Iterable[Value]], Value] = None) -> List[List[KeyValuePair]]:
        """
        Map phase: Apply mapper to each input in parallel.

        Args:
            inputs: Input items
            mapper: Mapper function
            combiner: Optional combiner function

        Returns:
            List of key-value pairs from each mapper
        """
        # Split inputs among mappers
        chunk_size = max(1, len(inputs) // self.num_mappers)
        input_chunks = [inputs[i:i + chunk_size]
                       for i in range(0, len(inputs), chunk_size)]

        def map_worker(chunk: List[Any]) -> List[KeyValuePair]:
            """Process a chunk of inputs"""
            results = []
            for item in chunk:
                results.extend(mapper(item))

            # Apply combiner if provided (local aggregation)
            if combiner:
                grouped = defaultdict(list)
                for key, value in results:
                    grouped[key].append(value)

                results = [(key, combiner(key, values))
                          for key, values in grouped.items()]

            return results

        # Execute mappers in parallel
        with mp.Pool(processes=self.num_mappers) as pool:
            mapped_results = pool.map(map_worker, input_chunks)

        return mapped_results

    def _shuffle_phase(self,
                      mapped_results: List[List[KeyValuePair]],
                      partitioner: Callable[[Key], int] = None) -> List[Dict[Key, List[Value]]]:
        """
        Shuffle phase: Group values by key and partition.

        Args:
            mapped_results: Results from map phase
            partitioner: Optional custom partitioner

        Returns:
            Partitioned data for reducers
        """
        # Default hash-based partitioner
        if partitioner is None:
            partitioner = lambda key: hash(key) % self.num_reducers

        # Initialize partitions for each reducer
        partitions = [defaultdict(list) for _ in range(self.num_reducers)]

        # Distribute key-value pairs to partitions
        for mapper_result in mapped_results:
            for key, value in mapper_result:
                partition_id = partitioner(key)
                partitions[partition_id][key].append(value)

        return partitions

    def _reduce_phase(self,
                     partitions: List[Dict[Key, List[Value]]],
                     reducer: Callable[[Key, Iterable[Value]], Value]) -> Dict[Key, Value]:
        """
        Reduce phase: Apply reducer to each key's values in parallel.

        Args:
            partitions: Partitioned data
            reducer: Reducer function

        Returns:
            Final results dictionary
        """
        def reduce_worker(partition: Dict[Key, List[Value]]) -> Dict[Key, Value]:
            """Process a partition"""
            results = {}
            for key, values in partition.items():
                results[key] = reducer(key, values)
            return results

        # Execute reducers in parallel
        with mp.Pool(processes=self.num_reducers) as pool:
            reduced_results = pool.map(reduce_worker, partitions)

        # Merge results from all reducers
        final_results = {}
        for result in reduced_results:
            final_results.update(result)

        return final_results


# ===== EXAMPLE APPLICATIONS =====

class WordCount:
    """Classic word count example"""

    @staticmethod
    def mapper(text: str) -> Iterable[KeyValuePair]:
        """Map: Split text into words and emit (word, 1)"""
        words = text.lower().split()
        for word in words:
            # Clean word
            word = ''.join(c for c in word if c.isalnum())
            if word:
                yield (word, 1)

    @staticmethod
    def reducer(key: str, values: Iterable[int]) -> int:
        """Reduce: Sum counts for each word"""
        return sum(values)

    @staticmethod
    def combiner(key: str, values: Iterable[int]) -> int:
        """Combiner: Local sum (same as reducer)"""
        return sum(values)


class InvertedIndex:
    """Inverted index example for search engines"""

    @staticmethod
    def mapper(doc_text: Tuple[str, str]) -> Iterable[KeyValuePair]:
        """Map: Emit (word, document_id) for each word"""
        doc_id, text = doc_text
        words = text.lower().split()
        seen = set()

        for word in words:
            word = ''.join(c for c in word if c.isalnum())
            if word and word not in seen:
                yield (word, doc_id)
                seen.add(word)

    @staticmethod
    def reducer(key: str, values: Iterable[str]) -> List[str]:
        """Reduce: Collect all document IDs for a word"""
        return list(set(values))


class AverageCalculator:
    """Calculate average values by key"""

    @staticmethod
    def mapper(key_value: Tuple[str, float]) -> Iterable[KeyValuePair]:
        """Map: Emit (key, (value, 1))"""
        key, value = key_value
        yield (key, (value, 1))

    @staticmethod
    def reducer(key: str, values: Iterable[Tuple[float, int]]) -> float:
        """Reduce: Calculate average"""
        total_sum = 0
        total_count = 0

        for value, count in values:
            total_sum += value
            total_count += count

        return total_sum / total_count if total_count > 0 else 0

    @staticmethod
    def combiner(key: str, values: Iterable[Tuple[float, int]]) -> Tuple[float, int]:
        """Combiner: Local sum and count"""
        total_sum = 0
        total_count = 0

        for value, count in values:
            total_sum += value
            total_count += count

        return (total_sum, total_count)


class GroupBy:
    """Generic group-by aggregation"""

    @staticmethod
    def create_mapper(key_func: Callable, value_func: Callable):
        """Create mapper that groups by key_func"""
        def mapper(item):
            key = key_func(item)
            value = value_func(item)
            yield (key, value)
        return mapper

    @staticmethod
    def create_reducer(agg_func: Callable):
        """Create reducer that aggregates with agg_func"""
        def reducer(key, values):
            return agg_func(values)
        return reducer


def benchmark_word_count(num_documents: int, words_per_doc: int) -> MapReduceResult:
    """Benchmark word count on random documents"""
    import random

    # Generate random documents
    words = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog',
             'hello', 'world', 'python', 'mapreduce', 'parallel', 'computing']

    documents = []
    for _ in range(num_documents):
        doc = ' '.join(random.choice(words) for _ in range(words_per_doc))
        documents.append(doc)

    # Run MapReduce
    mr = MapReduceFramework()
    result = mr.map_reduce(
        inputs=documents,
        mapper=WordCount.mapper,
        reducer=WordCount.reducer,
        combiner=WordCount.combiner
    )

    return result


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("MAPREDUCE FRAMEWORK DEMONSTRATION")
    print("=" * 80)

    # Example 1: Word Count
    print("\n" + "=" * 80)
    print("Example 1: Word Count")
    print("=" * 80)

    documents = [
        "the quick brown fox jumps over the lazy dog",
        "the lazy dog sleeps under the tree",
        "the quick fox is very quick and clever",
        "python mapreduce is powerful for parallel computing"
    ]

    mr = MapReduceFramework(num_mappers=2, num_reducers=2)
    result = mr.map_reduce(
        inputs=documents,
        mapper=WordCount.mapper,
        reducer=WordCount.reducer,
        combiner=WordCount.combiner
    )

    print(f"\nWord counts:")
    for word, count in sorted(result.results.items(), key=lambda x: -x[1])[:10]:
        print(f"  {word}: {count}")

    print(f"\nPerformance:")
    print(f"  Total time: {result.time_taken:.4f}s")
    print(f"  Map time: {result.map_time:.4f}s")
    print(f"  Shuffle time: {result.shuffle_time:.4f}s")
    print(f"  Reduce time: {result.reduce_time:.4f}s")
    print(f"  Unique words: {result.keys_processed}")

    # Example 2: Inverted Index
    print("\n" + "=" * 80)
    print("Example 2: Inverted Index")
    print("=" * 80)

    doc_collection = [
        ("doc1", "python programming language"),
        ("doc2", "java programming language"),
        ("doc3", "python data science"),
        ("doc4", "machine learning python")
    ]

    result = mr.map_reduce(
        inputs=doc_collection,
        mapper=InvertedIndex.mapper,
        reducer=InvertedIndex.reducer
    )

    print(f"\nInverted index:")
    for word, docs in sorted(result.results.items())[:5]:
        print(f"  {word}: {docs}")

    # Example 3: Benchmark
    print("\n" + "=" * 80)
    print("Example 3: Scalability Benchmark")
    print("=" * 80)

    sizes = [100, 500, 1000]

    print(f"\n{'Documents':<12} {'Words/Doc':<12} {'Time (s)':<12} {'Throughput':<15}")
    print("-" * 80)

    for num_docs in sizes:
        words_per_doc = 100
        result = benchmark_word_count(num_docs, words_per_doc)

        throughput = (num_docs * words_per_doc) / result.time_taken

        print(f"{num_docs:<12} {words_per_doc:<12} "
              f"{result.time_taken:>10.4f}  "
              f"{throughput:>13,.0f} words/s")

    print("\n" + "=" * 80)
    print("WHEN TO USE MAPREDUCE")
    print("=" * 80)
    print("""
MapReduce is beneficial when:

✓ Large datasets that don't fit in memory
✓ Embarrassingly parallel problems
✓ Aggregation and grouping operations
✓ ETL (Extract, Transform, Load) pipelines
✓ Log analysis and data mining

Key advantages:
✓ Simple programming model
✓ Automatic parallelization
✓ Fault tolerance (in distributed systems)
✓ Scalability to thousands of machines

MapReduce phases:
1. Map: Transform input to key-value pairs
2. Shuffle: Group values by key (automatic)
3. Reduce: Aggregate values for each key

Optimization techniques:
✓ Combiner: Local reduction (reduces shuffle)
✓ Partitioner: Custom key distribution
✓ In-mapper combining: Reduce intermediate data

Common applications:
- Word count and text analysis
- Inverted index for search
- Log aggregation
- Data deduplication
- Join operations
- PageRank and graph algorithms

Performance characteristics:
- Map phase: Embarrassingly parallel
- Shuffle phase: Communication bottleneck
- Reduce phase: Parallel per key
- Scalability: Limited by shuffle and reduce

Best practices:
1. Use combiner to reduce shuffle data
2. Balance partitioner for even load distribution
3. Minimize intermediate data size
4. Consider data locality
5. Profile to identify bottlenecks

vs. Other frameworks:
+ MapReduce: Simple, proven, fault-tolerant
- MapReduce: Rigid model, disk I/O heavy
+ Spark: In-memory, flexible, faster
+ Flink: Streaming, low-latency
    """)

    print("\nDemonstration complete!")
