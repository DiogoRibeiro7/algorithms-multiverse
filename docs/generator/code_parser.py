"""
Multi-Language Code Parser for Algorithm Metadata Extraction

Extracts:
- Algorithm names and categories
- Time and space complexity information
- Function signatures and docstrings
- Examples and use cases
- Language-specific features

Supports: Python, JavaScript, Java, C++, Go, Rust, and more

@author Algorithms Multiverse Documentation System
@version 1.0
"""

import re
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ComplexityType(Enum):
    """Types of complexity analysis"""
    TIME = "time"
    SPACE = "space"
    BEST = "best"
    AVERAGE = "average"
    WORST = "worst"


@dataclass
class Complexity:
    """Represents algorithm complexity"""
    type: ComplexityType
    notation: str  # e.g., "O(n log n)"
    case: Optional[str] = None  # best/average/worst
    description: Optional[str] = None


@dataclass
class FunctionInfo:
    """Information about a function/method"""
    name: str
    signature: str
    docstring: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    description: Optional[str] = None
    examples: List[str] = None
    line_number: int = 0

    def __post_init__(self):
        if self.examples is None:
            self.examples = []


@dataclass
class AlgorithmMetadata:
    """Complete metadata for an algorithm implementation"""
    name: str
    category: str
    language: str
    file_path: str
    description: Optional[str] = None
    time_complexity: List[Complexity] = None
    space_complexity: List[Complexity] = None
    functions: List[FunctionInfo] = None
    examples: List[str] = None
    features: List[str] = None  # Language-specific features
    use_cases: List[str] = None
    references: List[str] = None

    def __post_init__(self):
        if self.time_complexity is None:
            self.time_complexity = []
        if self.space_complexity is None:
            self.space_complexity = []
        if self.functions is None:
            self.functions = []
        if self.examples is None:
            self.examples = []
        if self.features is None:
            self.features = []
        if self.use_cases is None:
            self.use_cases = []
        if self.references is None:
            self.references = []


class CodeParser:
    """Multi-language code parser for extracting algorithm metadata"""

    # Complexity pattern - matches O(...) notations
    COMPLEXITY_PATTERN = re.compile(
        r'O\([^)]+\)|Θ\([^)]+\)|Ω\([^)]+\)',
        re.IGNORECASE
    )

    # Language-specific patterns
    LANGUAGE_PATTERNS = {
        'python': {
            'extension': ['.py'],
            'comment': ['#', '"""', "'''"],
            'function': re.compile(r'^\s*def\s+(\w+)\s*\(([^)]*)\)'),
            'class': re.compile(r'^\s*class\s+(\w+)'),
            'docstring': re.compile(r'"""(.*?)"""', re.DOTALL),
        },
        'javascript': {
            'extension': ['.js', '.mjs'],
            'comment': ['//', '/*', '*'],
            'function': re.compile(r'^\s*(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?function|\s*(\w+)\s*\([^)]*\)\s*\{)'),
            'class': re.compile(r'^\s*class\s+(\w+)'),
            'docstring': re.compile(r'/\*\*(.*?)\*/', re.DOTALL),
        },
        'java': {
            'extension': ['.java'],
            'comment': ['//', '/*', '*'],
            'function': re.compile(r'^\s*(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\('),
            'class': re.compile(r'^\s*(?:public|private)?\s*class\s+(\w+)'),
            'docstring': re.compile(r'/\*\*(.*?)\*/', re.DOTALL),
        },
        'cpp': {
            'extension': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
            'comment': ['//', '/*', '*'],
            'function': re.compile(r'^\s*\w+\s+(\w+)\s*\('),
            'class': re.compile(r'^\s*class\s+(\w+)'),
            'docstring': re.compile(r'/\*\*(.*?)\*/', re.DOTALL),
        },
        'go': {
            'extension': ['.go'],
            'comment': ['//', '/*', '*'],
            'function': re.compile(r'^\s*func\s+(\w+)\s*\('),
            'class': re.compile(r'^\s*type\s+(\w+)\s+struct'),
            'docstring': re.compile(r'//\s*(.*?)(?:\n\s*func|\n\s*type)', re.DOTALL),
        },
        'rust': {
            'extension': ['.rs'],
            'comment': ['//', '/*', '///'],
            'function': re.compile(r'^\s*(?:pub\s+)?fn\s+(\w+)'),
            'class': re.compile(r'^\s*(?:pub\s+)?struct\s+(\w+)'),
            'docstring': re.compile(r'///\s*(.*?)(?:\n\s*(?:pub\s+)?fn)', re.DOTALL),
        },
        'c': {
            'extension': ['.c', '.h'],
            'comment': ['//', '/*', '*'],
            'function': re.compile(r'^\s*\w+\s+(\w+)\s*\('),
            'docstring': re.compile(r'/\*\*(.*?)\*/', re.DOTALL),
        },
    }

    def __init__(self, root_dir: str = None):
        """Initialize parser with repository root directory"""
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()

    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix
        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            if ext in patterns['extension']:
                return lang
        return None

    def extract_complexity(self, text: str) -> List[Complexity]:
        """Extract complexity notations from text"""
        complexities = []

        # Look for time complexity
        time_matches = re.finditer(
            r'(?:Time\s+Complexity|Time|Runtime):\s*([^\n]+)',
            text,
            re.IGNORECASE | re.MULTILINE
        )
        for match in time_matches:
            line = match.group(1)
            notations = self.COMPLEXITY_PATTERN.findall(line)

            # Determine case (best/average/worst)
            case = None
            if 'best' in line.lower():
                case = 'best'
            elif 'average' in line.lower():
                case = 'average'
            elif 'worst' in line.lower():
                case = 'worst'

            for notation in notations:
                complexities.append(Complexity(
                    type=ComplexityType.TIME,
                    notation=notation,
                    case=case,
                    description=line.strip()
                ))

        # Look for space complexity
        space_matches = re.finditer(
            r'(?:Space\s+Complexity|Space|Memory):\s*([^\n]+)',
            text,
            re.IGNORECASE | re.MULTILINE
        )
        for match in space_matches:
            line = match.group(1)
            notations = self.COMPLEXITY_PATTERN.findall(line)

            for notation in notations:
                complexities.append(Complexity(
                    type=ComplexityType.SPACE,
                    notation=notation,
                    description=line.strip()
                ))

        return complexities

    def extract_functions(self, content: str, language: str) -> List[FunctionInfo]:
        """Extract function information from code"""
        functions = []

        if language not in self.LANGUAGE_PATTERNS:
            return functions

        patterns = self.LANGUAGE_PATTERNS[language]
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]
            func_match = patterns['function'].match(line)

            if func_match:
                # Get function name (handle multiple capture groups)
                func_name = next((g for g in func_match.groups() if g), 'unknown')

                # Extract signature (collect until opening brace or colon)
                signature = line.strip()
                j = i + 1
                while j < len(lines) and '{' not in lines[j] and ':' not in lines[j]:
                    signature += ' ' + lines[j].strip()
                    j += 1

                # Extract docstring/comment
                docstring = None
                time_complexity = None
                space_complexity = None

                # Look ahead for docstring
                k = i + 1
                if k < len(lines):
                    docstring_lines = []
                    in_docstring = False

                    # Python docstring
                    if language == 'python' and ('"""' in lines[k] or "'''" in lines[k]):
                        in_docstring = True
                        quote = '"""' if '"""' in lines[k] else "'''"
                        docstring_lines.append(lines[k].replace(quote, ''))
                        k += 1

                        while k < len(lines) and quote not in lines[k]:
                            docstring_lines.append(lines[k])
                            k += 1

                        docstring = '\n'.join(docstring_lines).strip()

                    # JavaScript/Java/C++ doc comment
                    elif language in ['javascript', 'java', 'cpp', 'c'] and '/**' in lines[k-1:k+5]:
                        for m in range(max(0, k-1), min(len(lines), k+10)):
                            if '/**' in lines[m]:
                                in_docstring = True
                                k = m
                            if in_docstring:
                                docstring_lines.append(lines[k].strip('/* \t'))
                                if '*/' in lines[k]:
                                    break
                                k += 1

                        docstring = '\n'.join(docstring_lines).strip()

                # Extract complexity from docstring
                if docstring:
                    complexities = self.extract_complexity(docstring)
                    time_comp = [c.notation for c in complexities if c.type == ComplexityType.TIME]
                    space_comp = [c.notation for c in complexities if c.type == ComplexityType.SPACE]

                    time_complexity = ', '.join(time_comp) if time_comp else None
                    space_complexity = ', '.join(space_comp) if space_comp else None

                functions.append(FunctionInfo(
                    name=func_name,
                    signature=signature,
                    docstring=docstring,
                    time_complexity=time_complexity,
                    space_complexity=space_complexity,
                    line_number=i + 1
                ))

            i += 1

        return functions

    def extract_features(self, content: str, language: str) -> List[str]:
        """Extract language-specific features mentioned in comments"""
        features = []

        # Look for "features:" or "Python features:" etc.
        feature_pattern = re.compile(
            r'(?:' + language + r'\s+)?features?:\s*([^\n]+(?:\n-[^\n]+)*)',
            re.IGNORECASE | re.MULTILINE
        )

        matches = feature_pattern.finditer(content)
        for match in matches:
            feature_text = match.group(1)
            # Split by newlines and bullet points
            feature_lines = [
                line.strip('- \t')
                for line in feature_text.split('\n')
                if line.strip()
            ]
            features.extend(feature_lines)

        return features

    def parse_file(self, file_path: str) -> Optional[AlgorithmMetadata]:
        """Parse a single file and extract algorithm metadata"""
        file_path = Path(file_path)

        if not file_path.exists():
            return None

        language = self.detect_language(str(file_path))
        if not language:
            return None

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

        # Determine category from directory structure
        parts = file_path.parts
        category = 'uncategorized'
        for part in parts:
            if part in ['sorting', 'searching', 'data-structures', 'graph-algorithms',
                       'dynamic-programming', 'string-algorithms', 'mathematical',
                       'computational-geometry', 'number-theory']:
                category = part
                break

        # Extract algorithm name from filename
        name = file_path.stem.replace('_', ' ').replace('-', ' ').title()

        # Extract header docstring/comment (first 50 lines)
        header = '\n'.join(content.split('\n')[:50])

        # Extract description
        description = None
        desc_patterns = [
            re.compile(r'"""(.*?)"""', re.DOTALL),
            re.compile(r'/\*\*(.*?)\*/', re.DOTALL),
            re.compile(r'//\s*(.*?)(?:\n\s*\n)', re.DOTALL),
        ]
        for pattern in desc_patterns:
            match = pattern.search(header)
            if match:
                description = match.group(1).strip()
                break

        # Extract complexities
        complexities = self.extract_complexity(header)
        time_complexities = [c for c in complexities if c.type == ComplexityType.TIME]
        space_complexities = [c for c in complexities if c.type == ComplexityType.SPACE]

        # Extract functions
        functions = self.extract_functions(content, language)

        # Extract features
        features = self.extract_features(header, language)

        # Extract examples (look for example code blocks)
        examples = []
        example_pattern = re.compile(
            r'(?:Example|Usage|Demo):\s*```.*?\n(.*?)```',
            re.DOTALL | re.IGNORECASE
        )
        for match in example_pattern.finditer(content):
            examples.append(match.group(1).strip())

        # Also look for >>> doctest examples
        doctest_pattern = re.compile(r'>>>\s+([^\n]+(?:\n(?!>>>)[^\n]+)*)', re.MULTILINE)
        for match in doctest_pattern.finditer(content):
            examples.append(match.group(0).strip())

        metadata = AlgorithmMetadata(
            name=name,
            category=category,
            language=language,
            file_path=str(file_path.relative_to(self.root_dir)),
            description=description,
            time_complexity=time_complexities,
            space_complexity=space_complexities,
            functions=functions,
            examples=examples[:5],  # Limit to 5 examples
            features=features,
        )

        return metadata

    def parse_directory(self, directory: str = None) -> List[AlgorithmMetadata]:
        """Parse all algorithm files in a directory"""
        if directory is None:
            directory = self.root_dir
        else:
            directory = Path(directory)

        results = []

        # Get all supported file extensions
        extensions = set()
        for patterns in self.LANGUAGE_PATTERNS.values():
            extensions.update(patterns['extension'])

        # Walk through directory
        for ext in extensions:
            for file_path in directory.rglob(f'*{ext}'):
                # Skip test files, benchmarks, and docs
                if any(x in str(file_path).lower() for x in ['test', 'benchmark', 'docs', '__pycache__', 'node_modules', 'target', 'build']):
                    continue

                metadata = self.parse_file(str(file_path))
                if metadata:
                    results.append(metadata)

        return results

    def export_to_json(self, metadata_list: List[AlgorithmMetadata], output_file: str):
        """Export metadata to JSON file"""
        data = []
        for metadata in metadata_list:
            item = asdict(metadata)
            # Convert Complexity objects to dicts
            item['time_complexity'] = [
                {'type': c.type.value, 'notation': c.notation, 'case': c.case, 'description': c.description}
                for c in metadata.time_complexity
            ]
            item['space_complexity'] = [
                {'type': c.type.value, 'notation': c.notation, 'case': c.case, 'description': c.description}
                for c in metadata.space_complexity
            ]
            data.append(item)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Exported {len(data)} algorithm metadata to {output_file}")


def main():
    """Main entry point for code parser"""
    import argparse

    parser = argparse.ArgumentParser(description='Parse algorithm code and extract metadata')
    parser.add_argument('--dir', default='.', help='Directory to parse (default: current)')
    parser.add_argument('--file', help='Single file to parse')
    parser.add_argument('--output', default='docs/output/metadata.json', help='Output JSON file')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    code_parser = CodeParser(root_dir=args.dir)

    if args.file:
        # Parse single file
        metadata = code_parser.parse_file(args.file)
        if metadata:
            if args.verbose:
                print(f"\nAlgorithm: {metadata.name}")
                print(f"Category: {metadata.category}")
                print(f"Language: {metadata.language}")
                print(f"Functions: {len(metadata.functions)}")
                print(f"Time Complexities: {[c.notation for c in metadata.time_complexity]}")
                print(f"Space Complexities: {[c.notation for c in metadata.space_complexity]}")

            code_parser.export_to_json([metadata], args.output)
        else:
            print(f"Failed to parse {args.file}")
    else:
        # Parse directory
        print(f"Parsing algorithms in {args.dir}...")
        metadata_list = code_parser.parse_directory(args.dir)

        print(f"\nFound {len(metadata_list)} algorithm implementations")

        # Group by category
        by_category = {}
        for metadata in metadata_list:
            if metadata.category not in by_category:
                by_category[metadata.category] = []
            by_category[metadata.category].append(metadata)

        print("\nBy Category:")
        for category, items in sorted(by_category.items()):
            print(f"  {category}: {len(items)} implementations")

        # Group by language
        by_language = {}
        for metadata in metadata_list:
            if metadata.language not in by_language:
                by_language[metadata.language] = []
            by_language[metadata.language].append(metadata)

        print("\nBy Language:")
        for language, items in sorted(by_language.items()):
            print(f"  {language}: {len(items)} implementations")

        # Export to JSON
        code_parser.export_to_json(metadata_list, args.output)


if __name__ == '__main__':
    main()
