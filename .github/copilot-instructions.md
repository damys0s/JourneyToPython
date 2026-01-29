# AI Coding Agent Instructions for JourneyToPython

## Project Overview
JourneyToPython is an educational Python project (v0.1.0) designed to explore Python concepts using modern practices. The project focuses on clean code patterns using `dataclasses`, type hints, and the `rich` library for enhanced console output.

**Python Version**: >=3.12.12  
**Key Dependency**: `rich>=14.3.1` for advanced terminal formatting

## Architecture & Key Components

### Main Modules
- **[main.py](main.py)**: Core module containing:
  - `Person` dataclass with nested defaults (id generation, email list)
  - `generate_id()` function using `random` string generation
  - Entry point demonstrating dataclass instantiation and printing

- **[demo.py](demo.py)**: Example/testing module showing:
  - Python version introspection
  - `rich` library import (currently commented)
  - Exploration of Python capabilities

### Data Model: Person
The `Person` dataclass demonstrates advanced patterns:
```python
@dataclass
class Person:
    name: str
    address: str
    active: bool = True
    email_adresses: list[str] = field(default_factory=list)  # Note: typo in field name (email_adresses)
    id: str = field(default_factory=generate_id)
```
**Pattern**: Uses `field(default_factory=...)` for mutable defaults and callable defaults, not `default=` assignments.

## Developer Conventions

### Styling & Type Hints
- **Python 3.12+ idioms**: Use `list[str]` instead of `List[str]` (no `typing` imports needed)
- **Dataclasses**: Preferred for data structures; always use type annotations
- **Return type hints**: All functions include explicit `-> ReturnType` annotations (see `generate_id() -> str`)
- **Main block**: Use `if __name__ == "__main__":` pattern for executable modules

### Import Organization
Standard library imports first, then third-party (e.g., `rich`), then local modules. Unused imports are commented (see `# import requests` in demo.py).

## Build & Execution
- **Project config**: [pyproject.toml](pyproject.toml) defines metadata and dependencies
- **Run main module**: `python main.py` from project root (generates Person instance, prints to console)
- **Dependencies installation**: `pip install -e .` or `pip install rich>=14.3.1`

## Known Quirks
- **Field naming typo**: `email_adresses` (missing 's') instead of `email_addresses` in Person class—maintain for consistency with existing code
- **Rich integration**: Currently unused (commented import in demo.py)—available for future enhancement of output formatting

## Common Tasks
1. **Add new dataclass fields**: Use `field(default_factory=...)` for mutable types; simple types use `field(default=value)`
2. **Extend Person model**: Add new attributes following existing pattern of name (str), address (str), and optional computed fields (id)
3. **Enhance output**: Leverage `rich` library for colored/formatted console output instead of plain print()
