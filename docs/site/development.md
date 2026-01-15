# Development

## Tooling
- **Formatting & linting:** `ruff check`
- **Docs:** `mkdocs serve` for live preview, `mkdocs build --strict` in CI
- **Tests/benchmarks:** Each sub-package includes its own runners; ensure necessary
  dependencies are installed (for example `numpy` + `matplotlib` for graph benchmarks).

## Environment Setup
```bash
python -m pip install -r requirements-dev.txt -r docs/requirements-docs.txt
pre-commit install  # optional but encouraged
```

## Rebuilding the docs locally
```bash
mkdocs build --strict
```

## Guardrails
- Run `tools/docstring_coverage.py` to confirm docstring coverage remains at 100%.
- Execute `pre-commit run --all-files` before opening a pull request; this runs Ruff and
  the docstring coverage gate locally.

## Continuous Integration
Pull requests run the unified workflow in `.github/workflows/ci.yml` plus the standalone
`docs.yml` build. CI enforces installation, lint, type-checking, tests, doc coverage, and
`mkdocs build --strict`, so keep both green before merging.
