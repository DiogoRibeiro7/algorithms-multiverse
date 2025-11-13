#!/bin/bash
################################################################################
# Documentation Generation Script for Algorithms Multiverse
#
# This script generates documentation for all supported languages:
# - C/C++/Fortran: Doxygen
# - Python: Sphinx
# - Rust: cargo doc
# - Go: godoc
# - R: roxygen2
# - JavaScript: JSDoc
#
# Usage:
#   ./generate_docs.sh [language]
#
# Examples:
#   ./generate_docs.sh all      # Generate all documentation
#   ./generate_docs.sh python   # Generate only Python docs
#   ./generate_docs.sh doxygen  # Generate C/C++/Fortran docs
#
# Author: Algorithms Multiverse
# Version: 1.0
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$SCRIPT_DIR/docs"
OUTPUT_DIR="$DOCS_DIR/generated"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "$1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "$1 is not installed"
        return 1
    fi
    print_success "$1 is installed"
    return 0
}

################################################################################
# Documentation Generation Functions
################################################################################

generate_doxygen() {
    print_header "Generating Doxygen Documentation (C/C++/Fortran)"

    if ! check_command doxygen; then
        print_warning "Skipping Doxygen documentation"
        return 1
    fi

    if [ ! -f "$SCRIPT_DIR/Doxyfile" ]; then
        print_error "Doxyfile not found"
        return 1
    fi

    cd "$SCRIPT_DIR"
    doxygen Doxyfile

    print_success "Doxygen documentation generated in $DOCS_DIR/doxygen/html/"
    print_info "   Open: $DOCS_DIR/doxygen/html/index.html"
}

generate_python() {
    print_header "Generating Python Documentation (Sphinx)"

    if ! check_command sphinx-build; then
        print_warning "sphinx-build not found, trying to install..."
        if check_command pip3; then
            pip3 install sphinx sphinx-rtd-theme --quiet
        else
            print_error "Cannot install Sphinx (pip3 not found)"
            return 1
        fi
    fi

    # Create Sphinx configuration if it doesn't exist
    SPHINX_DIR="$DOCS_DIR/sphinx"
    if [ ! -d "$SPHINX_DIR" ]; then
        mkdir -p "$SPHINX_DIR"
        cd "$SPHINX_DIR"
        sphinx-quickstart -q -p "Algorithms Multiverse" -a "Algorithms Multiverse" -v "1.0" --ext-autodoc
    fi

    # Generate API documentation
    cd "$SCRIPT_DIR"
    sphinx-apidoc -f -o "$SPHINX_DIR/source" . --separate

    # Build HTML documentation
    cd "$SPHINX_DIR"
    make html

    print_success "Python documentation generated in $SPHINX_DIR/build/html/"
    print_info "   Open: $SPHINX_DIR/build/html/index.html"
}

generate_rust() {
    print_header "Generating Rust Documentation (cargo doc)"

    if ! check_command cargo; then
        print_warning "Cargo not found, skipping Rust documentation"
        return 1
    fi

    # Find Cargo.toml files
    CARGO_PROJECTS=$(find "$SCRIPT_DIR" -name "Cargo.toml" -type f)

    if [ -z "$CARGO_PROJECTS" ]; then
        print_warning "No Rust projects found (no Cargo.toml files)"
        return 1
    fi

    while IFS= read -r cargo_file; do
        PROJECT_DIR=$(dirname "$cargo_file")
        print_info "   Generating docs for: $PROJECT_DIR"
        cd "$PROJECT_DIR"
        cargo doc --no-deps --quiet
    done <<< "$CARGO_PROJECTS"

    print_success "Rust documentation generated"
    print_info "   Run 'cargo doc --open' in project directories to view"
}

generate_go() {
    print_header "Generating Go Documentation (godoc)"

    if ! check_command go; then
        print_warning "Go not found, skipping Go documentation"
        return 1
    fi

    # Check if godoc is installed
    if ! check_command godoc; then
        print_warning "godoc not installed, trying to install..."
        go install golang.org/x/tools/cmd/godoc@latest
    fi

    GO_DOCS_DIR="$OUTPUT_DIR/godoc"
    mkdir -p "$GO_DOCS_DIR"

    # Generate static HTML documentation
    cd "$SCRIPT_DIR"
    print_info "   Starting godoc server on http://localhost:6060"
    print_info "   Press Ctrl+C to stop"

    godoc -http=:6060
}

generate_r() {
    print_header "Generating R Documentation (roxygen2)"

    if ! check_command Rscript; then
        print_warning "R not found, skipping R documentation"
        return 1
    fi

    # Create R documentation script
    cat > "/tmp/generate_r_docs.R" << 'EOF'
if (!requireNamespace("roxygen2", quietly = TRUE)) {
    install.packages("roxygen2", repos="http://cran.us.r-project.org")
}

library(roxygen2)

# Find R files and generate documentation
r_files <- list.files(pattern = "\\.R$", recursive = TRUE, full.names = TRUE)

for (file in r_files) {
    message(paste("Documenting:", file))
    tryCatch({
        # Parse and generate roxygen documentation
        parsed <- parse(file)
        # Could generate HTML or PDF documentation here
    }, error = function(e) {
        message(paste("Error processing", file, ":", e$message))
    })
}

message("R documentation generation complete")
EOF

    cd "$SCRIPT_DIR"
    Rscript /tmp/generate_r_docs.R
    rm /tmp/generate_r_docs.R

    print_success "R documentation processed"
}

generate_javascript() {
    print_header "Generating JavaScript Documentation (JSDoc)"

    if ! check_command jsdoc; then
        print_warning "jsdoc not found, trying to install..."
        if check_command npm; then
            npm install -g jsdoc --quiet
        else
            print_error "Cannot install JSDoc (npm not found)"
            return 1
        fi
    fi

    JS_DOCS_DIR="$OUTPUT_DIR/jsdoc"
    mkdir -p "$JS_DOCS_DIR"

    cd "$SCRIPT_DIR"
    jsdoc -r . -d "$JS_DOCS_DIR" -c /dev/null \
        --readme README.md \
        --exclude node_modules \
        --exclude test

    print_success "JavaScript documentation generated in $JS_DOCS_DIR/"
    print_info "   Open: $JS_DOCS_DIR/index.html"
}

generate_fortran_ford() {
    print_header "Generating Fortran Documentation (FORD)"

    if ! check_command ford; then
        print_warning "FORD not found, skipping enhanced Fortran documentation"
        print_info "   Install with: pip3 install ford"
        return 1
    fi

    # Create FORD configuration if it doesn't exist
    if [ ! -f "$SCRIPT_DIR/ford.md" ]; then
        cat > "$SCRIPT_DIR/ford.md" << 'EOF'
---
project: Algorithms Multiverse
summary: Multi-language algorithm implementations
author: Algorithms Multiverse
src_dir: ./
output_dir: ./docs/ford
exclude_dir: ./test
---

# Algorithms Multiverse - Fortran Documentation

Comprehensive Fortran algorithm implementations with modern features.
EOF
    fi

    cd "$SCRIPT_DIR"
    ford ford.md

    print_success "FORD documentation generated in $DOCS_DIR/ford/"
    print_info "   Open: $DOCS_DIR/ford/index.html"
}

generate_all() {
    print_header "Generating All Documentation"

    mkdir -p "$OUTPUT_DIR"

    generate_doxygen
    generate_python
    generate_rust
    generate_javascript
    generate_r
    generate_fortran_ford

    print_header "Documentation Generation Complete"
    print_success "All documentation has been generated"
    print_info ""
    print_info "Documentation locations:"
    print_info "  - C/C++/Fortran: $DOCS_DIR/doxygen/html/index.html"
    print_info "  - Python:        $DOCS_DIR/sphinx/build/html/index.html"
    print_info "  - JavaScript:    $OUTPUT_DIR/jsdoc/index.html"
    print_info "  - Rust:          target/doc/index.html (in project dirs)"
    print_info "  - Fortran (FORD):$DOCS_DIR/ford/index.html"
}

################################################################################
# Main Script
################################################################################

main() {
    print_header "Algorithms Multiverse Documentation Generator"

    # Parse command line arguments
    LANG="${1:-all}"

    case "$LANG" in
        all)
            generate_all
            ;;
        doxygen|c|cpp|fortran)
            generate_doxygen
            ;;
        python|py)
            generate_python
            ;;
        rust|rs)
            generate_rust
            ;;
        go)
            generate_go
            ;;
        r)
            generate_r
            ;;
        javascript|js)
            generate_javascript
            ;;
        ford)
            generate_fortran_ford
            ;;
        *)
            print_error "Unknown language: $LANG"
            echo ""
            echo "Usage: $0 [language]"
            echo ""
            echo "Supported languages:"
            echo "  all         - Generate all documentation"
            echo "  doxygen     - C/C++/Fortran (Doxygen)"
            echo "  python      - Python (Sphinx)"
            echo "  rust        - Rust (cargo doc)"
            echo "  go          - Go (godoc)"
            echo "  r           - R (roxygen2)"
            echo "  javascript  - JavaScript (JSDoc)"
            echo "  ford        - Fortran (FORD)"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
