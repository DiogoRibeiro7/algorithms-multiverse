# Python Modernization Guide

This document describes the modern Python 3.10+ features implemented across the algorithms-multiverse codebase.

## Overview

The Python implementations have been modernized to leverage the latest Python features for:
- Better type safety
- Improved performance
- Cleaner code
- Enhanced maintainability

## Modern Features Implemented

### 1. Python 3.10+ Type Hints

#### Union Types with `|` Syntax
```python
# Old style
from typing import Union, Optional
result: Union[int, str] = get_value()
maybe_value: Optional[str] = None

# Modern style (Python 3.10+)
result: int | str = get_value()
maybe_value: str | None = None
```

#### Type Aliases
```python
# Modern type aliases
StringPair: type = tuple[str, str]
DistanceMatrix: type = list[list[int]]
Number: type = int | float
```

### 2. Structural Pattern Matching (match/case)

```python
def analyze_performance(comparisons: int, swaps: int) -> str:
    match (comparisons, swaps):
        case (0, 0):
            return "No operations performed"
        case (comp, 0) if comp > 0:
            return f"Read-only: {comp} comparisons"
        case (comp, swaps) if swaps > comp * 2:
            return f"Write-heavy algorithm"
        case _:
            return f"Standard performance"
```

### 3. Protocols for Duck Typing

```python
from typing import Protocol

class Comparable(Protocol):
    """Protocol for comparable objects."""
    def __lt__(self, other: Any, /) -> bool: ...
    def __gt__(self, other: Any, /) -> bool: ...
    def __eq__(self, other: Any, /) -> bool: ...

def sort_items(items: list[Comparable]) -> list[Comparable]:
    """Works with any comparable type."""
    return sorted(items)
```

### 4. Dataclasses and Frozen Dataclasses

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class AlgorithmMetrics:
    """Immutable metrics for algorithm performance."""
    name: str
    comparisons: int
    swaps: int
    time_ms: float

    @property
    def operations(self) -> int:
        return self.comparisons + self.swaps

@dataclass
class SortResult:
    """Mutable result container."""
    data: list[int]
    metrics: AlgorithmMetrics
    is_stable: bool = True
```

### 5. Advanced Generic Types

#### ParamSpec for Preserving Function Signatures
```python
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
T = TypeVar("T")

def timer(func: Callable[P, T]) -> Callable[P, tuple[T, float]]:
    """Decorator that preserves function signature."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[T, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed
    return wrapper
```

#### TypeVarTuple for Variadic Generics
```python
from typing import TypeVarTuple

Ts = TypeVarTuple("Ts")

def process_args(*args: *Ts) -> tuple[*Ts]:
    """Process variable number of typed arguments."""
    return args
```

### 6. Type Guards for Type Narrowing

```python
from typing import TypeGuard

def is_list_of_ints(data: list[Any]) -> TypeGuard[list[int]]:
    """Type guard to narrow list[Any] to list[int]."""
    return all(isinstance(x, int) for x in data)

def process_data(data: list[Any]) -> list[int]:
    if is_list_of_ints(data):
        # Type checker knows data is list[int] here
        return sorted(data)
    raise TypeError("Expected list of integers")
```

### 7. Context Managers

```python
from contextlib import contextmanager
from collections.abc import Iterator

@contextmanager
def algorithm_timer(name: str) -> Iterator[dict[str, float]]:
    """Context manager for timing algorithms."""
    stats: dict[str, float] = {}
    start = time.perf_counter()

    try:
        yield stats
    finally:
        stats["elapsed_ms"] = (time.perf_counter() - start) * 1000
        print(f"[{name}] Completed in {stats['elapsed_ms']:.2f}ms")

# Usage
with algorithm_timer("Quick Sort") as stats:
    quick_sort(data)
print(f"Took {stats['elapsed_ms']:.2f}ms")
```

### 8. Async/Await Patterns

```python
async def async_merge_sort(arr: list[T]) -> list[T]:
    """Asynchronous merge sort for concurrent processing."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    # Sort both halves concurrently
    left_task = asyncio.create_task(async_merge_sort(arr[:mid]))
    right_task = asyncio.create_task(async_merge_sort(arr[mid:]))

    left = await left_task
    right = await right_task

    return merge(left, right)

# Parallel processing
async def process_multiple_datasets(
    datasets: list[list[T]],
    algorithm: Callable[[list[T]], list[T]]
) -> list[list[T]]:
    """Process multiple datasets concurrently."""
    tasks = [asyncio.create_task(async_execute(algorithm, data))
             for data in datasets]
    return await asyncio.gather(*tasks)
```

### 9. functools Optimizations

#### lru_cache for Memoization
```python
@functools.lru_cache(maxsize=1024)
def fibonacci(n: int) -> int:
    """Fibonacci with automatic caching."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

#### cached_property for Lazy Evaluation
```python
class Algorithm:
    def __init__(self, data: list[int]):
        self.data = data

    @functools.cached_property
    def sorted_data(self) -> list[int]:
        """Computed once and cached."""
        print("Computing sorted data...")
        return sorted(self.data)
```

#### singledispatch for Method Overloading
```python
@functools.singledispatch
def process(value: Any) -> str:
    return f"Generic: {value}"

@process.register
def _(value: int) -> str:
    return f"Integer: {value:,}"

@process.register
def _(value: list) -> str:
    return f"List of {len(value)} items"
```

### 10. Enums for Type Safety

```python
from enum import Enum, auto

class SortAlgorithm(Enum):
    """Enumeration of sorting algorithms."""
    BUBBLE = auto()
    INSERTION = auto()
    SELECTION = auto()
    MERGE = auto()
    QUICK = auto()
    HEAP = auto()

class DataPattern(Enum):
    """Common data patterns."""
    RANDOM = auto()
    SORTED = auto()
    REVERSED = auto()
    NEARLY_SORTED = auto()
```

## Files Updated

### Core Implementations

1. **`python_modern_patterns.py`** - Comprehensive showcase of all modern Python features
   - Pattern matching examples
   - Protocol definitions
   - Dataclasses and frozen dataclasses
   - Advanced generic types
   - Context managers
   - Async patterns
   - functools optimizations

2. **`async_algorithms.py`** - Asynchronous algorithm processing
   - Async sorting algorithms
   - Parallel benchmarking
   - Concurrent data processing
   - Progress tracking
   - Async file I/O

3. **`edit_distance.py`** - Enhanced with modern features
   - Dataclasses for results
   - Pattern matching for edge cases
   - Union types
   - Protocols for interfaces
   - functools.lru_cache for performance

## Best Practices

### Type Hints
- Always use `from __future__ import annotations` for forward references
- Prefer `list[T]` over `List[T]` (Python 3.9+)
- Use `|` for unions instead of `Union` (Python 3.10+)
- Use `type` keyword for type aliases (Python 3.12+)

### Dataclasses
- Use `frozen=True` for immutable data
- Use `field(default_factory=...)` for mutable defaults
- Add `__post_init__` for validation
- Use `@property` for computed fields

### Pattern Matching
- Use for complex conditional logic
- Match on data structure patterns
- Combine with guards (`if` conditions)
- Use `case _:` for default cases

### Async/Await
- Use for I/O-bound operations
- Use `asyncio.gather()` for concurrent execution
- Use `asyncio.Semaphore` for rate limiting
- Use `create_task()` for fire-and-forget tasks

### Performance
- Use `@functools.lru_cache` for expensive pure functions
- Use `@functools.cached_property` for expensive computations
- Use `itertools` for memory-efficient iterations
- Profile before optimizing

## Running the Examples

### Modern Patterns Showcase
```bash
python python_modern_patterns.py
```

### Async Algorithms Demo
```bash
python async_algorithms.py
```

### Edit Distance with Modern Features
```bash
python string-algorithms/edit_distance.py
```

## Requirements

- Python 3.10+ (for structural pattern matching)
- Python 3.11+ (for better performance)
- Python 3.12+ (for type keyword)

## Performance Improvements

The modernizations provide:

1. **Type Safety**: Catch errors at development time with type checkers
2. **Performance**: `lru_cache` and `cached_property` reduce redundant computations
3. **Concurrency**: Async enables parallel processing for better throughput
4. **Maintainability**: Clearer code with dataclasses and pattern matching
5. **Memory Efficiency**: Frozen dataclasses and efficient iterations

## Migration Guide

### Updating Existing Code

1. **Add Future Import**
   ```python
   from __future__ import annotations
   ```

2. **Update Type Hints**
   ```python
   # Before
   from typing import List, Dict, Optional, Union

   def process(data: List[int]) -> Optional[Dict[str, Union[int, str]]]:
       ...

   # After
   def process(data: list[int]) -> dict[str, int | str] | None:
       ...
   ```

3. **Convert to Dataclasses**
   ```python
   # Before
   class Result:
       def __init__(self, value: int, status: str):
           self.value = value
           self.status = status

   # After
   @dataclass(frozen=True)
   class Result:
       value: int
       status: str
   ```

4. **Add Pattern Matching**
   ```python
   # Before
   if len(data) == 0:
       return default_value
   elif len(data) == 1:
       return data[0]
   else:
       return process(data)

   # After
   match len(data):
       case 0:
           return default_value
       case 1:
           return data[0]
       case _:
           return process(data)
   ```

## Contributing

When adding new algorithms:
1. Use modern type hints
2. Add dataclasses for structured data
3. Use pattern matching where appropriate
4. Consider async variants for I/O operations
5. Add functools decorators for optimization
6. Include comprehensive docstrings
7. Add usage examples

## References

- [Python 3.10 Release Notes](https://docs.python.org/3/whatsnew/3.10.html)
- [Python 3.11 Release Notes](https://docs.python.org/3/whatsnew/3.11.html)
- [Python 3.12 Release Notes](https://docs.python.org/3/whatsnew/3.12.html)
- [PEP 634 – Structural Pattern Matching](https://peps.python.org/pep-0634/)
- [PEP 604 – Union Types with |](https://peps.python.org/pep-0604/)
- [PEP 544 – Protocols](https://peps.python.org/pep-0544/)
- [PEP 612 – ParamSpec](https://peps.python.org/pep-0612/)
- [PEP 646 – TypeVarTuple](https://peps.python.org/pep-0646/)

---

**Note**: Most of the existing Python files in this codebase are already quite modern with comprehensive type hints, docstrings, and good patterns. The additions focus on Python 3.10+ specific features and async patterns for enhanced functionality.
