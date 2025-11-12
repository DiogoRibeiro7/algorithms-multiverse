# Automated Documentation Generation System

## Overview

This directory contains a comprehensive automated documentation generation system for the Algorithms Multiverse repository. The system automatically extracts metadata from algorithm implementations across multiple programming languages and generates various forms of documentation.

## Features

### 🔍 Code Parser (`generator/code_parser.py`)
Extracts metadata from source code in multiple languages:
- **Algorithm complexity** (time and space)
- **Function signatures** and docstrings
- **Language-specific features**
- **Code examples** and use cases
- **Supports**: Python, JavaScript, Java, C++, Go, Rust, C, R, and more

### 📚 Documentation Generator (`generator/doc_generator.py`)
Generates comprehensive documentation:
- **Complexity cheat sheets** - Quick reference for algorithm complexities
- **Cross-language comparisons** - Side-by-side implementation comparisons
- **API references** - Detailed function documentation per language
- **Performance reports** - Complexity analysis and recommendations

### 🎓 Tutorial Generator (`generator/tutorial_generator.py`)
Creates learning materials:
- **Learning paths** - Beginner → Intermediate → Advanced curriculum
- **Algorithm tutorials** - Step-by-step guides with examples
- **Quick reference cards** - Fast lookup guides
- **Difficulty assessment** - Automatic difficulty rating (1-5 stars)

### 🎨 Interactive Visualizer (`interactive/algorithm_visualizer.html`)
Visual learning tool:
- **Live algorithm animations** - See algorithms in action
- **Step-by-step execution** - Watch comparisons and swaps
- **Performance metrics** - Real-time comparison and swap counts
- **Multiple algorithms** - Sorting, searching, and more

## Quick Start

### Generate All Documentation

```bash
# From repository root
python docs/generator/generate_docs.py
```

This will:
1. Parse all algorithm implementations
2. Generate complexity cheat sheets
3. Create cross-language comparison guides
4. Generate API references for each language
5. Create learning paths and tutorials
6. Setup interactive visualizations

Output will be in `docs/output/`

### Quick Mode (Skip Tutorials)

```bash
python docs/generator/generate_docs.py --quick
```

### Generate for Specific Category

```bash
# Only process sorting algorithms
python docs/generator/generate_docs.py --category sorting

# Or other categories
python docs/generator/generate_docs.py --category data-structures
python docs/generator/generate_docs.py --category graph-algorithms
```

### Parse Code Only (No Documentation)

```bash
python docs/generator/generate_docs.py --parse-only
```

## Command-Line Tools

### Code Parser

```bash
# Parse all code in current directory
python docs/generator/code_parser.py

# Parse specific directory
python docs/generator/code_parser.py --dir ./sorting

# Parse single file
python docs/generator/code_parser.py --file ./sorting/quicksort.py

# Verbose output
python docs/generator/code_parser.py --verbose
```

### Documentation Generator

```bash
# Generate all documentation
python docs/generator/doc_generator.py

# Generate only cheat sheet
python docs/generator/doc_generator.py --cheatsheet-only

# Generate only comparisons
python docs/generator/doc_generator.py --comparison-only

# Generate only API references
python docs/generator/doc_generator.py --api-only
```

### Tutorial Generator

```bash
# Generate all tutorials
python docs/generator/tutorial_generator.py

# Generate tutorial for specific algorithm
python docs/generator/tutorial_generator.py --algorithm "Binary Search"
```

## Output Structure

```
docs/output/
├── README.md                          # Main index
├── metadata.json                      # Extracted metadata
├── algorithm_visualizer.html          # Interactive visualizer
├── performance_report.md              # Performance analysis
├── cheatsheets/
│   └── complexity_cheatsheet.md       # Complexity reference
├── comparisons/
│   └── implementation_comparison.md   # Cross-language comparison
├── api/
│   ├── python_api.md                  # Python API reference
│   ├── javascript_api.md              # JavaScript API reference
│   ├── java_api.md                    # Java API reference
│   └── ...                            # Other languages
└── tutorials/
    ├── learning_paths.md              # Structured curriculum
    ├── quick_reference.md             # Quick lookup
    └── ...                            # Individual tutorials
```

## Documentation Types

### 1. Complexity Cheat Sheet
Quick reference guide showing time and space complexity for all algorithms, organized by category.

**Use when:** You need to quickly look up an algorithm's complexity.

### 2. Implementation Comparison
Side-by-side comparison of the same algorithm implemented in different languages, showing complexity, features, and key functions.

**Use when:** You want to see how an algorithm varies across languages or choose the best language for your use case.

### 3. API References
Detailed documentation for each language, including function signatures, docstrings, complexity information, and examples.

**Use when:** You need detailed information about a specific implementation.

### 4. Learning Paths
Structured curriculum from beginner to advanced, with recommended learning order and difficulty ratings.

**Use when:** You're learning algorithms systematically.

### 5. Performance Reports
Analysis of theoretical complexity and performance recommendations based on use case.

**Use when:** You need to choose the best algorithm for your specific requirements.

### 6. Interactive Visualizer
Web-based tool for visualizing algorithm execution with animations and real-time metrics.

**Use when:** You want to see how an algorithm works step-by-step.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  generate_docs.py                           │
│              (Main Orchestrator)                            │
└───────────┬─────────────────────────────────────────────────┘
            │
            ├─────────────────────────────────────────────────┐
            │                                                 │
    ┌───────▼────────┐     ┌─────────────┐     ┌────────────▼──────┐
    │  code_parser   │────▶│  metadata   │────▶│  doc_generator    │
    │                │     │   .json     │     │                   │
    └────────────────┘     └─────────────┘     └───────────────────┘
            │                                            │
            │                                            │
    ┌───────▼────────┐                          ┌───────▼───────────┐
    │   Source Code  │                          │   Documentation   │
    │   (.py, .js,   │                          │   (.md, .html)    │
    │    .java, etc) │                          │                   │
    └────────────────┘                          └───────────────────┘
            │
    ┌───────▼────────────┐
    │ tutorial_generator │
    │                    │
    └────────────────────┘
            │
    ┌───────▼────────┐
    │   Tutorials    │
    │   Learning     │
    │   Paths        │
    └────────────────┘
```

## Extending the System

### Adding Support for New Languages

Edit `code_parser.py` and add language patterns:

```python
LANGUAGE_PATTERNS = {
    'newlang': {
        'extension': ['.nl'],
        'comment': ['#', '/*'],
        'function': re.compile(r'pattern_for_functions'),
        'class': re.compile(r'pattern_for_classes'),
        'docstring': re.compile(r'pattern_for_docstrings'),
    }
}
```

### Adding New Documentation Types

1. Create new method in `DocumentationGenerator` class
2. Add output path in `generate_all_documentation()`
3. Call from orchestrator in `generate_docs.py`

### Customizing Templates

Templates are dynamically generated but can be customized by modifying the generator methods in:
- `doc_generator.py` - Main documentation templates
- `tutorial_generator.py` - Tutorial templates

## Integration with Benchmarks

The documentation system can integrate with the existing benchmark framework:

```python
# In doc_generator.py
benchmark_data = load_benchmark_results('benchmarks/results.db')
report = generator.generate_performance_report(benchmark_data)
```

This allows real-world performance data to be included in documentation.

## Requirements

```
Python 3.7+
No external dependencies (uses standard library only)
```

## Maintenance

### Updating Documentation

Documentation should be regenerated whenever:
- New algorithm implementations are added
- Existing implementations are modified
- Complexity information changes
- New languages are added

### Automation

Set up a git hook or CI/CD pipeline to automatically regenerate:

```bash
# .git/hooks/pre-commit
#!/bin/bash
python docs/generator/generate_docs.py --quick
git add docs/output/
```

## Troubleshooting

### Issue: No algorithms found

**Solution:** Check that you're running from the repository root:
```bash
cd /path/to/algorithms-multiverse
python docs/generator/generate_docs.py
```

### Issue: Missing complexity information

**Solution:** Ensure source files have docstrings with complexity info:
```python
"""
Time Complexity: O(n log n)
Space Complexity: O(1)
"""
```

### Issue: Parse errors

**Solution:** Check file encoding and ensure files are valid UTF-8:
```bash
file -i your_file.py  # Check encoding
```

## Examples

### Example 1: Generate docs for new sorting algorithm

```bash
# 1. Implement algorithm
vim sorting/timsort.py

# 2. Add complexity in docstring
"""
Time Complexity: O(n log n)
Space Complexity: O(n)
"""

# 3. Regenerate documentation
python docs/generator/generate_docs.py

# 4. View in docs/output/
```

### Example 2: Compare implementations

```bash
# Generate comparison guide
python docs/generator/doc_generator.py --comparison-only

# Open docs/output/comparisons/implementation_comparison.md
```

### Example 3: Create learning path

```bash
# Generate tutorials
python docs/generator/tutorial_generator.py

# Open docs/output/tutorials/learning_paths.md
```

## Best Practices

1. **Keep docstrings consistent** - Use the same format across languages
2. **Include examples** - Add usage examples in docstrings
3. **Document complexity** - Always specify time and space complexity
4. **Regenerate regularly** - Keep documentation in sync with code
5. **Review generated docs** - Check output for accuracy

## Contributing

When adding new features to the documentation system:

1. Maintain backward compatibility
2. Add comprehensive docstrings
3. Update this README
4. Test with multiple languages
5. Ensure performance at scale (100+ files)

## License

MIT License - Same as main repository

## Support

For issues or questions:
- GitHub Issues: [algorithms-multiverse/issues](https://github.com/anthropics/algorithms-multiverse/issues)
- Documentation: This README
- Examples: See `docs/output/` after generation

---

**Generated with ❤️ by the Algorithms Multiverse Documentation System**
