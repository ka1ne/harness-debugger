# Migration from harness_pipeline_checker.py

The functionality of `harness_pipeline_checker.py` has been refactored into a proper Python package 
structure in the `harness_debugger` directory.

## Why We Refactored

- **Maintainability**: Smaller, focused modules are easier to maintain
- **Extensibility**: New features can be added without making one file enormous
- **Testability**: Modular code is easier to test
- **Installation**: Package can be installed via pip

## How to Migrate

If you were previously running: 