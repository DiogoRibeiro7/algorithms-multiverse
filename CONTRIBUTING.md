# 🤝 Contributing to Algorithms Multiverse

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 📑 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Review Process](#review-process)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them learn
- Provide constructive feedback
- Focus on technical merit
- Respect different viewpoints

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal attacks
- Publishing others' private information

---

## How Can I Contribute?

### 1. Implement New Algorithms

**Most Needed**:
- Algorithms missing from specific languages
- Advanced algorithms (see [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md))
- Optimized versions of existing algorithms

### 2. Add Language Implementations

Current priorities:
- TypeScript implementations
- Rust data structures
- Go concurrency examples
- Julia scientific algorithms

### 3. Improve Documentation

- Fix typos and grammar
- Add examples
- Improve explanations
- Create tutorials
- Add visualizations

### 4. Add Test Cases

- Edge cases
- Performance tests
- Cross-language validation
- Stress tests

### 5. Performance Optimization

- Identify bottlenecks
- Optimize existing implementations
- Add benchmarking
- Document trade-offs

### 6. Bug Fixes

- Fix incorrect implementations
- Handle edge cases
- Improve error handling

### 7. Enhance Visualizer

- Add new algorithms
- Improve UI/UX
- Add features
- Fix bugs

---

## Getting Started

### Prerequisites

1. **Git** - Version control
2. **Programming language** of choice (Python, Java, C++, etc.)
3. **Text editor** or IDE
4. **GitHub account**

### Fork and Clone

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/algorithms-multiverse.git
cd algorithms-multiverse

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/algorithms-multiverse.git

# 4. Create a branch
git checkout -b feature/your-feature-name
```

### Choose What to Implement

1. Check [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)
2. Look for "🚧 In Progress" or missing implementations
3. Check existing issues for ideas
4. Create an issue to claim what you're working on

---

## Development Workflow

### Step-by-Step Process

1. **Create an issue** (or comment on existing one)
   - Describe what you plan to implement
   - Get feedback before starting

2. **Create a branch**
   ```bash
   git checkout -b feature/algorithm-name-language
   # Example: feature/quicksort-rust
   ```

3. **Implement the algorithm**
   - Follow [Code Style Guidelines](#code-style-guidelines)
   - Add documentation
   - Write tests

4. **Test thoroughly**
   - Run all tests
   - Add new test cases
   - Verify edge cases

5. **Commit changes**
   ```bash
   git add .
   git commit -m "Add QuickSort implementation in Rust"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/algorithm-name-language
   ```

7. **Create Pull Request**
   - Use our [PR template](#pull-request-template)
   - Link related issues
   - Provide clear description

---

## Code Style Guidelines

### General Principles

✅ **DO**:
- Write clear, readable code
- Use descriptive variable names
- Add comments for complex logic
- Follow language conventions
- Include complexity analysis
- Handle edge cases
- Write self-documenting code

❌ **DON'T**:
- Use single-letter variables (except `i, j, k` for loops)
- Write overly clever code
- Copy-paste without understanding
- Ignore edge cases
- Skip documentation

### Language-Specific Guidelines

#### Python

```python
def quick_sort(arr: list[int]) -> list[int]:
    """
    Sorts an array using the QuickSort algorithm.

    Time Complexity: O(n log n) average, O(n²) worst
    Space Complexity: O(log n) due to recursion

    Args:
        arr: List of integers to sort

    Returns:
        Sorted list of integers

    Examples:
        >>> quick_sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)
```

**Python Style**:
- Use type hints (Python 3.9+)
- Follow PEP 8
- Use snake_case for functions and variables
- Docstrings for all public functions
- Use list comprehensions when clear
- Prefer `enumerate()` over manual indexing

#### JavaScript/TypeScript

```typescript
/**
 * Sorts an array using the QuickSort algorithm
 *
 * @param {number[]} arr - Array of numbers to sort
 * @returns {number[]} Sorted array
 *
 * Time Complexity: O(n log n) average, O(n²) worst
 * Space Complexity: O(log n)
 *
 * @example
 * quickSort([3, 1, 4, 1, 5, 9, 2, 6])
 * // Returns: [1, 1, 2, 3, 4, 5, 6, 9]
 */
function quickSort(arr: number[]): number[] {
    if (arr.length <= 1) {
        return arr;
    }

    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);

    return [...quickSort(left), ...middle, ...quickSort(right)];
}
```

**JS/TS Style**:
- Use ES6+ features
- TypeScript with strict mode
- JSDoc comments
- camelCase for functions and variables
- Use `const` and `let`, never `var`
- Arrow functions for callbacks

#### Java

```java
/**
 * QuickSort implementation using divide and conquer.
 *
 * <p>Time Complexity: O(n log n) average, O(n²) worst
 * <p>Space Complexity: O(log n) due to recursion
 *
 * @param arr Array to be sorted
 * @param low Starting index
 * @param high Ending index
 *
 * @example
 * int[] arr = {3, 1, 4, 1, 5, 9, 2, 6};
 * quickSort(arr, 0, arr.length - 1);
 */
public class QuickSort {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, high);
        return i + 1;
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

**Java Style**:
- Follow Oracle Java conventions
- Javadoc for all public methods
- PascalCase for class names
- camelCase for methods and variables
- Use generics where appropriate
- Avoid raw types

#### C++

```cpp
/**
 * @brief Sorts an array using QuickSort algorithm
 *
 * Time Complexity: O(n log n) average, O(n²) worst
 * Space Complexity: O(log n) due to recursion
 *
 * @param arr Vector of integers to sort
 * @param low Starting index
 * @param high Ending index
 *
 * @example
 * vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
 * quickSort(arr, 0, arr.size() - 1);
 */
template<typename T>
void quickSort(std::vector<T>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

template<typename T>
int partition(std::vector<T>& arr, int low, int high) {
    T pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }

    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}
```

**C++ Style**:
- Modern C++ (C++17/20)
- Use STL when appropriate
- Doxygen-style comments
- snake_case or camelCase (be consistent)
- Use smart pointers for memory management
- Prefer `nullptr` over `NULL`

---

## Testing Requirements

### Minimum Test Coverage

Each implementation must include:

1. **Basic functionality test**
   - Unsorted input
   - Already sorted input
   - Reverse sorted input

2. **Edge cases**
   - Empty array
   - Single element
   - Two elements
   - All same elements
   - Negative numbers

3. **Performance test** (optional but recommended)
   - Large input (1000+ elements)
   - Time measurement

### Test Examples

#### Python (pytest)

```python
def test_quick_sort():
    # Basic test
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    # Edge cases
    assert quick_sort([]) == []
    assert quick_sort([1]) == [1]
    assert quick_sort([2, 1]) == [1, 2]
    assert quick_sort([1, 1, 1]) == [1, 1, 1]

    # Negative numbers
    assert quick_sort([-5, 3, -1, 0, 2]) == [-5, -1, 0, 2, 3]

    # Already sorted
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    # Reverse sorted
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
```

#### JavaScript (Jest)

```javascript
describe('Quick Sort', () => {
    test('sorts unsorted array', () => {
        expect(quickSort([3, 1, 4, 1, 5, 9, 2, 6])).toEqual([1, 1, 2, 3, 4, 5, 6, 9]);
    });

    test('handles edge cases', () => {
        expect(quickSort([])).toEqual([]);
        expect(quickSort([1])).toEqual([1]);
        expect(quickSort([2, 1])).toEqual([1, 2]);
    });

    test('handles negative numbers', () => {
        expect(quickSort([-5, 3, -1, 0, 2])).toEqual([-5, -1, 0, 2, 3]);
    });
});
```

---

## Documentation Standards

### Algorithm Documentation

Each algorithm file must include:

1. **File header**:
   ```python
   """
   QuickSort Implementation

   A divide-and-conquer sorting algorithm that picks a pivot element
   and partitions the array around it.

   Author: Your Name
   Date: 2024-01-01
   Language: Python 3.9+
   """
   ```

2. **Complexity analysis**:
   ```python
   # Time Complexity:
   #   - Best case: O(n log n) - pivot always splits evenly
   #   - Average case: O(n log n)
   #   - Worst case: O(n²) - pivot is always min/max
   #
   # Space Complexity: O(log n) - recursion stack
   #
   # Stable: No
   # In-place: Yes (for array version)
   ```

3. **Algorithm explanation**:
   ```python
   # Algorithm Steps:
   # 1. Choose a pivot element
   # 2. Partition array: elements < pivot | pivot | elements > pivot
   # 3. Recursively sort left and right partitions
   # 4. Combine results
   ```

4. **Usage example**:
   ```python
   # Example:
   #   Input:  [3, 1, 4, 1, 5, 9, 2, 6]
   #   Output: [1, 1, 2, 3, 4, 5, 6, 9]
   ```

### README Files

Add or update README files when:
- Creating a new directory
- Adding a new algorithm category
- Implementing a complex algorithm

README should include:
- Overview of algorithms in directory
- Complexity comparison table
- Usage examples
- References to theory

---

## Pull Request Process

### PR Template

```markdown
## Description
Brief description of what this PR adds/fixes.

## Type of Change
- [ ] New algorithm implementation
- [ ] Bug fix
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Visualizer enhancement

## Algorithm Details (if applicable)
- **Algorithm**: QuickSort
- **Language**: Python
- **Time Complexity**: O(n log n) average, O(n²) worst
- **Space Complexity**: O(log n)

## Testing
- [ ] All existing tests pass
- [ ] Added new tests
- [ ] Tested edge cases
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Added documentation/comments
- [ ] Updated README if necessary
- [ ] Tests pass
- [ ] No merge conflicts

## Related Issues
Closes #issue_number
```

### PR Title Format

```
<type>: <description>

Examples:
feat: Add QuickSort implementation in Rust
fix: Correct binary search edge case in Python
docs: Improve complexity guide examples
test: Add test cases for merge sort
perf: Optimize bubble sort with early termination
```

---

## Review Process

### What Reviewers Look For

1. **Correctness**
   - Algorithm works correctly
   - Handles edge cases
   - No bugs

2. **Code Quality**
   - Follows style guide
   - Clear variable names
   - Appropriate comments

3. **Documentation**
   - Proper docstrings/comments
   - Complexity analysis
   - Usage examples

4. **Testing**
   - Adequate test coverage
   - Edge cases tested
   - Tests pass

5. **Performance**
   - Optimal complexity
   - No unnecessary operations
   - Memory efficient

### Response Time

- Initial review: Within 3-5 days
- Follow-up reviews: Within 2-3 days

### Addressing Feedback

1. Read all comments carefully
2. Ask questions if unclear
3. Make requested changes
4. Reply to each comment
5. Request re-review when ready

---

## Recognition

Contributors are recognized in:
- Git commit history
- Contributors list (planned)
- Release notes for major contributions

---

## Questions?

- Open an issue with "question" label
- Join discussions in existing issues
- Reach out to maintainers

---

## Thank You!

Every contribution, no matter how small, helps make this project better for everyone. We appreciate your time and effort!

---

**[⬆ Back to Main README](./README.md)** | **[IMPLEMENTATION_GUIDE](./IMPLEMENTATION_GUIDE.md)** | **[CODE_REVIEW_CHECKLIST](./docs/CODE_REVIEW_CHECKLIST.md)**
