"""Pipeline-related commands for the Harness Debugger CLI tool."""

import json
import time
from colorama import Fore
from datetime import datetime, timedelta

from harness_debugger.utils.constants import *
from harness_debugger.utils.formatting import format_delegate_info

def check_pipeline(args, client):
    """Check for failed runs in a specific pipeline stage."""
    if not args.pipeline:
        print(f"{EMOJI_ERROR}{Fore.RED}Error: Pipeline ID is required")
        return 1
        
    if not args.stage:
        print(f"{EMOJI_ERROR}{Fore.RED}Error: Stage name is required")
        return 1
        
    pipeline_id = args.pipeline
    stage_name = args.stage
    days = args.days
    
    print(f"{EMOJI_INFO}{Fore.CYAN}Checking for failures in pipeline {Fore.YELLOW}{pipeline_id}{Fore.CYAN}, stage {Fore.YELLOW}{stage_name}{Fore.CYAN} in the last {Fore.YELLOW}{days}{Fore.CYAN} days...")
    
    failed_runs = client.get_failed_runs(stage_name, pipeline_id, days)
    
    if not failed_runs:
        print(f"{EMOJI_SUCCESS}{Fore.GREEN}No failed runs found for this stage in the specified time period.")
        return 0
        
    if args.output == 'json':
        print(json.dumps(failed_runs, indent=2))
        return 0
        
    print(f"\n{EMOJI_ERROR}{Fore.RED}Found {Fore.YELLOW}{len(failed_runs)}{Fore.RED} failed runs for stage {Fore.YELLOW}{stage_name}{Fore.RED}:")
    
    # Display each failed run with delegate information
    for run in failed_runs:
        print("\n" + "=" * 80)
        print(f"{EMOJI_PIPELINE}{Fore.CYAN}Execution ID: {Fore.WHITE}{run['execution_id']}")
        print(f"{EMOJI_TIME}{Fore.CYAN}Start Time: {Fore.WHITE}{run['start_time']}")
        print(f"{EMOJI_ERROR}{Fore.CYAN}Status: {Fore.RED}{run['status']}")
        print(f"{EMOJI_ERROR}{Fore.CYAN}Failure Message: {Fore.WHITE}{run['failure_message']}")
        
        # Print delegate information
        if run.get('delegates'):
            print(f"\n{EMOJI_DELEGATE}{Fore.CYAN}DELEGATE INFORMATION:")
            for d_info in run['delegates']:
                delegate = d_info.get('delegate_info', {})
                
                print(f"  {Fore.YELLOW}Step: {Fore.WHITE}{d_info.get('step_name')}")
                print(format_delegate_info(delegate))
                
                if d_info.get('step_status') == 'FAILED':
                    print(f"  {EMOJI_ERROR}{Fore.YELLOW}Step Error: {Fore.RED}{d_info.get('error_message')}")
                print()
        else:
            print(f"  {EMOJI_WARNING}{Fore.YELLOW}No delegate information available")
            
        print("-" * 80)
    
    # Set output variables for Harness if running in pipeline
    output_file = args.output_file or os.environ.get("HARNESS_OUTPUT_PATH", "output.txt")
    with open(output_file, "w") as f:
        f.write(f"FAILED_RUNS_COUNT={len(failed_runs)}\n")
        f.write(f"LAST_FAILED_RUN_ID={failed_runs[0]['execution_id']}\n")
        f.write(f"LAST_FAILED_TIME={failed_runs[0]['start_time']}\n")
        
        # Add delegate information to output
        if failed_runs[0].get('delegates'):
            delegates_used = ','.join([d.get('delegate_info', {}).get('name', 'Unknown') 
                                    for d in failed_runs[0].get('delegates', [])])
            f.write(f"DELEGATES_USED={delegates_used}\n")
            
            # Add labels from the delegates
            all_labels = []
            for d_info in failed_runs[0].get('delegates', []):
                all_labels.extend(d_info.get('delegate_info', {}).get('labels', []))
            
            if all_labels:
                unique_labels = ','.join(set(all_labels))
                f.write(f"DELEGATE_LABELS={unique_labels}\n")
                
    return 0

# Add other pipeline command functions here... 