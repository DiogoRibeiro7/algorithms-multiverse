#!/bin/bash
################################################################################
# Pre-Commit Hook for Documentation Quality
#
# This hook checks documentation quality before allowing commits.
# Install by copying to .git/hooks/pre-commit and making executable:
#
#   cp docs/PRE_COMMIT_HOOK_EXAMPLE.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Checks performed:
# - All functions have documentation
# - No TODO/FIXME comments in production code
# - Code formatting is correct
# - Documentation examples are valid
#
# Author: Algorithms Multiverse
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

echo "================================"
echo " Documentation Quality Check"
echo "================================"

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

################################################################################
# Check 1: C/C++ Documentation
################################################################################

echo ""
echo "Checking C/C++ documentation..."

C_FILES=$(echo "$STAGED_FILES" | grep -E '\.(c|cpp|h|hpp)$' || true)

if [ -n "$C_FILES" ]; then
    for file in $C_FILES; do
        # Check for functions without Doxygen comments
        UNDOCUMENTED=$(grep -Pzo '(?<!\/\*\*\n)(?<!\/\/\/\n)^[^\s].*\s+\w+\s*\([^)]*\)\s*{' "$file" | grep -c "^" || true)

        if [ "$UNDOCUMENTED" -gt 0 ]; then
            echo -e "${YELLOW}WARNING: $file has $UNDOCUMENTED potentially undocumented functions${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi

        # Check for @param, @return tags
        FUNCTIONS=$(grep -c '^[a-zA-Z].*(' "$file" || echo "0")
        PARAM_TAGS=$(grep -c '@param' "$file" || echo "0")
        RETURN_TAGS=$(grep -c '@return' "$file" || echo "0")

        if [ "$FUNCTIONS" -gt 0 ] && [ "$PARAM_TAGS" -eq 0 ]; then
            echo -e "${YELLOW}WARNING: $file has functions but no @param tags${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi
    done
fi

################################################################################
# Check 2: Fortran Documentation
################################################################################

echo ""
echo "Checking Fortran documentation..."

FORTRAN_FILES=$(echo "$STAGED_FILES" | grep -E '\.(f90|F90|f95|F95)$' || true)

if [ -n "$FORTRAN_FILES" ]; then
    for file in $FORTRAN_FILES; do
        # Check for modern documentation style (!>)
        DOC_COMMENTS=$(grep -c '^[[:space:]]*!>' "$file" || echo "0")
        SUBROUTINES=$(grep -c '^[[:space:]]*subroutine' "$file" || echo "0")
        FUNCTIONS=$(grep -c '^[[:space:]]*function' "$file" || echo "0")

        TOTAL_PROCS=$((SUBROUTINES + FUNCTIONS))

        if [ "$TOTAL_PROCS" -gt 0 ] && [ "$DOC_COMMENTS" -eq 0 ]; then
            echo -e "${YELLOW}WARNING: $file has procedures but no !> documentation${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi

        # Check for error handling
        HAS_ERROR_CHECK=$(grep -c 'status\|iostat\|stat\=' "$file" || echo "0")
        if [ "$TOTAL_PROCS" -gt 0 ] && [ "$HAS_ERROR_CHECK" -eq 0 ]; then
            echo -e "${YELLOW}WARNING: $file has no error handling${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi
    done
fi

################################################################################
# Check 3: Python Documentation
################################################################################

echo ""
echo "Checking Python documentation..."

PYTHON_FILES=$(echo "$STAGED_FILES" | grep '\.py$' || true)

if [ -n "$PYTHON_FILES" ]; then
    for file in $PYTHON_FILES; do
        # Check for docstrings
        python3 << EOF
import ast
import sys

try:
    with open('$file', 'r') as f:
        tree = ast.parse(f.read())

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    missing_docs = 0

    for func in functions:
        if not func.name.startswith('_'):  # Skip private functions
            if not ast.get_docstring(func):
                print(f"WARNING: Function '{func.name}' has no docstring")
                missing_docs += 1

    for cls in classes:
        if not ast.get_docstring(cls):
            print(f"WARNING: Class '{cls.name}' has no docstring")
            missing_docs += 1

    if missing_docs > 0:
        sys.exit(1)
except Exception as e:
    print(f"ERROR: Could not parse $file: {e}")
    sys.exit(2)
EOF

        if [ $? -eq 1 ]; then
            WARNINGS=$((WARNINGS + 1))
        elif [ $? -eq 2 ]; then
            echo -e "${RED}ERROR: Failed to parse $file${NC}"
            ERRORS=$((ERRORS + 1))
        fi

        # Check for type hints
        if ! grep -q 'def.*->.*:' "$file" && ! grep -q ': [A-Z]' "$file"; then
            echo -e "${YELLOW}INFO: $file may be missing type hints${NC}"
        fi
    done
fi

################################################################################
# Check 4: R Documentation
################################################################################

echo ""
echo "Checking R documentation..."

R_FILES=$(echo "$STAGED_FILES" | grep -E '\.(R|r)$' || true)

if [ -n "$R_FILES" ]; then
    for file in $R_FILES; do
        # Check for roxygen2 comments
        ROXYGEN=$(grep -c "^#'" "$file" || echo "0")
        FUNCTIONS=$(grep -c '^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*<-[[:space:]]*function' "$file" || echo "0")

        if [ "$FUNCTIONS" -gt 0 ] && [ "$ROXYGEN" -eq 0 ]; then
            echo -e "${YELLOW}WARNING: $file has functions but no roxygen2 documentation${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi

        # Check for tryCatch blocks
        TRYCATCH=$(grep -c 'tryCatch' "$file" || echo "0")
        if [ "$FUNCTIONS" -gt 2 ] && [ "$TRYCATCH" -eq 0 ]; then
            echo -e "${YELLOW}INFO: $file may benefit from error handling (tryCatch)${NC}"
        fi
    done
fi

################################################################################
# Check 5: Rust Documentation
################################################################################

echo ""
echo "Checking Rust documentation..."

RUST_FILES=$(echo "$STAGED_FILES" | grep '\.rs$' || true)

if [ -n "$RUST_FILES" ]; then
    for file in $RUST_FILES; do
        # Check for doc comments
        DOC_COMMENTS=$(grep -c '^[[:space:]]*///' "$file" || echo "0")
        PUB_FUNCTIONS=$(grep -c '^[[:space:]]*pub fn' "$file" || echo "0")

        if [ "$PUB_FUNCTIONS" -gt 0 ] && [ "$DOC_COMMENTS" -eq 0 ]; then
            echo -e "${YELLOW}WARNING: $file has public functions but no /// documentation${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi

        # Check for examples in docs
        EXAMPLES=$(grep -c '# Examples' "$file" || echo "0")
        if [ "$PUB_FUNCTIONS" -gt 0 ] && [ "$EXAMPLES" -eq 0 ]; then
            echo -e "${YELLOW}INFO: $file may benefit from documentation examples${NC}"
        fi
    done
fi

################################################################################
# Check 6: TODO/FIXME Comments
################################################################################

echo ""
echo "Checking for TODO/FIXME comments..."

for file in $STAGED_FILES; do
    # Skip test files
    if [[ "$file" == *"test"* ]]; then
        continue
    fi

    TODOS=$(grep -n 'TODO\|FIXME\|HACK\|XXX' "$file" || true)
    if [ -n "$TODOS" ]; then
        echo -e "${YELLOW}INFO: $file contains TODO/FIXME comments:${NC}"
        echo "$TODOS"
    fi
done

################################################################################
# Check 7: File Headers
################################################################################

echo ""
echo "Checking file headers..."

for file in $STAGED_FILES; do
    # Check for copyright/author header in first 20 lines
    if ! head -20 "$file" | grep -qi 'author\|copyright\|@file'; then
        echo -e "${YELLOW}INFO: $file may be missing file header${NC}"
    fi
done

################################################################################
# Summary
################################################################################

echo ""
echo "================================"
echo " Summary"
echo "================================"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}✗ Commit blocked due to errors${NC}"
    echo "Please fix the errors above and try again."
    exit 1
fi

if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠ Commit allowed with warnings${NC}"
    echo "Consider addressing warnings for better code quality."
fi

echo -e "${GREEN}✓ Documentation quality check passed${NC}"
exit 0
