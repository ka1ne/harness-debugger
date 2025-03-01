"""Harness API client for making requests to the Harness platform."""

import os
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from tqdm import tqdm
from colorama import Fore
from urllib.parse import urlparse

from harness_debugger.utils.constants import *

class HarnessClient:
    def __init__(self, api_key=None, account_id=None, org_id=None, project_id=None):
        # Try to get from env vars if not provided
        self.api_key = api_key or os.environ.get("HARNESS_API_KEY")
        self.account_id = account_id or os.environ.get("HARNESS_ACCOUNT_ID")
        self.org_id = org_id or os.environ.get("HARNESS_ORG_ID", "")
        self.project_id = project_id or os.environ.get("HARNESS_PROJECT_ID", "")
        
        if not self.api_key or not self.account_id:
            raise ValueError("API key and Account ID are required. Provide them as arguments or set HARNESS_API_KEY and HARNESS_ACCOUNT_ID environment variables.")
        
        self.base_url = "https://app.harness.io/gateway/pipeline/api"
        self.delegate_url = "https://app.harness.io/gateway/ng/api/delegate-service/delegates"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def get_delegate_info(self, delegate_id: str) -> Dict:
        """
        Get information about a specific delegate
        
        Args:
            delegate_id (str): The ID of the delegate
            
        Returns:
            Dict: Delegate information including labels and status
        """
        try:
            params = {
                "accountIdentifier": self.account_id,
            }
            
            response = requests.get(
                f"{self.delegate_url}/{delegate_id}",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "SUCCESS":
                print(f"{EMOJI_ERROR}{Fore.RED}Error getting delegate info: {data.get('message')}")
                return {}
                
            delegate_data = data.get("data", {})
            return {
                "id": delegate_data.get("uuid", "Unknown"),
                "name": delegate_data.get("name", "Unknown"),
                "hostname": delegate_data.get("hostName", "Unknown"),
                "ip": delegate_data.get("ip", "Unknown"),
                "status": delegate_data.get("status", "Unknown"),
                "version": delegate_data.get("version", "Unknown"),
                "labels": delegate_data.get("selectors", []),
                "last_heartbeat": datetime.fromtimestamp(int(delegate_data.get("lastHeartBeat", 0)) / 1000).strftime("%Y-%m-%d %H:%M:%S") if delegate_data.get("lastHeartBeat") else "Unknown",
                "connected_at": datetime.fromtimestamp(int(delegate_data.get("connectedAt", 0)) / 1000).strftime("%Y-%m-%d %H:%M:%S") if delegate_data.get("connectedAt") else "Unknown",
                "profile": delegate_data.get("delegateProfileId", "None")
            }
        except requests.exceptions.RequestException as e:
            print(f"{EMOJI_ERROR}{Fore.RED}Error making API request for delegate info: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"{Fore.RED}Response text: {e.response.text}")
            return {}

    def get_all_delegates(self) -> Dict[str, Dict]:
        """
        Get information about all delegates in the account
        
        Returns:
            Dict[str, Dict]: Map of delegate ID to delegate information
        """
        try:
            params = {
                "accountIdentifier": self.account_id,
                "pageIndex": 0,
                "pageSize": 100
            }
            
            print(f"{EMOJI_INFO}{Fore.CYAN}Fetching delegates information...")
            response = requests.get(
                self.delegate_url,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "SUCCESS":
                print(f"{EMOJI_ERROR}{Fore.RED}Error getting delegates: {data.get('message')}")
                return {}
                
            delegates = {}
            delegate_list = data.get("data", {}).get("content", [])
            
            for delegate in tqdm(delegate_list, desc="Processing delegates", unit="delegate"):
                delegate_id = delegate.get("uuid")
                if delegate_id:
                    delegates[delegate_id] = {
                        "id": delegate_id,
                        "name": delegate.get("name", "Unknown"),
                        "hostname": delegate.get("hostName", "Unknown"),
                        "ip": delegate.get("ip", "Unknown"),
                        "status": delegate.get("status", "Unknown"),
                        "version": delegate.get("version", "Unknown"),
                        "labels": delegate.get("selectors", []),
                        "last_heartbeat": datetime.fromtimestamp(int(delegate.get("lastHeartBeat", 0)) / 1000).strftime("%Y-%m-%d %H:%M:%S") if delegate.get("lastHeartBeat") else "Unknown",
                        "connected_at": datetime.fromtimestamp(int(delegate.get("connectedAt", 0)) / 1000).strftime("%Y-%m-%d %H:%M:%S") if delegate.get("connectedAt") else "Unknown",
                        "profile": delegate.get("delegateProfileId", "None")
                    }
            
            return delegates
        except requests.exceptions.RequestException as e:
            print(f"{EMOJI_ERROR}{Fore.RED}Error making API request for delegates: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"{Fore.RED}Response text: {e.response.text}")
            return {}
    
    # Add other methods from original HarnessClient here...
    # (get_step_delegate_info, get_failed_runs, get_connectors, test_delegate_connectivity) 