"""
MapReduce Patterns Implementation
==================================

Implementation of the MapReduce programming model for distributed data processing,
including common patterns and use cases.

Key Components:
- Basic MapReduce framework
- Common MapReduce patterns
- Combiner optimization
- Partitioning strategies
- Secondary sorting
- Join operations
- Graph algorithms with MapReduce
- Machine learning with MapReduce

Applications:
- Word count and text analysis
- Log analysis
- PageRank computation
- Distributed grep
- Inverted index creation
- Matrix multiplication
- K-means clustering
- Recommendation systems

Author: Claude
Date: January 2026
"""

import os
import json
import hashlib
import heapq
from typing import List, Tuple, Any, Dict, Callable, Optional, Iterator, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from multiprocessing import Pool, cpu_count
from functools import reduce
import numpy as np
import random
import time


@dataclass
class MapReduceJob:
    """Configuration for a MapReduce job."""
    name: str
    mapper: Callable
    reducer: Callable
    combiner: Optional[Callable] = None
    partitioner: Optional[Callable] = None
    num_reducers: int = 1
    input_format: str = "text"
    output_format: str = "text"


class MapReduceFramework:
    """
    Basic MapReduce framework for local execution.

    Simulates distributed MapReduce with multiprocessing.
    """

    def __init__(self, num_workers: Optional[int] = None):
        """
        Initialize MapReduce framework.

        Args:
            num_workers: Number of worker processes (default: CPU count)
        """
        self.num_workers = num_workers or cpu_count()

    def run(self, job: MapReduceJob, input_data: Any) -> List[Tuple[Any, Any]]:
        """
        Execute MapReduce job.

        Args:
            job: Job configuration
            input_data: Input data (format depends on job)

        Returns:
            Final key-value pairs after reduction
        """
        # Map phase
        print(f"Starting MapReduce job: {job.name}")
        print(f"Map phase with {self.num_workers} workers...")

        map_output = self._map_phase(job, input_data)

        # Combine phase (optional local aggregation)
        if job.combiner:
            print("Combine phase...")
            map_output = self._combine_phase(job, map_output)

        # Shuffle and sort phase
        print("Shuffle and sort phase...")
        shuffled = self._shuffle_sort_phase(job, map_output)

        # Reduce phase
        print(f"Reduce phase with {job.num_reducers} reducers...")
        final_output = self._reduce_phase(job, shuffled)

        print(f"Job {job.name} completed!")
        return final_output

    def _map_phase(self, job: MapReduceJob, input_data: Any) -> List[Tuple[Any, Any]]:
        """Execute map phase in parallel."""
        # Split input data for parallel processing
        if isinstance(input_data, list):
            chunks = self._split_list(input_data, self.num_workers)
        elif isinstance(input_data, str):
            # Text input - split by lines
            lines = input_data.strip().split('\n')
            chunks = self._split_list(lines, self.num_workers)
        else:
            chunks = [input_data]  # Single chunk

        # Parallel mapping
        with Pool(self.num_workers) as pool:
            map_results = pool.map(job.mapper, chunks)

        # Flatten results
        output = []
        for result in map_results:
            if isinstance(result, list):
                output.extend(result)
            else:
                output.append(result)

        return output

    def _combine_phase(self, job: MapReduceJob, map_output: List[Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
        """Local aggregation using combiner."""
        combined = defaultdict(list)

        for key, value in map_output:
            combined[key].append(value)

        output = []
        for key, values in combined.items():
            combined_value = job.combiner(key, values)
            if isinstance(combined_value, list):
                for v in combined_value:
                    output.append((key, v))
            else:
                output.append((key, combined_value))

        return output

    def _shuffle_sort_phase(self, job: MapReduceJob, map_output: List[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
        """Group values by key."""
        shuffled = defaultdict(list)

        for key, value in map_output:
            # Determine reducer using partitioner
            if job.partitioner:
                reducer_id = job.partitioner(key, job.num_reducers)
            else:
                # Default: hash partitioning
                reducer_id = hash(key) % job.num_reducers

            shuffled[key].append(value)

        # Sort keys
        return dict(sorted(shuffled.items()))

    def _reduce_phase(self, job: MapReduceJob, shuffled: Dict[Any, List[Any]]) -> List[Tuple[Any, Any]]:
        """Execute reduce phase."""
        output = []

        for key, values in shuffled.items():
            result = job.reducer(key, values)
            if isinstance(result, list):
                output.extend(result)
            else:
                output.append((key, result))

        return output

    def _split_list(self, data: List[Any], n: int) -> List[List[Any]]:
        """Split list into n roughly equal chunks."""
        chunk_size = max(1, len(data) // n)
        chunks = []

        for i in range(0, len(data), chunk_size):
            chunks.append(data[i:i + chunk_size])

        return chunks


# Common MapReduce Patterns

def word_count_mapper(chunk: List[str]) -> List[Tuple[str, int]]:
    """Map function for word count."""
    output = []
    for line in chunk:
        words = line.lower().split()
        for word in words:
            # Remove punctuation
            word = ''.join(c for c in word if c.isalnum())
            if word:
                output.append((word, 1))
    return output


def word_count_reducer(word: str, counts: List[int]) -> int:
    """Reduce function for word count."""
    return sum(counts)


def word_count_combiner(word: str, counts: List[int]) -> int:
    """Combiner for word count (same as reducer)."""
    return sum(counts)


def inverted_index_mapper(chunk: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Map function for inverted index. Input: (doc_id, content)."""
    output = []
    for doc_id, content in chunk:
        words = content.lower().split()
        word_positions = defaultdict(list)

        for pos, word in enumerate(words):
            word = ''.join(c for c in word if c.isalnum())
            if word:
                word_positions[word].append(pos)

        for word, positions in word_positions.items():
            output.append((word, f"{doc_id}:{positions}"))

    return output


def inverted_index_reducer(word: str, postings: List[str]) -> List[str]:
    """Reduce function for inverted index."""
    return postings


def grep_mapper(pattern: str):
    """Create grep mapper for pattern."""
    def mapper(chunk: List[str]) -> List[Tuple[int, str]]:
        output = []
        for i, line in enumerate(chunk):
            if pattern in line:
                output.append((i, line))
        return output
    return mapper


def grep_reducer(line_num: int, lines: List[str]) -> str:
    """Reduce function for grep (identity)."""
    return lines[0] if lines else ""


class PageRankMapReduce:
    """PageRank implementation using MapReduce."""

    @staticmethod
    def mapper(chunk: List[Tuple[str, Dict[str, Any]]]) -> List[Tuple[str, Any]]:
        """
        Map function for PageRank.
        Input: (node, {rank, neighbors})
        """
        output = []
        for node, data in chunk:
            rank = data['rank']
            neighbors = data['neighbors']
            num_neighbors = len(neighbors)

            # Emit rank contributions
            if num_neighbors > 0:
                contribution = rank / num_neighbors
                for neighbor in neighbors:
                    output.append((neighbor, ('rank', contribution)))

            # Emit graph structure
            output.append((node, ('neighbors', neighbors)))

        return output

    @staticmethod
    def reducer(node: str, values: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """Reduce function for PageRank."""
        damping = 0.85
        rank_sum = 0
        neighbors = []

        for value_type, value in values:
            if value_type == 'rank':
                rank_sum += value
            elif value_type == 'neighbors':
                neighbors = value

        # Calculate new rank
        new_rank = (1 - damping) + damping * rank_sum

        return {'rank': new_rank, 'neighbors': neighbors}


class MatrixMultiplicationMapReduce:
    """Matrix multiplication using MapReduce."""

    @staticmethod
    def mapper(chunk: List[Tuple[str, int, int, float]]) -> List[Tuple[Tuple[int, int], Tuple[str, int, float]]]:
        """
        Map function for matrix multiplication.
        Input: (matrix_name, row, col, value)
        Output: ((i, k), (matrix, j, value))
        """
        output = []
        for matrix_name, i, j, value in chunk:
            if matrix_name == 'A':
                # For A[i,j], emit to all (i, k) for k in columns of B
                for k in range(10):  # Assuming B has 10 columns
                    output.append(((i, k), ('A', j, value)))
            else:  # matrix_name == 'B'
                # For B[j,k], emit to all (i, k) for i in rows of A
                for i in range(10):  # Assuming A has 10 rows
                    output.append(((i, j), ('B', j, value)))
        return output

    @staticmethod
    def reducer(key: Tuple[int, int], values: List[Tuple[str, int, float]]) -> float:
        """Reduce function for matrix multiplication."""
        i, k = key
        a_values = {}
        b_values = {}

        for matrix_name, j, value in values:
            if matrix_name == 'A':
                a_values[j] = value
            else:  # matrix_name == 'B'
                b_values[j] = value

        # Compute dot product
        result = 0
        for j in a_values:
            if j in b_values:
                result += a_values[j] * b_values[j]

        return result


class KMeansMapReduce:
    """K-means clustering using MapReduce."""

    def __init__(self, k: int, dimensions: int):
        """Initialize K-means."""
        self.k = k
        self.dimensions = dimensions
        self.centers = None

    def initialize_centers(self, data: List[np.ndarray]):
        """Initialize cluster centers randomly."""
        self.centers = random.sample(data, self.k)

    def mapper(self, chunk: List[np.ndarray]) -> List[Tuple[int, Tuple[np.ndarray, int]]]:
        """
        Map function for K-means.
        Assigns each point to nearest center.
        """
        output = []
        for point in chunk:
            # Find nearest center
            min_dist = float('inf')
            nearest_center = 0

            for i, center in enumerate(self.centers):
                dist = np.linalg.norm(point - center)
                if dist < min_dist:
                    min_dist = dist
                    nearest_center = i

            # Emit (center_id, (point, 1))
            output.append((nearest_center, (point, 1)))

        return output

    def reducer(self, center_id: int, values: List[Tuple[np.ndarray, int]]) -> np.ndarray:
        """
        Reduce function for K-means.
        Computes new center as mean of assigned points.
        """
        total_point = np.zeros(self.dimensions)
        total_count = 0

        for point, count in values:
            total_point += point
            total_count += count

        if total_count > 0:
            return total_point / total_count
        else:
            return self.centers[center_id]  # Keep old center if no points


class SecondarySort:
    """Secondary sorting in MapReduce."""

    @staticmethod
    def create_composite_key(primary: Any, secondary: Any) -> Tuple[Any, Any]:
        """Create composite key for secondary sorting."""
        return (primary, secondary)

    @staticmethod
    def partitioner(key: Tuple[Any, Any], num_reducers: int) -> int:
        """Partition only by primary key."""
        primary_key = key[0]
        return hash(primary_key) % num_reducers

    @staticmethod
    def mapper(chunk: List[Tuple[Any, Any, Any]]) -> List[Tuple[Tuple[Any, Any], Any]]:
        """Map with composite key."""
        output = []
        for primary, secondary, value in chunk:
            composite_key = (primary, secondary)
            output.append((composite_key, value))
        return output


class JoinOperations:
    """Different join operations in MapReduce."""

    @staticmethod
    def map_side_join(chunk: List[Tuple[str, str, Any]],
                      lookup_table: Dict[str, Any]) -> List[Tuple[str, Tuple[Any, Any]]]:
        """Map-side join using replicated lookup table."""
        output = []
        for table_name, key, value in chunk:
            if key in lookup_table:
                # Join with lookup table
                output.append((key, (value, lookup_table[key])))
        return output

    @staticmethod
    def reduce_side_join_mapper(chunk: List[Tuple[str, str, Any]]) -> List[Tuple[str, Tuple[str, Any]]]:
        """Mapper for reduce-side join."""
        output = []
        for table_name, key, value in chunk:
            # Tag values with table name
            output.append((key, (table_name, value)))
        return output

    @staticmethod
    def reduce_side_join_reducer(key: str, values: List[Tuple[str, Any]]) -> List[Tuple[Any, Any]]:
        """Reducer for reduce-side join."""
        table_a_values = []
        table_b_values = []

        for table_name, value in values:
            if table_name == 'A':
                table_a_values.append(value)
            else:
                table_b_values.append(value)

        # Cartesian product for join
        output = []
        for a_val in table_a_values:
            for b_val in table_b_values:
                output.append((a_val, b_val))

        return output


def word_count_example():
    """Example: Classic word count."""
    print("=" * 60)
    print("WORD COUNT WITH MAPREDUCE")
    print("=" * 60)

    text = """
    MapReduce is a programming model for processing large data sets
    with a parallel distributed algorithm on a cluster
    The model is a specialization of the split apply combine strategy
    """

    framework = MapReduceFramework(num_workers=2)

    job = MapReduceJob(
        name="WordCount",
        mapper=word_count_mapper,
        reducer=word_count_reducer,
        combiner=word_count_combiner,
        num_reducers=1
    )

    result = framework.run(job, text)

    print("\nWord counts:")
    for word, count in sorted(result, key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {word}: {count}")


def inverted_index_example():
    """Example: Building inverted index."""
    print("\n" + "=" * 60)
    print("INVERTED INDEX WITH MAPREDUCE")
    print("=" * 60)

    documents = [
        ("doc1", "the quick brown fox jumps over the lazy dog"),
        ("doc2", "the dog was lazy but the fox was quick"),
        ("doc3", "quick brown foxes are common in the forest")
    ]

    framework = MapReduceFramework(num_workers=2)

    job = MapReduceJob(
        name="InvertedIndex",
        mapper=inverted_index_mapper,
        reducer=inverted_index_reducer,
        num_reducers=1
    )

    # Prepare input
    input_data = []
    for doc in documents:
        input_data.append(doc)

    result = framework.run(job, [documents])

    print("\nInverted index (sample):")
    for word, postings in sorted(result)[:5]:
        print(f"  {word}: {postings}")


def pagerank_example():
    """Example: PageRank computation."""
    print("\n" + "=" * 60)
    print("PAGERANK WITH MAPREDUCE")
    print("=" * 60)

    # Initial graph
    graph = {
        'A': {'rank': 1.0, 'neighbors': ['B', 'C']},
        'B': {'rank': 1.0, 'neighbors': ['C']},
        'C': {'rank': 1.0, 'neighbors': ['A']},
        'D': {'rank': 1.0, 'neighbors': ['C']}
    }

    print("Initial graph:")
    for node, data in graph.items():
        print(f"  {node}: neighbors={data['neighbors']}, rank={data['rank']:.2f}")

    framework = MapReduceFramework(num_workers=2)

    # Run 3 iterations
    for iteration in range(3):
        print(f"\nIteration {iteration + 1}:")

        job = MapReduceJob(
            name=f"PageRank_Iter{iteration}",
            mapper=PageRankMapReduce.mapper,
            reducer=PageRankMapReduce.reducer,
            num_reducers=1
        )

        # Prepare input
        input_data = list(graph.items())
        result = framework.run(job, [input_data])

        # Update graph
        for node, data in result:
            if isinstance(data, dict):
                graph[node] = data

        # Print ranks
        for node in sorted(graph.keys()):
            print(f"  {node}: rank={graph[node]['rank']:.3f}")


def kmeans_example():
    """Example: K-means clustering with MapReduce."""
    print("\n" + "=" * 60)
    print("K-MEANS CLUSTERING WITH MAPREDUCE")
    print("=" * 60)

    # Generate sample 2D data
    np.random.seed(42)
    data = []

    # Generate 3 clusters
    for center in [(0, 0), (5, 5), (10, 0)]:
        for _ in range(30):
            point = np.array(center) + np.random.randn(2) * 0.8
            data.append(point)

    print(f"Generated {len(data)} points in 3 clusters")

    kmeans = KMeansMapReduce(k=3, dimensions=2)
    kmeans.initialize_centers(data[:3])

    framework = MapReduceFramework(num_workers=2)

    # Run iterations
    for iteration in range(5):
        print(f"\nIteration {iteration + 1}:")

        job = MapReduceJob(
            name=f"KMeans_Iter{iteration}",
            mapper=kmeans.mapper,
            reducer=kmeans.reducer,
            num_reducers=1
        )

        result = framework.run(job, [data])

        # Update centers
        new_centers = []
        for center_id, new_center in result:
            new_centers.append(new_center)

        # Check convergence
        converged = True
        for i in range(len(new_centers)):
            if not np.allclose(kmeans.centers[i], new_centers[i], atol=0.01):
                converged = False
                break

        kmeans.centers = new_centers

        print("Cluster centers:")
        for i, center in enumerate(kmeans.centers):
            print(f"  Cluster {i}: ({center[0]:.2f}, {center[1]:.2f})")

        if converged:
            print("Converged!")
            break


def log_analysis_example():
    """Example: Log analysis with MapReduce."""
    print("\n" + "=" * 60)
    print("LOG ANALYSIS WITH MAPREDUCE")
    print("=" * 60)

    # Sample log entries
    logs = [
        "2024-01-15 10:23:45 ERROR Database connection failed",
        "2024-01-15 10:24:01 INFO User login successful",
        "2024-01-15 10:24:15 WARNING Memory usage high",
        "2024-01-15 10:24:30 ERROR Database connection failed",
        "2024-01-15 10:25:00 INFO Request processed",
        "2024-01-15 10:25:15 ERROR File not found",
        "2024-01-15 10:25:30 INFO User logout",
        "2024-01-15 10:26:00 WARNING Disk space low",
    ]

    def log_level_mapper(chunk: List[str]) -> List[Tuple[str, int]]:
        """Count log levels."""
        output = []
        for line in chunk:
            parts = line.split()
            if len(parts) >= 3:
                level = parts[2]
                output.append((level, 1))
        return output

    def error_mapper(chunk: List[str]) -> List[Tuple[str, str]]:
        """Extract error messages."""
        output = []
        for line in chunk:
            if "ERROR" in line:
                parts = line.split("ERROR")
                if len(parts) > 1:
                    error_msg = parts[1].strip()
                    output.append(("ERROR", error_msg))
        return output

    framework = MapReduceFramework(num_workers=2)

    # Count log levels
    print("Log level distribution:")
    job1 = MapReduceJob(
        name="LogLevelCount",
        mapper=log_level_mapper,
        reducer=word_count_reducer,
        num_reducers=1
    )

    result1 = framework.run(job1, logs)
    for level, count in sorted(result1):
        print(f"  {level}: {count}")

    # Extract errors
    print("\nError messages:")
    job2 = MapReduceJob(
        name="ErrorExtraction",
        mapper=error_mapper,
        reducer=lambda k, v: v,  # Just collect
        num_reducers=1
    )

    result2 = framework.run(job2, logs)
    for _, messages in result2:
        if isinstance(messages, list):
            for msg in messages:
                print(f"  - {msg}")
        else:
            print(f"  - {messages}")


def performance_test():
    """Test MapReduce performance on different data sizes."""
    print("\n" + "=" * 60)
    print("MAPREDUCE PERFORMANCE TEST")
    print("=" * 60)

    # Generate test data
    data_sizes = [100, 1000, 10000]

    for size in data_sizes:
        # Generate random text
        words = ['apple', 'banana', 'cherry', 'date', 'elderberry',
                'fig', 'grape', 'honeydew', 'kiwi', 'lemon']
        text_lines = []
        for _ in range(size):
            line = ' '.join(random.choices(words, k=10))
            text_lines.append(line)
        text = '\n'.join(text_lines)

        # Test with different worker counts
        for num_workers in [1, 2, 4]:
            framework = MapReduceFramework(num_workers=num_workers)

            job = MapReduceJob(
                name=f"WordCount_{size}_{num_workers}",
                mapper=word_count_mapper,
                reducer=word_count_reducer,
                combiner=word_count_combiner,
                num_reducers=1
            )

            start_time = time.time()
            result = framework.run(job, text)
            elapsed = time.time() - start_time

            print(f"Data size: {size} lines, Workers: {num_workers}, "
                  f"Time: {elapsed*1000:.2f}ms, "
                  f"Unique words: {len(result)}")


if __name__ == "__main__":
    # Run examples
    word_count_example()
    inverted_index_example()
    pagerank_example()
    kmeans_example()
    log_analysis_example()
    performance_test()

    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("- MapReduce simplifies distributed data processing")
    print("- Map phase processes data in parallel")
    print("- Shuffle groups data by key")
    print("- Reduce phase aggregates grouped data")
    print("- Combiners optimize by local aggregation")
    print("- Suitable for embarrassingly parallel problems")
    print("=" * 60)