"""Connector-related commands for the Harness Debugger CLI tool."""

import json
from colorama import Fore
from datetime import datetime
from tabulate import tabulate

from harness_debugger.utils.constants import *
from harness_debugger.utils.formatting import format_connector_table

def list_connectors(args, client):
    """List all connectors in the account."""
    connectors = client.get_connectors()
    
    if not connectors:
        print(f"{EMOJI_WARNING}{Fore.YELLOW}No connectors found")
        return 0
    
    if args.output == 'json':
        print(json.dumps(connectors, indent=2))
    else:
        print(f"\n{EMOJI_INFO}{Fore.CYAN}Found {Fore.YELLOW}{len(connectors)}{Fore.CYAN} connectors:")
        print(format_connector_table(connectors))
    
    return 0

def find_by_delegate(args, client):
    """Find connectors using a specific delegate selector."""
    selector = args.selector
    connectors = client.get_connectors(selector)
    
    if not connectors:
        print(f"{EMOJI_WARNING}{Fore.YELLOW}No connectors found using delegate selector '{selector}'")
        return 0
    
    if args.output == 'json':
        print(json.dumps(connectors, indent=2))
    else:
        print(f"\n{EMOJI_INFO}{Fore.CYAN}Found {Fore.YELLOW}{len(connectors)}{Fore.CYAN} connectors using delegate selector '{Fore.YELLOW}{selector}{Fore.CYAN}':")
        print(format_connector_table(connectors))
    
    return 0

# Add other connector command functions here... 