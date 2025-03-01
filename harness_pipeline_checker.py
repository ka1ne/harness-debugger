#!/usr/bin/env python3
"""
Compatibility wrapper for the original harness_pipeline_checker.py script.
This script preserves backward compatibility while using the new modular structure.
"""

import sys
from harness_debugger.cli import main

if __name__ == "__main__":
    sys.exit(main()) 