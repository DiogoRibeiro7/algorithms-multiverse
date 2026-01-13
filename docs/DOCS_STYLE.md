# Documentation Style Guide

This repository contains Python, Fortran, JavaScript, and other language examples, but the
primary public API that is consumed by tooling and docs automation lives in the Python
packages. This guide standardizes how we document that surface so contributors can produce
consistent API reference material and automated checks can enforce it.

## Public API Definition

Use the following rules to decide whether a symbol must carry a full docstring:

- **Modules**: every `.py` file that ships with the repository (source code, CLIs, scripts)
  unless it is an internal testing helper under `tests/` or `__pycache__`.
- **Classes, functions, coroutines, and context managers** that are imported by a package
  `__init__.py`, exposed via `__all__`, referenced in CLI entry-points, or whose names do not
  start with `_`. Methods that form part of a public class API (again, not prefixed with `_`)
  are public as well.
- **Data containers and enums** (e.g., configuration objects, `Enum` subclasses) because they
  participate in module-level type contracts.

Helper utilities or constants whose names start with `_` are treated as internal and may omit
docstrings, but prefer documenting anything that users or documentation tooling might import.

## Docstring Convention (Google Style)

We adopt the [Google Python style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
and the Ruff `D` (pydocstyle) rule set. Every docstring follows this shape:

```
"""One-line summary in the imperative mood.

Longer description that provides context, intent, or important guarantees.

Args:
    param_name: Description in terms of responsibility and constraints.
    other_param: Mention types or accepted values when the type hint alone is not enough.

Returns:
    Type or semantic meaning of the returned object.

Raises:
    ImportantError: Conditions that trigger this exception.
"""
```

Sections (`Args`, `Keyword Args`, `Attributes`, `Yields`, `Returns`, `Raises`, `Examples`)
are optional and should only be included when they add information beyond the type hints.
Document async functions the same way as synchronous ones.

### Module Docstrings

- Start every Python file with a top-level docstring describing the module purpose, the primary
  algorithms inside, and any side effects (filesystem, network, etc.).
- Reference related documents (e.g., `DOCS_STYLE.md`) or generated reports when helpful.

### Class Docstrings

- Provide an overview sentence plus `Attributes:` or `Properties:` when public attributes exist.
- For dataclasses, describe invariants or derived metadata.
- For enums, document what each member represents or where it is used.

### Function and Method Docstrings

- Begin with an imperative summary (“Return…”, “Compute…”, “Generate…”).
- Include an `Args:` section whenever there is non-obvious behavior or accepted ranges.
- Include `Returns:` and `Raises:` whenever the function returns something or can fail.
- Prefer `Examples:` for CLI scripts or helpers that are commonly invoked from documentation.

### Inline Examples

Embed short code snippets inside triple backticks inside the docstring when the behavior is
easier to describe with code than prose. Keep examples deterministic and fast.

## Inline Comment Rules

- Add comments to capture **why** the code is structured a particular way, list invariants, or
  explain non-obvious control flow or concurrency constraints.
- Place comments above the relevant block, sentence case, no trailing periods unless multiple
  sentences.
- Avoid comments that merely restate the code (“Increment i”, “Call foo()”). They will be
  rejected during review.
- Prefer docstrings over inline comments for API contracts; use inline comments for algorithmic
  insights, hardware assumptions, or tricky resource management.

## Type Hints, Returns, and Raises

- All public callables must include full type hints. When a parameter accepts a `Protocol` or
  callable, describe the expected callable signature in the docstring even if the type hint is
  present.
- When returning tuples, dataclasses, or custom containers, explain the semantic meaning of each
  element in the `Returns:` section.
- Always list user-visible exceptions under `Raises:`; propagate lower-level exceptions when
  possible but mention them if they are part of the public contract.
- Generators and async generators must describe their `Yields:` semantics as well as any
  `Returns:` values (supported in Python 3.10+).

## Review and Tooling Checklist

1. Confirm that module, class, and public callable docstrings exist and follow Google style.
2. Ensure inline comments describe reasoning, not restate instructions.
3. Run `ruff check --select D` (configured in `pyproject.toml`) before submitting a PR.
4. Run `python tools/docstring_coverage.py` to keep coverage above the 100% gate enforced by CI.
5. Update `docs/DOC_COVERAGE.md` whenever a module’s docstring coverage changes.
6. Add entries to `docs/DOC_COVERAGE.md` that explain what was fixed in the current PR.

Following these rules keeps the autogenerated documentation, tutorials, and visualization
pipelines in sync with the constantly evolving algorithm catalog.
