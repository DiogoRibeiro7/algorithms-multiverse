#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Documentation Generation Orchestrator

Coordinates all documentation generation components:
1. Parse code and extract metadata
2. Generate documentation (cheat sheets, comparisons, API refs)
3. Create learning paths and tutorials
4. Export interactive visualizations

Usage:
    python generate_docs.py
    python generate_docs.py --quick  # Skip tutorials
    python generate_docs.py --category sorting  # Specific category only

@author Algorithms Multiverse Documentation System
@version 1.0
"""

import sys
import json
import shutil
import io
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add generator modules to path
sys.path.insert(0, str(Path(__file__).parent))

from code_parser import CodeParser, AlgorithmMetadata
from doc_generator import DocumentationGenerator
from tutorial_generator import TutorialGenerator


class DocumentationOrchestrator:
    """Orchestrates the entire documentation generation pipeline"""

    def __init__(self, root_dir: str = None, output_dir: str = None):
        """Initialize orchestrator"""
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()
        self.output_dir = Path(output_dir) if output_dir else self.root_dir / 'docs' / 'output'
        self.metadata_file = self.output_dir / 'metadata.json'

        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'cheatsheets').mkdir(exist_ok=True)
        (self.output_dir / 'comparisons').mkdir(exist_ok=True)
        (self.output_dir / 'api').mkdir(exist_ok=True)
        (self.output_dir / 'tutorials').mkdir(exist_ok=True)

        self.metadata = []
        self.stats = {
            'total_files': 0,
            'total_algorithms': 0,
            'by_category': {},
            'by_language': {},
            'generation_time': 0,
        }

    def step1_parse_code(self, directory: str = None):
        """Step 1: Parse all code and extract metadata"""
        print("\n" + "="*70)
        print("STEP 1: Parsing Code and Extracting Metadata")
        print("="*70)

        parser = CodeParser(root_dir=self.root_dir)

        if directory:
            parse_dir = Path(directory)
        else:
            parse_dir = self.root_dir

        print(f"\nScanning directory: {parse_dir}")

        self.metadata = parser.parse_directory(str(parse_dir))

        print(f"\n✓ Parsed {len(self.metadata)} algorithm implementations")

        # Update stats
        self.stats['total_files'] = len(self.metadata)
        self.stats['total_algorithms'] = len(set(m.name for m in self.metadata))

        # Group by category
        for meta in self.metadata:
            cat = meta.category
            if cat not in self.stats['by_category']:
                self.stats['by_category'][cat] = 0
            self.stats['by_category'][cat] += 1

        # Group by language
        for meta in self.metadata:
            lang = meta.language
            if lang not in self.stats['by_language']:
                self.stats['by_language'][lang] = 0
            self.stats['by_language'][lang] += 1

        # Display breakdown
        print("\nBy Category:")
        for category, count in sorted(self.stats['by_category'].items()):
            print(f"  {category:25} {count:3} files")

        print("\nBy Language:")
        for language, count in sorted(self.stats['by_language'].items()):
            print(f"  {language:15} {count:3} implementations")

        # Export metadata
        parser.export_to_json(self.metadata, str(self.metadata_file))
        print(f"\n✓ Metadata exported to {self.metadata_file}")

    def step2_generate_documentation(self):
        """Step 2: Generate all documentation"""
        print("\n" + "="*70)
        print("STEP 2: Generating Documentation")
        print("="*70)

        if not self.metadata_file.exists():
            print("ERROR: Metadata file not found. Run step 1 first.")
            return

        generator = DocumentationGenerator(
            metadata_file=str(self.metadata_file),
            output_dir=str(self.output_dir)
        )

        generator.generate_all_documentation()

    def step3_generate_tutorials(self, sample_count: int = 10):
        """Step 3: Generate learning paths and tutorials"""
        print("\n" + "="*70)
        print("STEP 3: Generating Learning Paths and Tutorials")
        print("="*70)

        if not self.metadata_file.exists():
            print("ERROR: Metadata file not found. Run step 1 first.")
            return

        # Load metadata
        from code_parser import Complexity, ComplexityType, FunctionInfo

        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        metadata = []
        for item in data:
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

        tutorial_gen = TutorialGenerator(metadata)
        tutorial_dir = self.output_dir / 'tutorials'

        # Generate learning paths
        print("\n  - Generating learning paths...")
        learning_path = tutorial_gen.generate_learning_path_doc()
        with open(tutorial_dir / 'learning_paths.md', 'w', encoding='utf-8') as f:
            f.write(learning_path)
        print("    ✓ Learning paths generated")

        # Generate quick reference
        print("  - Generating quick reference...")
        quick_ref = tutorial_gen.generate_quick_reference()
        with open(tutorial_dir / 'quick_reference.md', 'w', encoding='utf-8') as f:
            f.write(quick_ref)
        print("    ✓ Quick reference generated")

        # Generate sample tutorials
        print(f"  - Generating {sample_count} sample tutorials...")
        sample_algos = metadata[:sample_count]

        for algo in sample_algos:
            tutorial = tutorial_gen.generate_algorithm_tutorial(algo)
            safe_name = algo.name.lower().replace(' ', '_')
            tutorial_file = tutorial_dir / f'{safe_name}_{algo.language}.md'
            with open(tutorial_file, 'w', encoding='utf-8') as f:
                f.write(tutorial)

        print(f"    ✓ Generated {len(sample_algos)} tutorials")

    def step4_setup_interactive(self):
        """Step 4: Setup interactive visualizations"""
        print("\n" + "="*70)
        print("STEP 4: Setting Up Interactive Visualizations")
        print("="*70)

        interactive_src = self.root_dir / 'docs' / 'interactive' / 'algorithm_visualizer.html'
        interactive_dst = self.output_dir / 'algorithm_visualizer.html'

        if interactive_src.exists():
            shutil.copy(interactive_src, interactive_dst)
            print(f"\n✓ Interactive visualizer copied to {interactive_dst}")
            print(f"  Open in browser: file://{interactive_dst.absolute()}")
        else:
            print(f"\nWARNING: Visualizer not found at {interactive_src}")

    def generate_index(self):
        """Generate main index file"""
        print("\n" + "="*70)
        print("Generating Index File")
        print("="*70)

        output = []

        output.append("# Algorithm Documentation - Algorithms Multiverse\n\n")
        output.append(f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

        output.append("## 📚 Documentation Overview\n\n")
        output.append("Complete, automatically generated documentation for the Algorithms Multiverse repository.\n\n")

        # Stats
        output.append("## 📊 Statistics\n\n")
        output.append(f"- **Total Files**: {self.stats['total_files']}\n")
        output.append(f"- **Unique Algorithms**: {self.stats['total_algorithms']}\n")
        output.append(f"- **Categories**: {len(self.stats['by_category'])}\n")
        output.append(f"- **Languages**: {len(self.stats['by_language'])}\n\n")

        # Quick links
        output.append("## 🚀 Quick Links\n\n")
        output.append("### Essential References\n\n")
        output.append("- [**Complexity Cheat Sheet**](cheatsheets/complexity_cheatsheet.md) - Quick complexity reference\n")
        output.append("- [**Implementation Comparison**](comparisons/implementation_comparison.md) - Cross-language comparisons\n")
        output.append("- [**Performance Report**](performance_report.md) - Performance analysis\n\n")

        output.append("### Learning Materials\n\n")
        output.append("- [**Learning Paths**](tutorials/learning_paths.md) - Structured curriculum\n")
        output.append("- [**Quick Reference**](tutorials/quick_reference.md) - Quick lookup guide\n")
        output.append("- [**Interactive Visualizer**](algorithm_visualizer.html) - Visual algorithm learning\n\n")

        output.append("### API References\n\n")
        api_dir = self.output_dir / 'api'
        if api_dir.exists():
            for api_file in sorted(api_dir.glob('*.md')):
                lang = api_file.stem.replace('_api', '').title()
                output.append(f"- [{lang} API Reference](api/{api_file.name})\n")
        output.append("\n")

        # Category breakdown
        output.append("## 📂 By Category\n\n")
        for category, count in sorted(self.stats['by_category'].items()):
            cat_title = category.replace('-', ' ').title()
            output.append(f"- **{cat_title}**: {count} implementations\n")
        output.append("\n")

        # Language breakdown
        output.append("## 🌐 By Language\n\n")
        for language, count in sorted(self.stats['by_language'].items()):
            output.append(f"- **{language.title()}**: {count} implementations\n")
        output.append("\n")

        # How to use
        output.append("## 📖 How to Use This Documentation\n\n")
        output.append("1. **Start with the [Complexity Cheat Sheet](cheatsheets/complexity_cheatsheet.md)** for quick complexity lookups\n")
        output.append("2. **Follow the [Learning Paths](tutorials/learning_paths.md)** for structured learning\n")
        output.append("3. **Use the [Implementation Comparison](comparisons/implementation_comparison.md)** to see cross-language differences\n")
        output.append("4. **Explore [API References](api/)** for detailed function documentation\n")
        output.append("5. **Try the [Interactive Visualizer](algorithm_visualizer.html)** to see algorithms in action\n\n")

        # Generation info
        output.append("---\n\n")
        output.append("## 🔧 About This Documentation\n\n")
        output.append("This documentation is automatically generated from source code using the documentation generation system.\n\n")
        output.append("**Generation System Components:**\n\n")
        output.append("- `code_parser.py` - Extracts metadata from source code\n")
        output.append("- `doc_generator.py` - Generates markdown documentation\n")
        output.append("- `tutorial_generator.py` - Creates learning paths and tutorials\n")
        output.append("- `generate_docs.py` - Main orchestration script\n\n")

        output.append("**To regenerate:**\n\n")
        output.append("```bash\n")
        output.append("python docs/generator/generate_docs.py\n")
        output.append("```\n\n")

        index_file = self.output_dir / 'README.md'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(''.join(output))

        print(f"\n✓ Index file generated: {index_file}")

    def run_all(self, quick_mode: bool = False, category: str = None):
        """Run complete documentation generation pipeline"""
        start_time = datetime.now()

        print("\n" + "="*70)
        print(" ALGORITHMS MULTIVERSE - DOCUMENTATION GENERATOR")
        print("="*70)
        print(f"\nStarted at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Root directory: {self.root_dir}")
        print(f"Output directory: {self.output_dir}")

        if category:
            print(f"Category filter: {category}")
            category_dir = self.root_dir / category
            if not category_dir.exists():
                print(f"ERROR: Category directory not found: {category_dir}")
                return
            self.step1_parse_code(str(category_dir))
        else:
            self.step1_parse_code()

        self.step2_generate_documentation()

        if not quick_mode:
            self.step3_generate_tutorials(sample_count=15)
        else:
            print("\n[Quick mode: Skipping tutorials]")

        self.step4_setup_interactive()

        self.generate_index()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        self.stats['generation_time'] = duration

        # Final summary
        print("\n" + "="*70)
        print(" GENERATION COMPLETE")
        print("="*70)
        print(f"\n✓ Documentation generated in {duration:.2f} seconds")
        print(f"\n📁 Output location: {self.output_dir}")
        print(f"\n📖 Open index: {self.output_dir / 'README.md'}")
        print(f"🎨 Open visualizer: file://{(self.output_dir / 'algorithm_visualizer.html').absolute()}")
        print("\n" + "="*70 + "\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate comprehensive algorithm documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all documentation
  python generate_docs.py

  # Quick mode (skip tutorials)
  python generate_docs.py --quick

  # Specific category only
  python generate_docs.py --category sorting

  # Custom directories
  python generate_docs.py --root /path/to/repo --output /path/to/output
        """
    )

    parser.add_argument('--root', default='.',
                       help='Root directory of repository (default: current)')
    parser.add_argument('--output', default='docs/output',
                       help='Output directory (default: docs/output)')
    parser.add_argument('--quick', action='store_true',
                       help='Quick mode (skip tutorials)')
    parser.add_argument('--category', help='Generate for specific category only')
    parser.add_argument('--parse-only', action='store_true',
                       help='Only parse code, don\'t generate docs')

    args = parser.parse_args()

    orchestrator = DocumentationOrchestrator(
        root_dir=args.root,
        output_dir=args.output
    )

    if args.parse_only:
        orchestrator.step1_parse_code(args.category)
    else:
        orchestrator.run_all(quick_mode=args.quick, category=args.category)


if __name__ == '__main__':
    main()
