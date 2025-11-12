"""
Tutorial and Learning Path Generator

Creates:
- Beginner to advanced learning paths
- Step-by-step tutorials
- Interactive exercises
- Difficulty-based curriculum

@author Algorithms Multiverse Documentation System
@version 1.0
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent))
from code_parser import AlgorithmMetadata


class TutorialGenerator:
    """Generates learning paths and tutorials"""

    # Complexity difficulty mapping
    COMPLEXITY_DIFFICULTY = {
        'O(1)': 1,
        'O(log n)': 2,
        'O(n)': 2,
        'O(n log n)': 3,
        'O(n²)': 3,
        'O(n³)': 4,
        'O(2ⁿ)': 5,
        'O(n!)': 5,
    }

    # Category difficulty
    CATEGORY_DIFFICULTY = {
        'data-structures': 2,
        'sorting': 2,
        'searching': 2,
        'string-algorithms': 3,
        'graph-algorithms': 4,
        'dynamic-programming': 5,
        'mathematical': 3,
        'computational-geometry': 4,
    }

    def __init__(self, metadata: List[AlgorithmMetadata]):
        """Initialize with algorithm metadata"""
        self.metadata = metadata

    def assess_difficulty(self, algo: AlgorithmMetadata) -> int:
        """Assess algorithm difficulty (1-5)"""
        scores = []

        # Based on time complexity
        if algo.time_complexity:
            for tc in algo.time_complexity:
                for pattern, score in self.COMPLEXITY_DIFFICULTY.items():
                    if pattern in tc.notation:
                        scores.append(score)
                        break

        # Based on category
        if algo.category in self.CATEGORY_DIFFICULTY:
            scores.append(self.CATEGORY_DIFFICULTY[algo.category])

        # Based on function count (more functions = more complex)
        if algo.functions:
            func_score = min(5, 1 + len(algo.functions) // 3)
            scores.append(func_score)

        # Return average score
        return round(sum(scores) / len(scores)) if scores else 3

    def generate_learning_paths(self) -> Dict[str, List[AlgorithmMetadata]]:
        """Generate learning paths by difficulty"""
        paths = {
            'beginner': [],      # Difficulty 1-2
            'intermediate': [],  # Difficulty 3
            'advanced': [],      # Difficulty 4-5
        }

        for algo in self.metadata:
            difficulty = self.assess_difficulty(algo)

            if difficulty <= 2:
                paths['beginner'].append(algo)
            elif difficulty == 3:
                paths['intermediate'].append(algo)
            else:
                paths['advanced'].append(algo)

        return paths

    def generate_learning_path_doc(self) -> str:
        """Generate learning path documentation"""
        output = []

        output.append("# Algorithm Learning Paths\n\n")
        output.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        output.append("Structured learning paths from beginner to advanced levels.\n\n")

        paths = self.generate_learning_paths()

        # Overview
        output.append("## Overview\n\n")
        output.append(f"- **Beginner Path**: {len(paths['beginner'])} algorithms\n")
        output.append(f"- **Intermediate Path**: {len(paths['intermediate'])} algorithms\n")
        output.append(f"- **Advanced Path**: {len(paths['advanced'])} algorithms\n\n")

        output.append("---\n\n")

        # Beginner Path
        output.append("## 🌱 Beginner Path\n\n")
        output.append("**Prerequisites:** Basic programming knowledge\n\n")
        output.append("**Goal:** Master fundamental algorithms and data structures\n\n")

        output.append("### Recommended Order\n\n")

        # Group by category
        beginner_by_cat = defaultdict(list)
        for algo in paths['beginner']:
            beginner_by_cat[algo.category].append(algo)

        step = 1
        # Recommended order: data structures -> sorting -> searching
        priority_order = ['data-structures', 'sorting', 'searching']

        for category in priority_order:
            if category in beginner_by_cat:
                output.append(f"#### {step}. {category.replace('-', ' ').title()}\n\n")
                for algo in beginner_by_cat[category]:
                    time_comp = algo.time_complexity[0].notation if algo.time_complexity else "N/A"
                    output.append(f"- **{algo.name}** ({algo.language})\n")
                    output.append(f"  - Complexity: {time_comp}\n")
                    output.append(f"  - File: `{algo.file_path}`\n")
                    if algo.description:
                        desc = algo.description.split('\n')[0][:100]
                        output.append(f"  - *{desc}...*\n")
                    output.append("\n")
                step += 1

        # Other categories
        for category in sorted(beginner_by_cat.keys()):
            if category not in priority_order:
                output.append(f"#### {step}. {category.replace('-', ' ').title()}\n\n")
                for algo in beginner_by_cat[category]:
                    output.append(f"- **{algo.name}** ({algo.language}) - `{algo.file_path}`\n")
                step += 1

        output.append("\n---\n\n")

        # Intermediate Path
        output.append("## 🚀 Intermediate Path\n\n")
        output.append("**Prerequisites:** Completed beginner path or equivalent\n\n")
        output.append("**Goal:** Master efficient algorithms and advanced data structures\n\n")

        output.append("### Recommended Topics\n\n")

        inter_by_cat = defaultdict(list)
        for algo in paths['intermediate']:
            inter_by_cat[algo.category].append(algo)

        for category in sorted(inter_by_cat.keys()):
            output.append(f"#### {category.replace('-', ' ').title()}\n\n")
            for algo in inter_by_cat[category][:10]:  # Limit to 10 per category
                time_comp = algo.time_complexity[0].notation if algo.time_complexity else "N/A"
                output.append(f"- **{algo.name}** - {time_comp} - [{algo.language}]({algo.file_path})\n")
            output.append("\n")

        output.append("\n---\n\n")

        # Advanced Path
        output.append("## 🎓 Advanced Path\n\n")
        output.append("**Prerequisites:** Strong foundation in algorithms and data structures\n\n")
        output.append("**Goal:** Master complex algorithms and optimization techniques\n\n")

        output.append("### Advanced Topics\n\n")

        adv_by_cat = defaultdict(list)
        for algo in paths['advanced']:
            adv_by_cat[algo.category].append(algo)

        for category in sorted(adv_by_cat.keys()):
            output.append(f"#### {category.replace('-', ' ').title()}\n\n")
            for algo in adv_by_cat[category][:10]:
                time_comp = algo.time_complexity[0].notation if algo.time_complexity else "N/A"
                output.append(f"- **{algo.name}** - {time_comp} - [{algo.language}]({algo.file_path})\n")
            output.append("\n")

        # Study tips
        output.append("\n---\n\n")
        output.append("## 📚 Study Tips\n\n")
        output.append("### Beginner\n")
        output.append("1. Understand the problem before coding\n")
        output.append("2. Implement in your preferred language first\n")
        output.append("3. Analyze time and space complexity\n")
        output.append("4. Test with small examples\n")
        output.append("5. Compare with other implementations\n\n")

        output.append("### Intermediate\n")
        output.append("1. Focus on optimization techniques\n")
        output.append("2. Understand trade-offs between time and space\n")
        output.append("3. Practice implementing in multiple languages\n")
        output.append("4. Benchmark your implementations\n")
        output.append("5. Study real-world applications\n\n")

        output.append("### Advanced\n")
        output.append("1. Master dynamic programming patterns\n")
        output.append("2. Understand graph algorithm optimizations\n")
        output.append("3. Learn advanced data structures (segment trees, etc.)\n")
        output.append("4. Study competitive programming problems\n")
        output.append("5. Contribute to open source projects\n\n")

        return ''.join(output)

    def generate_algorithm_tutorial(self, algo: AlgorithmMetadata) -> str:
        """Generate detailed tutorial for a specific algorithm"""
        output = []

        output.append(f"# {algo.name} Tutorial\n\n")
        output.append(f"*{algo.language.title()} Implementation*\n\n")

        # Difficulty badge
        difficulty = self.assess_difficulty(algo)
        diff_emoji = ['🌱', '🌱', '🚀', '🚀', '🎓', '🎓'][min(difficulty, 5)]
        diff_label = ['Beginner', 'Beginner', 'Intermediate', 'Intermediate', 'Advanced', 'Advanced'][min(difficulty, 5)]
        output.append(f"{diff_emoji} **Difficulty:** {diff_label}\n\n")

        output.append("---\n\n")

        # Overview
        output.append("## Overview\n\n")
        if algo.description:
            output.append(f"{algo.description}\n\n")

        # Complexity
        if algo.time_complexity or algo.space_complexity:
            output.append("### Complexity\n\n")
            if algo.time_complexity:
                for tc in algo.time_complexity:
                    case_str = f" ({tc.case})" if tc.case else ""
                    output.append(f"- **Time:** {tc.notation}{case_str}\n")
            if algo.space_complexity:
                for sc in algo.space_complexity:
                    output.append(f"- **Space:** {sc.notation}\n")
            output.append("\n")

        # When to use
        output.append("### When to Use\n\n")
        output.append("This algorithm is best suited for:\n\n")
        if algo.use_cases:
            for use_case in algo.use_cases:
                output.append(f"- {use_case}\n")
        else:
            # Generate generic use cases based on complexity
            output.append(f"- Problems in the {algo.category.replace('-', ' ')} category\n")
            if algo.time_complexity:
                tc = algo.time_complexity[0].notation
                if 'O(1)' in tc:
                    output.append("- When constant-time operations are required\n")
                elif 'O(log n)' in tc:
                    output.append("- Large datasets where logarithmic performance is acceptable\n")
                elif 'O(n)' in tc:
                    output.append("- Linear scans through data\n")
                elif 'O(n log n)' in tc:
                    output.append("- Efficient sorting and divide-and-conquer problems\n")
        output.append("\n")

        # Implementation details
        output.append("## Implementation\n\n")

        if algo.features:
            output.append("### Key Features\n\n")
            for feature in algo.features:
                output.append(f"- {feature}\n")
            output.append("\n")

        # Functions
        if algo.functions:
            output.append("### Core Functions\n\n")
            for func in algo.functions[:5]:  # Top 5 functions
                output.append(f"#### `{func.name}`\n\n")

                output.append(f"```{algo.language}\n{func.signature}\n```\n\n")

                if func.docstring:
                    output.append(f"{func.docstring}\n\n")

                if func.time_complexity or func.space_complexity:
                    parts = []
                    if func.time_complexity:
                        parts.append(f"Time: {func.time_complexity}")
                    if func.space_complexity:
                        parts.append(f"Space: {func.space_complexity}")
                    output.append(f"**Complexity:** {', '.join(parts)}\n\n")

        # Examples
        if algo.examples:
            output.append("## Examples\n\n")
            for i, example in enumerate(algo.examples[:3], 1):
                output.append(f"### Example {i}\n\n")
                output.append(f"```{algo.language}\n{example}\n```\n\n")

        # Practice exercises
        output.append("## Practice Exercises\n\n")
        output.append("Try these exercises to master this algorithm:\n\n")
        output.append(f"1. Implement a variation that handles edge cases\n")
        output.append(f"2. Optimize the space complexity\n")
        output.append(f"3. Add error handling and input validation\n")
        output.append(f"4. Benchmark against alternative approaches\n")
        output.append(f"5. Port the implementation to another language\n\n")

        # Further reading
        output.append("## Further Reading\n\n")
        output.append(f"- [Source Code]({algo.file_path})\n")
        output.append(f"- Related algorithms in {algo.category}\n")
        if algo.references:
            for ref in algo.references:
                output.append(f"- {ref}\n")
        output.append("\n")

        return ''.join(output)

    def generate_quick_reference(self) -> str:
        """Generate quick reference card"""
        output = []

        output.append("# Algorithm Quick Reference Card\n\n")
        output.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

        # Group by category
        by_category = defaultdict(list)
        for algo in self.metadata:
            by_category[algo.category].append(algo)

        for category in sorted(by_category.keys()):
            output.append(f"## {category.replace('-', ' ').title()}\n\n")

            # Get unique algorithm names
            algo_names = {}
            for algo in by_category[category]:
                if algo.name not in algo_names:
                    algo_names[algo.name] = algo

            for name, algo in sorted(algo_names.items()):
                difficulty = self.assess_difficulty(algo)
                diff_stars = '⭐' * min(difficulty, 5)

                time_comp = algo.time_complexity[0].notation if algo.time_complexity else "N/A"

                output.append(f"**{name}** {diff_stars}\n")
                output.append(f"- Complexity: {time_comp}\n")
                output.append(f"- Category: {algo.category}\n")

                # Count implementations
                impl_count = len([a for a in self.metadata if a.name == name])
                if impl_count > 1:
                    languages = [a.language for a in self.metadata if a.name == name]
                    output.append(f"- Languages: {', '.join(set(languages))}\n")

                output.append("\n")

        return ''.join(output)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate learning paths and tutorials')
    parser.add_argument('--metadata', default='docs/output/metadata.json',
                       help='Metadata JSON file')
    parser.add_argument('--output', default='docs/output/tutorials',
                       help='Output directory')
    parser.add_argument('--algorithm', help='Generate tutorial for specific algorithm')

    args = parser.parse_args()

    # Load metadata
    with open(args.metadata, 'r', encoding='utf-8') as f:
        data = json.load(f)

    metadata = []
    for item in data:
        from code_parser import Complexity, ComplexityType, FunctionInfo

        # Convert complexity dicts
        time_complexities = [
            Complexity(
                type=ComplexityType(c['type']),
                notation=c['notation'],
                case=c.get('case'),
                description=c.get('description')
            )
            for c in item.get('time_complexity', [])
        ]

        space_complexities = [
            Complexity(
                type=ComplexityType(c['type']),
                notation=c['notation'],
                case=c.get('case'),
                description=c.get('description')
            )
            for c in item.get('space_complexity', [])
        ]

        functions = [FunctionInfo(**f) for f in item.get('functions', [])]

        metadata.append(AlgorithmMetadata(
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
        ))

    generator = TutorialGenerator(metadata)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.algorithm:
        # Generate tutorial for specific algorithm
        matching = [m for m in metadata if m.name.lower() == args.algorithm.lower()]
        if matching:
            tutorial = generator.generate_algorithm_tutorial(matching[0])
            print(tutorial)
        else:
            print(f"Algorithm '{args.algorithm}' not found")
    else:
        # Generate all learning materials
        print("Generating learning materials...")

        # Learning paths
        learning_path = generator.generate_learning_path_doc()
        path_file = output_dir / 'learning_paths.md'
        with open(path_file, 'w', encoding='utf-8') as f:
            f.write(learning_path)
        print(f"✓ Learning paths: {path_file}")

        # Quick reference
        quick_ref = generator.generate_quick_reference()
        ref_file = output_dir / 'quick_reference.md'
        with open(ref_file, 'w', encoding='utf-8') as f:
            f.write(quick_ref)
        print(f"✓ Quick reference: {ref_file}")

        # Generate sample tutorials
        sample_algos = metadata[:5]  # First 5 algorithms
        for algo in sample_algos:
            tutorial = generator.generate_algorithm_tutorial(algo)
            safe_name = algo.name.lower().replace(' ', '_')
            tutorial_file = output_dir / f'{safe_name}_{algo.language}.md'
            with open(tutorial_file, 'w', encoding='utf-8') as f:
                f.write(tutorial)

        print(f"✓ Generated {len(sample_algos)} sample tutorials")
        print(f"\n✓ All materials generated in {output_dir}")


if __name__ == '__main__':
    main()
