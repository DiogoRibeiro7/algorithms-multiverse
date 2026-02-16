# Usage

Below are short, runnable snippets that exercise core modules. Each example uses real
functions/classes that ship in the repository.

## 1. Build and traverse a graph
```python
from algorithms_multiverse.graph import Graph, GraphType

# Undirected graph with five vertices
graph = Graph(num_vertices=5, graph_type=GraphType.UNDIRECTED)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)

print("Breadth-first traversal from 0:", graph.bfs(0))
```

## 2. Run a quick MST benchmark
```python
from algorithms_multiverse.mst_benchmark import GraphGenerator, MSTBenchmark

benchmark = MSTBenchmark()
result = benchmark.run_benchmark(
    graph_type="random",
    num_vertices=12,
    num_runs=3,
    edge_probability=0.4,
)
print("Average Kruskal runtime (ms):", result["algorithms"]["kruskal"]["mean"])
```

## 3. Process datasets concurrently
```python
import asyncio
from async_algorithms import async_process_datasets

async def main() -> None:
    datasets = [list(range(10, 0, -1)) for _ in range(4)]
    results = await async_process_datasets(datasets, sorted, max_concurrent=2)
    for entry in results:
        print(entry.algorithm_name, entry.output_data[:3])

asyncio.run(main())
```

Each snippet can be copied into a Python REPL or standalone script once the repository is on
your `PYTHONPATH` (cloning the repo and activating the virtual environment is sufficient).
