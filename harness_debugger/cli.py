"""Command-line interface for the Harness Debugger tool."""

import argparse
import sys
import os
from colorama import init, Fore, Style
from dotenv import load_dotenv

from harness_debugger.client import HarnessClient
from harness_debugger.utils.constants import *
from harness_debugger.utils.formatting import print_welcome
from harness_debugger.commands import delegate, connector, pipeline

# Load .env file if it exists
load_dotenv()

# Initialize colorama
init(autoreset=True)

class HarnessDebuggerCLI:
    def __init__(self):
        self.parser = self._create_parser()
        
    def _create_parser(self):
        """Create command line argument parser"""
        parser = argparse.ArgumentParser(
            description=f"{EMOJI_INFO} Harness Platform Debugging Utility",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
{Fore.CYAN}Examples:{Style.RESET_ALL}
  List all delegates:
    {Fore.GREEN}harness-debugger delegate list{Style.RESET_ALL}
    
  Get details for a specific delegate:
    {Fore.GREEN}harness-debugger delegate info DELEGATE_ID{Style.RESET_ALL}
    
  Check for delegate usage in failed pipeline stages:
    {Fore.GREEN}harness-debugger delegate check-pipeline --pipeline=PIPELINE_ID --stage=STAGE_NAME{Style.RESET_ALL}
    
  Check for pipeline failures:
    {Fore.GREEN}harness-debugger pipeline check --pipeline=PIPELINE_ID --stage=STAGE_NAME{Style.RESET_ALL}
"""
        )
        
        # Global arguments
        parser.add_argument('--api-key', help='Harness API key (defaults to HARNESS_API_KEY env var)')
        parser.add_argument('--account', help='Harness account ID (defaults to HARNESS_ACCOUNT_ID env var)')
        parser.add_argument('--org', help='Harness organization ID (defaults to HARNESS_ORG_ID env var)')
        parser.add_argument('--project', help='Harness project ID (defaults to HARNESS_PROJECT_ID env var)')
        parser.add_argument('--output', choices=['text', 'json'], default='text', 
                         help='Output format (text or json)')
        
        # Create subparsers for main commands
        subparsers = parser.add_subparsers(dest='command')
        
        # Delegate commands
        delegate_parser = subparsers.add_parser('delegate', help='Delegate-related commands')
        delegate_subparsers = delegate_parser.add_subparsers(dest='subcommand')
        
        # List delegates
        list_parser = delegate_subparsers.add_parser('list', help='List all delegates')
        
        # Get delegate info
        info_parser = delegate_subparsers.add_parser('info', help='Get detailed information about a delegate')
        info_parser.add_argument('delegate_id', help='Delegate ID')
        
        # Test delegate connectivity
        conn_parser = delegate_subparsers.add_parser('test-connectivity', 
                                                 help='Generate commands to test delegate connectivity')
        conn_parser.add_argument('delegate_id', help='Delegate ID')
        conn_parser.add_argument('--urls', nargs='+', help='URLs to test (defaults to common services)')
        
        # Check delegate usage in pipeline
        check_pipeline_parser = delegate_subparsers.add_parser('check-pipeline', 
                                                          help='Check delegate usage in failed pipeline stages')
        check_pipeline_parser.add_argument('--pipeline', required=True, help='Pipeline ID')
        check_pipeline_parser.add_argument('--stage', required=True, help='Stage name')
        check_pipeline_parser.add_argument('--days', type=int, default=7, 
                                        help='Number of days to look back (default: 7)')
        check_pipeline_parser.add_argument('--output-file', help='Path to write output variables')
        
        # Pipeline commands
        pipeline_parser = subparsers.add_parser('pipeline', help='Pipeline-related commands')
        pipeline_subparsers = pipeline_parser.add_subparsers(dest='subcommand')
        
        # Check pipeline failures
        pipeline_check_parser = pipeline_subparsers.add_parser('check', 
                                                          help='Check for pipeline failures')
        pipeline_check_parser.add_argument('--pipeline', required=True, help='Pipeline ID')
        pipeline_check_parser.add_argument('--stage', required=True, help='Stage name')
        pipeline_check_parser.add_argument('--days', type=int, default=7, 
                                        help='Number of days to look back (default: 7)')
        pipeline_check_parser.add_argument('--output-file', help='Path to write output variables')
        
        # Connector commands
        connector_parser = subparsers.add_parser('connector', help='Connector-related commands')
        connector_subparsers = connector_parser.add_subparsers(dest='subcommand')
        
        # List connectors
        connector_list_parser = connector_subparsers.add_parser('list', help='List all connectors')
        
        # Find connectors by delegate
        connector_by_delegate_parser = connector_subparsers.add_parser('by-delegate', 
                                                                  help='Find connectors using a specific delegate selector')
        connector_by_delegate_parser.add_argument('selector', help='Delegate selector')
        
        return parser
    
    def run(self):
        """Parse arguments and execute appropriate command"""
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return 1
            
        # Create client with provided credentials
        client = HarnessClient(
            api_key=args.api_key,
            account_id=args.account,
            org_id=args.org,
            project_id=args.project
        )
        
        if args.command == 'delegate':
            return self._handle_delegate_command(args, client)
        elif args.command == 'pipeline':
            return self._handle_pipeline_command(args, client)
        elif args.command == 'connector':
            return self._handle_connector_command(args, client)
        else:
            print(f"{EMOJI_ERROR}{Fore.RED}Unknown command: {args.command}")
            return 1
    
    def _handle_delegate_command(self, args, client):
        """Handle delegate-related commands"""
        if not args.subcommand:
            print(f"{EMOJI_ERROR}{Fore.RED}Error: No delegate subcommand specified")
            return 1
            
        if args.subcommand == 'list':
            return delegate.list_delegates(args, client)
        elif args.subcommand == 'info':
            return delegate.show_delegate_info(args, client)
        elif args.subcommand == 'check-pipeline':
            return pipeline.check_pipeline(args, client)
        elif args.subcommand == 'test-connectivity':
            return delegate.test_connectivity(args, client)
            
        return 0
    
    def _handle_pipeline_command(self, args, client):
        """Handle pipeline-related commands"""
        if not args.subcommand:
            print(f"{EMOJI_ERROR}{Fore.RED}Error: No pipeline subcommand specified")
            return 1
            
        if args.subcommand == 'check':
            return pipeline.check_pipeline(args, client)
            
        return 0
        
    def _handle_connector_command(self, args, client):
        """Handle connector-related commands"""
        if not args.subcommand:
            print(f"{EMOJI_ERROR}{Fore.RED}Error: No connector subcommand specified")
            return 1
        
        if args.subcommand == 'list':
            return connector.list_connectors(args, client)
        elif args.subcommand == 'by-delegate':
            return connector.find_by_delegate(args, client)
        
        return 0

def main():
    """Main entry point for the CLI."""
    print_welcome()
    cli = HarnessDebuggerCLI()
    return cli.run()

if __name__ == "__main__":
    sys.exit(main()) 