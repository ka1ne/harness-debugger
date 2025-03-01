"""Formatting utilities for CLI output."""

import json
from datetime import datetime
from colorama import Fore, Style
import tabulate

from harness_debugger.utils.constants import *

def print_welcome():
    """Print welcome message for the CLI tool."""
    print(f"\n{Style.BRIGHT}{Fore.CYAN}{'=' * 60}")
    print(f"{EMOJI_INFO} {Fore.WHITE}Harness Debugger - Pipeline & Delegate Troubleshooting Tool")
    print(f"{Style.BRIGHT}{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

def format_connector_table(connectors):
    """Format connectors as a table."""
    table_data = []
    for connector in connectors:
        created_by = connector.get("createdBy", {}).get("name", "Unknown")
        created_at = datetime.fromtimestamp(int(connector.get("createdAt", 0)) / 1000).strftime("%Y-%m-%d %H:%M:%S") if connector.get("createdAt") else "Unknown"
        
        table_data.append([
            connector.get("name", "Unknown"),
            connector.get("id", "Unknown"),
            connector.get("connectorType", "Unknown"),
            ", ".join(connector.get("delegateSelectors", [])) or "None",
            created_by,
            created_at
        ])
    
    headers = ["Name", "ID", "Type", "Delegate Selectors", "Created By", "Created At"]
    return tabulate.tabulate(table_data, headers=headers, tablefmt="pretty")

def format_delegate_info(delegate):
    """Format delegate information for display."""
    status = delegate.get('status')
    status_color = Fore.GREEN if status == 'ENABLED' else Fore.RED
    
    output = [
        f"  {Fore.YELLOW}Delegate Name: {Fore.WHITE}{delegate.get('name')}",
        f"  {Fore.YELLOW}Delegate ID: {Fore.WHITE}{delegate.get('id')}",
        f"  {Fore.YELLOW}Hostname: {Fore.WHITE}{delegate.get('hostname')}",
        f"  {Fore.YELLOW}IP: {Fore.WHITE}{delegate.get('ip')}",
        f"  {Fore.YELLOW}Status: {status_color}{status}",
        f"  {Fore.YELLOW}Version: {Fore.WHITE}{delegate.get('version')}",
        f"  {Fore.YELLOW}Profile: {Fore.WHITE}{delegate.get('profile')}",
        f"  {EMOJI_TIME}{Fore.YELLOW}Last Heartbeat: {Fore.WHITE}{delegate.get('last_heartbeat')}"
    ]
    
    # Add labels
    labels = delegate.get('labels', [])
    if labels:
        output.append(f"  {EMOJI_LABEL}{Fore.YELLOW}Labels:")
        for label in labels:
            output.append(f"    {Fore.WHITE}- {label}")
    else:
        output.append(f"  {EMOJI_LABEL}{Fore.YELLOW}Labels: {Fore.RED}None")
    
    return "\n".join(output) 