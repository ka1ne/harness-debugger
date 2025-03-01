#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env

from harness_debugger.cli import main

if __name__ == "__main__":
    main() 