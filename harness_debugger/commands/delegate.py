"""Delegate-related commands for the Harness Debugger CLI tool."""

import json
from colorama import Fore
from tabulate import tabulate

from harness_debugger.utils.constants import *
from harness_debugger.utils.formatting import format_delegate_info

def list_delegates(args, client):
    """List all delegates in the account."""
    delegates = client.get_all_delegates()
    
    if not delegates:
        print(f"{EMOJI_WARNING}{Fore.YELLOW}No delegates found")
        return 0
        
    if args.output == 'json':
        print(json.dumps(delegates, indent=2))
        return 0
        
    print(f"\n{EMOJI_INFO}{Fore.CYAN}Found {Fore.YELLOW}{len(delegates)}{Fore.CYAN} delegates:")
    
    # Create a table for better display
    table_data = []
    for delegate_id, delegate in delegates.items():
        status = delegate.get('status')
        status_color = Fore.GREEN if status == 'ENABLED' else Fore.RED
        
        table_data.append([
            delegate.get('name'),
            delegate_id,
            delegate.get('hostname'),
            delegate.get('ip'),
            f"{status_color}{status}{Fore.RESET}",
            delegate.get('version'),
            ", ".join(delegate.get('labels', [])) or "None"
        ])
    
    headers = ["Name", "ID", "Hostname", "IP", "Status", "Version", "Labels"]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    
    return 0

def show_delegate_info(args, client):
    """Show detailed information about a specific delegate."""
    delegate_id = args.delegate_id
    delegate = client.get_delegate_info(delegate_id)
    
    if not delegate:
        print(f"{EMOJI_ERROR}{Fore.RED}Could not find delegate with ID: {delegate_id}")
        return 1
        
    if args.output == 'json':
        print(json.dumps(delegate, indent=2))
        return 0
        
    print(f"\n{EMOJI_DELEGATE}{Fore.CYAN}Delegate Information:")
    print(format_delegate_info(delegate))
    
    return 0

def test_connectivity(args, client):
    """Generate connectivity test commands for a delegate."""
    delegate_id = args.delegate_id
    urls = args.urls
    
    if urls:
        urls = [url if url.startswith(('http://', 'https://')) else f"https://{url}" for url in urls]
    
    results = client.test_delegate_connectivity(delegate_id, urls)
    
    if not results:
        print(f"{EMOJI_ERROR}{Fore.RED}Failed to get delegate information")
        return 1
        
    delegate_info = results.get("delegate", {})
    connectivity_tests = results.get("connectivity_tests", {})
    
    if not connectivity_tests:
        print(f"{EMOJI_WARNING}{Fore.YELLOW}No connectivity tests generated")
        return 0
        
    print(f"\n{EMOJI_DELEGATE}{Fore.CYAN}Delegate: {Fore.WHITE}{delegate_info.get('name')} ({delegate_info.get('id')})")
    print(f"{Fore.CYAN}Hostname: {Fore.WHITE}{delegate_info.get('hostname')}")
    print(f"{Fore.CYAN}IP: {Fore.WHITE}{delegate_info.get('ip')}")
    
    print(f"\n{EMOJI_NETWORK}{Fore.CYAN}Connectivity Test Commands")
    print(f"{Fore.YELLOW}Run these commands on the delegate machine to test connectivity:")
    print(f"{Fore.YELLOW}--------------------------------------------------------------")
    
    for url, test_info in connectivity_tests.items():
        hostname = test_info.get("hostname")
        port = test_info.get("port")
        command = test_info.get("command")
        
        print(f"\n{Fore.CYAN}Test URL: {Fore.WHITE}{url}")
        print(f"{Fore.CYAN}Hostname: {Fore.WHITE}{hostname}")
        print(f"{Fore.CYAN}Port: {Fore.WHITE}{port}")
        print(f"{Fore.GREEN}Network test: {Fore.WHITE}nc -zv {hostname} {port}")
        print(f"{Fore.GREEN}HTTP test: {Fore.WHITE}{command}")
    
    print(f"\n{EMOJI_INFO}{Fore.CYAN}Instructions:")
    print(f"{Fore.WHITE}1. SSH into the delegate machine")
    print(f"{Fore.WHITE}2. Run the above commands to test connectivity")
    print(f"{Fore.WHITE}3. For network tests, look for 'Connection to [host] [port] succeeded!'")
    print(f"{Fore.WHITE}4. For HTTP tests, a response code of 200 indicates success")
    
    return 0

# Add other delegate command functions here... 