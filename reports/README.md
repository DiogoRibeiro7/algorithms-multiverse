# 📊 Automated Performance Analysis & Reporting System

**Comprehensive performance benchmarking, analysis, and reporting for the Algorithms Multiverse project.**

---

## 🎯 Overview

This system provides automated performance analysis across all algorithm implementations with:
- **Multi-language benchmarking** (Python, JavaScript, Java, C++, Go, Rust, etc.)
- **Statistical analysis** with confidence intervals and distribution analysis
- **Trend detection** and performance regression alerts
- **Memory profiling** for resource usage tracking
- **Interactive dashboards** with charts and visualizations
- **Multiple report formats** (HTML, PDF, Markdown, JSON)
- **CI/CD integration** for continuous performance monitoring

---

## 🚀 Quick Start

### Basic Usage

```bash
# Run full performance analysis
python reports/generator.py

# Quick benchmark for specific algorithm
python reports/generator.py --mode quick --algorithm quicksort --language python

# Compare implementations across languages
python reports/generator.py --mode compare --algorithm mergesort --languages python java cpp

# Analyze scalability
python reports/generator.py --mode scalability --algorithm binarysearch --language python
```

### Installation

```bash
# Install Python dependencies
pip install -r reports/requirements.txt

# Or use conda
conda env create -f reports/environment.yml
conda activate algo-perf
```

### Dependencies

- Python 3.9+
- NumPy, SciPy (statistical analysis)
- Matplotlib, Plotly (visualization)
- Jinja2 (templating)
- ReportLab (PDF generation)
- psutil (memory profiling)

---

## 📁 Directory Structure

```
reports/
├── generator.py                  # Main entry point
├── config.json                   # Configuration file
├── requirements.txt              # Python dependencies
├──  README.md                     # This file
│
├── analysis/                     # Analysis modules
│   ├── benchmark_runner.py      # Execute benchmarks
│   ├── statistical_analyzer.py  # Statistical analysis
│   ├── trend_detector.py        # Trend & regression detection
│   ├── memory_profiler.py       # Memory usage profiling
│   └── recommendation_engine.py # Algorithm recommendations
│
├── dashboard/                    # Report generators
│   ├── html_generator.py        # HTML dashboard with charts
│   ├── pdf_generator.py         # PDF report generation
│   └── markdown_generator.py    # Markdown summaries
│
├── database/                     # Data persistence
│   └── performance_db.py        # SQLite database management
│
├── alerts/                       # Alert system
│   └── alert_manager.py         # Email/Slack notifications
│
├── templates/                    # Report templates
│   ├── dashboard.html           # HTML dashboard template
│   ├── report.html              # PDF report template
│   └── summary.md               # Markdown template
│
├── data/                         # Data storage
│   ├── performance.db           # Performance database
│   └── cache/                   # Temporary cache
│
├── output/                       # Generated reports
│   ├── latest -> YYYYMMDD_HHMMSS/
│   └── YYYYMMDD_HHMMSS/
│       ├── dashboard.html
│       ├── report.pdf
│       ├── summary.md
│       └── performance_data.json
│
└── logs/                         # Log files
    └── generator.log
```

---

## ⚙️ Configuration

### config.json

```json
{
  "database_path": "reports/data/performance.db",
  "output_dir": "reports/output",
  "benchmark_iterations": 100,
  "input_sizes": [10, 100, 1000, 10000],
  "languages": ["python", "javascript", "java", "cpp", "go", "rust"],
  "algorithm_categories": [
    "sorting",
    "searching",
    "graph-algorithms",
    "dynamic-programming"
  ],
  "regression_threshold": 0.10,
  "memory_profiling_enabled": true,
  "generate_html": true,
  "generate_pdf": true,
  "generate_markdown": true,
  "generate_json": true,
  "alert_email": "team@example.com",
  "alert_slack_webhook": "https://hooks.slack.com/..."
}
```

---

## 📊 Features

### 1. Automated Benchmarking

**Multi-Language Support**:
- Python, JavaScript, Java, C++, C, Go, Rust
- Ruby, TypeScript, Swift, Kotlin
- Fortran, COBOL (legacy)

**Benchmark Metrics**:
- Execution time (avg, median, min, max, stdev)
- Memory usage (average, peak)
- CPU utilization
- Multiple input sizes
- Configurable iterations

**Example**:
```python
# Run 100 iterations across 4 input sizes
benchmark_runner.run_single_benchmark('quicksort', 'python')
```

### 2. Statistical Analysis

**Analyses Performed**:
- **Descriptive Statistics**: Mean, median, mode, stdev, variance
- **Distribution Analysis**: Normality tests, skewness, kurtosis
- **Outlier Detection**: IQR method, z-score method
- **Confidence Intervals**: 95% confidence by default
- **Comparative Analysis**: Language comparisons, speedup factors

**Example Output**:
```json
{
  "mean": 12.5,
  "median": 12.3,
  "stdev": 0.8,
  "confidence_interval": [12.1, 12.9],
  "is_normal_distribution": true
}
```

### 3. Trend Detection

**Capabilities**:
- Historical trend analysis
- Performance regression detection
- Improvement tracking
- Anomaly detection

**Regression Detection**:
- Compares against historical baseline
- Configurable threshold (default: 10%)
- Automatic alerts on regression

**Example**:
```json
{
  "algorithm": "quicksort",
  "language": "python",
  "regression_percent": 15.2,
  "status": "REGRESSION",
  "baseline": 10.5,
  "current": 12.1
}
```

### 4. Memory Profiling

**Metrics**:
- Heap memory usage
- Peak memory consumption
- Memory allocation patterns
- Garbage collection impact (for managed languages)

**Tools Used**:
- `memory_profiler` (Python)
- `valgrind` (C/C++)
- Built-in profilers for other languages

### 5. Scalability Analysis

**Analysis Types**:
- Time complexity fitting (O(1), O(log n), O(n), O(n log n), O(n²))
- R² goodness of fit
- Extrapolation for larger inputs
- Bottleneck identification

**Example**:
```json
{
  "best_fit_complexity": "O(n log n)",
  "r_squared": 0.998,
  "formula": "0.00015 * n * log(n) + 0.5"
}
```

### 6. Interactive HTML Dashboard

**Features**:
- **Overview**: Summary statistics, fastest/slowest algorithms
- **Charts**: Interactive Plotly charts (bar, line, scatter, heatmap)
- **Comparisons**: Side-by-side language comparisons
- **Trends**: Historical performance trends
- **Details**: Drill-down into specific benchmarks

**Charts Included**:
- Performance comparison bar charts
- Execution time distributions (histograms)
- Scalability curves (line charts)
- Language heatmaps
- Trend timeseries

### 7. PDF Reports

**Sections**:
1. Executive Summary
2. Benchmark Results
3. Statistical Analysis
4. Performance Trends
5. Recommendations
6. Appendix (raw data)

**Features**:
- Professional formatting
- Embedded charts
- Table of contents
- Page numbering

### 8. Markdown Summaries

**Perfect for**:
- GitHub README updates
- Pull request comments
- Documentation integration

**Example Output**:
```markdown
## Performance Report - 2024-01-15

### Summary
- **Total Benchmarks**: 120
- **Languages Tested**: 6
- **Fastest Overall**: QuickSort (Rust) - 2.1ms
- **Regressions Detected**: 2

### Top Performers
1. Rust: 2.1ms (baseline)
2. C++: 2.3ms (1.1x slower)
3. Go: 3.5ms (1.7x slower)

### Regressions
⚠️ BubbleSort (Python): 15% slower than baseline
```

### 9. JSON Data Export

**Use Cases**:
- Custom analysis scripts
- Data warehousing
- Integration with other tools
- Long-term archival

**Structure**:
```json
{
  "run_id": "20240115_143022",
  "timestamp": "2024-01-15T14:30:22",
  "benchmarks": { ... },
  "statistics": { ... },
  "trends": { ... }
}
```

### 10. Alert System

**Alert Types**:
- Performance regressions
- Benchmark failures
- Anomalies detected
- Significant improvements

**Notification Channels**:
- Email (SMTP)
- Slack webhooks
- Custom webhooks
- Log files

**Example Alert**:
```
🚨 Performance Regression Detected

Algorithm: QuickSort (Python)
Regression: 15.2% slower
Baseline: 10.5ms
Current: 12.1ms

Run ID: 20240115_143022
View Report: https://reports.example.com/20240115_143022
```

---

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Performance Benchmarks

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  benchmark:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r reports/requirements.txt

      - name: Run benchmarks
        run: |
          python reports/generator.py

      - name: Upload reports
        uses: actions/upload-artifact@v2
        with:
          name: performance-reports
          path: reports/output/latest/

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v5
        with:
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('reports/output/latest/summary.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.name,
              body: summary
            });
```

### GitLab CI

```yaml
performance:
  stage: test
  script:
    - pip install -r reports/requirements.txt
    - python reports/generator.py
  artifacts:
    paths:
      - reports/output/latest/
    expire_in: 30 days
  only:
    - main
    - merge_requests
```

---

## 📈 Usage Examples

### Example 1: Full Analysis

```bash
python reports/generator.py

# Output:
# [Phase 1/6] Executing Benchmarks
# [Phase 2/6] Performing Statistical Analysis
# [Phase 3/6] Detecting Performance Trends
# [Phase 4/6] Profiling Memory Usage
# [Phase 5/6] Generating Recommendations
# [Phase 6/6] Storing Results in Database
#
# Reports generated in: reports/output/20240115_143022/
```

### Example 2: Compare Sorting Algorithms

```bash
python reports/generator.py \
  --mode compare \
  --algorithm quicksort \
  --languages python java cpp rust

# Output: JSON comparison data
```

### Example 3: Analyze Scalability

```bash
python reports/generator.py \
  --mode scalability \
  --algorithm mergesort \
  --language python

# Tests with input sizes: 10, 100, 1000, 10000
# Fits to O(n log n), O(n²), etc.
```

### Example 4: Custom Categories

```bash
python reports/generator.py \
  --categories sorting searching \
  --output ./custom_reports/
```

### Example 5: Scheduled Monitoring

```bash
# Add to crontab for daily monitoring
0 0 * * * cd /path/to/repo && python reports/generator.py
```

---

## 🎯 Recommendation Engine

The system provides intelligent recommendations based on:
- Performance characteristics
- Memory usage
- Input size expectations
- Language constraints

**Example Recommendation**:
```
For sorting 1M elements:
✓ RECOMMENDED: Merge Sort (Rust)
  - Consistent O(n log n) performance
  - Low memory overhead
  - Stable sorting

⚠️ AVOID: Bubble Sort
  - O(n²) complexity
  - 100x slower for large inputs
```

---

## 🔧 Advanced Usage

### Custom Benchmark Script

```python
from reports.generator import PerformanceReportGenerator

# Initialize
generator = PerformanceReportGenerator()

# Run specific analysis
results = generator.run_quick_benchmark('quicksort', 'python')

# Generate reports
generator.generate_reports(results)

# Query database
historical = generator.db.get_historical_data('quicksort', 'python', limit=30)
```

### Custom Configuration

```python
config = {
    'benchmark_iterations': 1000,  # More iterations
    'input_sizes': [100, 1000, 10000, 100000],  # Custom sizes
    'regression_threshold': 0.05,  # 5% threshold
}

generator = PerformanceReportGenerator(config)
```

---

## 📊 Database Schema

```sql
-- Runs table
CREATE TABLE runs (
    run_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    config TEXT,
    status TEXT DEFAULT 'completed'
);

-- Benchmarks table
CREATE TABLE benchmarks (
    id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL,
    category TEXT,
    algorithm TEXT,
    language TEXT,
    avg_time_ms REAL,
    median_time_ms REAL,
    stdev_time_ms REAL,
    iterations INTEGER,
    input_size INTEGER,
    raw_data TEXT
);

-- Trends table
CREATE TABLE trends (
    id INTEGER PRIMARY KEY,
    algorithm TEXT,
    language TEXT,
    trend_type TEXT,
    regression_percent REAL,
    detected_at TEXT
);
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Missing dependencies**
   ```bash
   pip install -r reports/requirements.txt
   ```

2. **Benchmark timeout**
   - Increase timeout in config
   - Reduce input sizes

3. **Memory profiling fails**
   - Ensure profiling tools installed
   - Disable with `memory_profiling_enabled: false`

4. **Database locked**
   - Close other connections
   - Check file permissions

---

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding new language support
- Implementing custom analyzers
- Creating new report formats
- Improving visualizations

---

## 📄 License

MIT License - See [LICENSE](../LICENSE)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/algorithms-multiverse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/algorithms-multiverse/discussions)
- **Documentation**: [Main README](../README.md)

---

**[⬆ Back to Main README](../README.md)**
