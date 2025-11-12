"""
Documentation Generator for Algorithms Multiverse

Generates:
- Algorithm complexity cheat sheets
- Cross-language implementation comparisons
- API reference documentation
- Performance analysis reports

Outputs: Markdown and HTML formats

@author Algorithms Multiverse Documentation System
@version 1.0
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict
import sys

# Import code parser
sys.path.insert(0, str(Path(__file__).parent))
from code_parser import AlgorithmMetadata, Complexity, FunctionInfo


class DocumentationGenerator:
    """Generates comprehensive documentation from algorithm metadata"""

    def __init__(self, metadata_file: str = None, output_dir: str = 'docs/output'):
        """Initialize generator with metadata"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.metadata = []
        if metadata_file and Path(metadata_file).exists():
            self.load_metadata(metadata_file)

    def load_metadata(self, metadata_file: str):
        """Load metadata from JSON file"""
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert dicts back to AlgorithmMetadata objects
        for item in data:
            # Convert complexity dicts back to Complexity objects
            time_complexities = []
            for c in item.get('time_complexity', []):
                from code_parser import ComplexityType
                time_complexities.append(Complexity(
                    type=ComplexityType(c['type']),
                    notation=c['notation'],
                    case=c.get('case'),
                    description=c.get('description')
                ))

            space_complexities = []
            for c in item.get('space_complexity', []):
                from code_parser import ComplexityType
                space_complexities.append(Complexity(
                    type=ComplexityType(c['type']),
                    notation=c['notation'],
                    case=c.get('case'),
                    description=c.get('description')
                ))

            # Convert function dicts
            functions = []
            for f in item.get('functions', []):
                functions.append(FunctionInfo(**f))

            metadata = AlgorithmMetadata(
                name=item['name'],
                category=item['category'],
                language=item['language'],
                file_path=item['file_path'],
                description=item.get('description'),
                time_complexity=time_complexities,
                space_complexity=space_complexities,
                functions=functions,
                examples=item.get('examples', []),
                features=item.get('features', []),
                use_cases=item.get('use_cases', []),
                references=item.get('references', [])
            )
            self.metadata.append(metadata)

        print(f"Loaded {len(self.metadata)} algorithm metadata entries")

    def generate_complexity_cheatsheet(self) -> str:
        """Generate comprehensive complexity cheat sheet"""
        output = []

        output.append("# Algorithm Complexity Cheat Sheet\n")
        output.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        output.append("Quick reference guide for algorithm time and space complexities.\n\n")

        # Group by category
        by_category = defaultdict(list)
        for meta in self.metadata:
            by_category[meta.category].append(meta)

        output.append("## Table of Contents\n\n")
        for category in sorted(by_category.keys()):
            output.append(f"- [{category.replace('-', ' ').title()}](#{category.replace(' ', '-').lower()})\n")

        output.append("\n---\n\n")

        # Generate sections by category
        for category in sorted(by_category.keys()):
            output.append(f"## {category.replace('-', ' ').title()}\n\n")

            # Create comparison table
            output.append("| Algorithm | Time Complexity | Space Complexity | Languages |\n")
            output.append("|-----------|----------------|------------------|------------|\n")

            # Group by algorithm name
            algo_groups = defaultdict(list)
            for meta in by_category[category]:
                algo_groups[meta.name].append(meta)

            for algo_name in sorted(algo_groups.keys()):
                implementations = algo_groups[algo_name]

                # Get best complexity representation
                time_comp = "N/A"
                space_comp = "N/A"

                # Use first implementation's complexity
                if implementations:
                    meta = implementations[0]
                    if meta.time_complexity:
                        time_notations = []
                        for tc in meta.time_complexity:
                            if tc.case:
                                time_notations.append(f"{tc.notation} ({tc.case})")
                            else:
                                time_notations.append(tc.notation)
                        time_comp = "<br>".join(time_notations) if time_notations else "N/A"

                    if meta.space_complexity:
                        space_comp = ", ".join(sc.notation for sc in meta.space_complexity)

                languages = ", ".join(sorted(set(impl.language for impl in implementations)))

                output.append(f"| {algo_name} | {time_comp} | {space_comp} | {languages} |\n")

            output.append("\n")

        # Add complexity notation guide
        output.append("\n---\n\n")
        output.append("## Complexity Notation Guide\n\n")
        output.append("| Notation | Name | Description | Example |\n")
        output.append("|----------|------|-------------|----------|\n")
        output.append("| O(1) | Constant | Does not depend on input size | Array access |\n")
        output.append("| O(log n) | Logarithmic | Divides problem in half | Binary search |\n")
        output.append("| O(n) | Linear | Proportional to input size | Linear search |\n")
        output.append("| O(n log n) | Linearithmic | Efficient sorting algorithms | Merge sort |\n")
        output.append("| O(n²) | Quadratic | Nested loops | Bubble sort |\n")
        output.append("| O(n³) | Cubic | Triple nested loops | Matrix multiplication |\n")
        output.append("| O(2ⁿ) | Exponential | Doubles with each input | Fibonacci (naive) |\n")
        output.append("| O(n!) | Factorial | All permutations | Traveling salesman |\n\n")

        return ''.join(output)

    def generate_comparison_guide(self) -> str:
        """Generate cross-language implementation comparison"""
        output = []

        output.append("# Cross-Language Implementation Comparison\n\n")
        output.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        output.append("Compare algorithm implementations across different programming languages.\n\n")

        # Group by algorithm name
        algo_groups = defaultdict(list)
        for meta in self.metadata:
            algo_groups[meta.name].append(meta)

        # Filter to algorithms with multiple language implementations
        multi_lang = {name: impls for name, impls in algo_groups.items() if len(impls) > 1}

        output.append(f"Found {len(multi_lang)} algorithms with multiple language implementations.\n\n")
        output.append("---\n\n")

        for algo_name in sorted(multi_lang.keys()):
            implementations = multi_lang[algo_name]

            output.append(f"## {algo_name}\n\n")

            # Category and description (from first impl)
            first = implementations[0]
            output.append(f"**Category:** {first.category.replace('-', ' ').title()}\n\n")

            if first.description:
                desc_lines = first.description.split('\n')[:3]  # First 3 lines
                output.append(f"**Description:** {' '.join(desc_lines)}\n\n")

            # Comparison table
            output.append("### Implementation Comparison\n\n")
            output.append("| Language | Time Complexity | Space Complexity | Functions | Features |\n")
            output.append("|----------|----------------|------------------|-----------|----------|\n")

            for impl in sorted(implementations, key=lambda x: x.language):
                time_comp = ", ".join(tc.notation for tc in impl.time_complexity) if impl.time_complexity else "N/A"
                space_comp = ", ".join(sc.notation for sc in impl.space_complexity) if impl.space_complexity else "N/A"
                func_count = len(impl.functions)
                features = "<br>".join(impl.features[:3]) if impl.features else "-"

                output.append(f"| {impl.language.title()} | {time_comp} | {space_comp} | {func_count} | {features} |\n")

            output.append("\n")

            # Key functions comparison
            output.append("### Key Functions\n\n")

            # Get common function names
            all_func_names = set()
            for impl in implementations:
                all_func_names.update(f.name for f in impl.functions[:5])  # Top 5 functions

            for func_name in sorted(all_func_names):
                output.append(f"**`{func_name}`**\n\n")

                for impl in implementations:
                    matching_funcs = [f for f in impl.functions if f.name == func_name]
                    if matching_funcs:
                        func = matching_funcs[0]
                        output.append(f"- **{impl.language.title()}**: `{func.signature}`")
                        if func.time_complexity:
                            output.append(f" - {func.time_complexity}")
                        output.append("\n")

                output.append("\n")

            # File locations
            output.append("### File Locations\n\n")
            for impl in implementations:
                output.append(f"- **{impl.language.title()}**: `{impl.file_path}`\n")

            output.append("\n---\n\n")

        return ''.join(output)

    def generate_api_reference(self) -> Dict[str, str]:
        """Generate API reference documentation for each language"""
        references = {}

        # Group by language
        by_language = defaultdict(list)
        for meta in self.metadata:
            by_language[meta.language].append(meta)

        for language, implementations in by_language.items():
            output = []

            output.append(f"# {language.title()} API Reference\n\n")
            output.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            output.append(f"Complete API reference for {language.title()} algorithm implementations.\n\n")

            # Group by category
            by_category = defaultdict(list)
            for impl in implementations:
                by_category[impl.category].append(impl)

            output.append("## Table of Contents\n\n")
            for category in sorted(by_category.keys()):
                output.append(f"- [{category.replace('-', ' ').title()}](#{category.replace(' ', '-').lower()})\n")
            output.append("\n---\n\n")

            # Generate sections
            for category in sorted(by_category.keys()):
                output.append(f"## {category.replace('-', ' ').title()}\n\n")

                for impl in sorted(by_category[category], key=lambda x: x.name):
                    output.append(f"### {impl.name}\n\n")

                    if impl.description:
                        output.append(f"{impl.description}\n\n")

                    # Complexity
                    if impl.time_complexity or impl.space_complexity:
                        output.append("**Complexity:**\n\n")
                        if impl.time_complexity:
                            for tc in impl.time_complexity:
                                case_str = f" ({tc.case})" if tc.case else ""
                                output.append(f"- Time: {tc.notation}{case_str}\n")
                        if impl.space_complexity:
                            for sc in impl.space_complexity:
                                output.append(f"- Space: {sc.notation}\n")
                        output.append("\n")

                    # Features
                    if impl.features:
                        output.append("**Language Features:**\n\n")
                        for feature in impl.features:
                            output.append(f"- {feature}\n")
                        output.append("\n")

                    # Functions
                    if impl.functions:
                        output.append("**Functions:**\n\n")
                        for func in impl.functions[:10]:  # Limit to 10 functions
                            output.append(f"#### `{func.name}`\n\n")
                            output.append(f"```{language}\n{func.signature}\n```\n\n")

                            if func.docstring:
                                # Limit docstring length
                                doc_lines = func.docstring.split('\n')[:5]
                                output.append(f"{' '.join(doc_lines)}\n\n")

                            if func.time_complexity or func.space_complexity:
                                complexity_parts = []
                                if func.time_complexity:
                                    complexity_parts.append(f"Time: {func.time_complexity}")
                                if func.space_complexity:
                                    complexity_parts.append(f"Space: {func.space_complexity}")
                                output.append(f"*Complexity: {', '.join(complexity_parts)}*\n\n")

                    # Examples
                    if impl.examples:
                        output.append("**Examples:**\n\n")
                        for i, example in enumerate(impl.examples[:3], 1):  # Limit to 3 examples
                            output.append(f"```{language}\n{example}\n```\n\n")

                    # File location
                    output.append(f"**File:** `{impl.file_path}`\n\n")
                    output.append("---\n\n")

            references[language] = ''.join(output)

        return references

    def generate_performance_report(self, benchmark_data: Dict = None) -> str:
        """Generate performance analysis report"""
        output = []

        output.append("# Performance Analysis Report\n\n")
        output.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        output.append("Comprehensive performance analysis across implementations.\n\n")

        # Group by algorithm
        algo_groups = defaultdict(list)
        for meta in self.metadata:
            algo_groups[meta.name].append(meta)

        # Filter to algorithms with multiple implementations
        multi_impl = {name: impls for name, impls in algo_groups.items() if len(impls) > 1}

        output.append("## Theoretical Complexity Comparison\n\n")

        for algo_name in sorted(multi_impl.keys()):
            implementations = multi_impl[algo_name]

            output.append(f"### {algo_name}\n\n")

            output.append("| Language | Time Complexity | Space Complexity | Notes |\n")
            output.append("|----------|----------------|------------------|--------|\n")

            for impl in sorted(implementations, key=lambda x: x.language):
                time_comp = ", ".join(tc.notation for tc in impl.time_complexity) if impl.time_complexity else "N/A"
                space_comp = ", ".join(sc.notation for sc in impl.space_complexity) if impl.space_complexity else "N/A"

                notes = ""
                if impl.features:
                    notes = impl.features[0][:50] + "..." if len(impl.features[0]) > 50 else impl.features[0]

                output.append(f"| {impl.language.title()} | {time_comp} | {space_comp} | {notes} |\n")

            output.append("\n")

        # Benchmark data section (if provided)
        if benchmark_data:
            output.append("\n## Benchmark Results\n\n")
            output.append("*Integration with benchmark framework*\n\n")
            # TODO: Integrate with actual benchmark data
            output.append("Run benchmarks using the framework in `benchmarks/` directory.\n\n")

        # Recommendations
        output.append("\n## Performance Recommendations\n\n")
        output.append("### By Use Case\n\n")
        output.append("- **Small datasets (n < 100)**: Simple algorithms often outperform complex ones\n")
        output.append("- **Large datasets (n > 10,000)**: Use O(n log n) or better algorithms\n")
        output.append("- **Memory-constrained**: Prefer in-place algorithms with O(1) space\n")
        output.append("- **Real-time systems**: Use algorithms with predictable worst-case performance\n\n")

        output.append("### Language Selection\n\n")
        output.append("- **Python**: Rapid development, clear syntax, good for prototyping\n")
        output.append("- **C/C++**: Maximum performance, low-level control\n")
        output.append("- **Rust**: Performance with memory safety guarantees\n")
        output.append("- **Go**: Good balance of performance and simplicity\n")
        output.append("- **JavaScript**: Web applications, Node.js backend\n")
        output.append("- **Java**: Enterprise applications, JVM ecosystem\n\n")

        return ''.join(output)

    def generate_all_documentation(self):
        """Generate all documentation outputs"""
        print("Generating documentation...")

        # 1. Complexity cheat sheet
        print("  - Generating complexity cheat sheet...")
        cheatsheet = self.generate_complexity_cheatsheet()
        cheatsheet_path = self.output_dir / 'cheatsheets' / 'complexity_cheatsheet.md'
        cheatsheet_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cheatsheet_path, 'w', encoding='utf-8') as f:
            f.write(cheatsheet)
        print(f"    ✓ Saved to {cheatsheet_path}")

        # 2. Comparison guide
        print("  - Generating comparison guide...")
        comparison = self.generate_comparison_guide()
        comparison_path = self.output_dir / 'comparisons' / 'implementation_comparison.md'
        comparison_path.parent.mkdir(parents=True, exist_ok=True)
        with open(comparison_path, 'w', encoding='utf-8') as f:
            f.write(comparison)
        print(f"    ✓ Saved to {comparison_path}")

        # 3. API references
        print("  - Generating API references...")
        references = self.generate_api_reference()
        for language, content in references.items():
            api_path = self.output_dir / 'api' / f'{language}_api.md'
            api_path.parent.mkdir(parents=True, exist_ok=True)
            with open(api_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"    ✓ Saved {language} API to {api_path}")

        # 4. Performance report
        print("  - Generating performance report...")
        performance = self.generate_performance_report()
        perf_path = self.output_dir / 'performance_report.md'
        with open(perf_path, 'w', encoding='utf-8') as f:
            f.write(performance)
        print(f"    ✓ Saved to {perf_path}")

        print(f"\n✓ All documentation generated in {self.output_dir}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate algorithm documentation')
    parser.add_argument('--metadata', default='docs/output/metadata.json',
                       help='Metadata JSON file')
    parser.add_argument('--output', default='docs/output',
                       help='Output directory')
    parser.add_argument('--cheatsheet-only', action='store_true',
                       help='Generate only complexity cheat sheet')
    parser.add_argument('--comparison-only', action='store_true',
                       help='Generate only comparison guide')
    parser.add_argument('--api-only', action='store_true',
                       help='Generate only API references')

    args = parser.parse_args()

    generator = DocumentationGenerator(
        metadata_file=args.metadata,
        output_dir=args.output
    )

    if args.cheatsheet_only:
        cheatsheet = generator.generate_complexity_cheatsheet()
        print(cheatsheet)
    elif args.comparison_only:
        comparison = generator.generate_comparison_guide()
        print(comparison)
    elif args.api_only:
        references = generator.generate_api_reference()
        for lang, content in references.items():
            print(f"\n{'='*50}\n{lang.upper()}\n{'='*50}\n")
            print(content[:500] + "...\n")
    else:
        generator.generate_all_documentation()


if __name__ == '__main__':
    main()
