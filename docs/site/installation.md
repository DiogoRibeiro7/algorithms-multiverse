# Installation

The repository ships as source code so you can run the algorithms directly or import
modules inside a virtual environment.

1. **Clone the repo**
   ```bash
   git clone https://github.com/ORIGINAL-OWNER/algorithms-multiverse.git
   cd algorithms-multiverse
   ```
2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate            # Windows
   source .venv/bin/activate             # macOS/Linux
   ```
3. **Install runtime + docs dependencies**
   ```bash
   python -m pip install -r docs/requirements-docs.txt
   ```
   The project does not currently publish a single lock file because each sub-package has
   unique needs. Install any additional requirements on demand (for example
   `pip install numpy matplotlib` before running the MST benchmarks).
4. **Verify the docs build**
   ```bash
   mkdocs build --strict
   ```

After these steps the repository is ready for scripting, benchmarking, and documentation
workflows.
