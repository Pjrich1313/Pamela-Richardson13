#!/usr/bin/env python3
"""
Etherscan v2 API Example Script

This script demonstrates correct usage of the Etherscan v2 API with the required
'chainid' parameter. It includes examples for:
1. Fetching gas prices
2. Fetching token balances
3. Fetching ETH balances

Note: Replace 'YourApiKeyToken' with your actual Etherscan API key.
You can get a free API key from https://etherscan.io/myapikey
"""

import requests
import json
from typing import Dict, Optional


class EtherscanAPI:
    """
    A simple wrapper for Etherscan v2 API calls.
    
    Attributes:
        api_key (str): Your Etherscan API key
        chainid (int): The chain ID (1 for Ethereum mainnet)
        base_url (str): The base URL for Etherscan API
    """
    
    def __init__(self, api_key: str = "YourApiKeyToken", chainid: int = 1):
        """
        Initialize the Etherscan API client.
        
        Args:
            api_key: Your Etherscan API key
            chainid: The chain ID (1 for Ethereum mainnet, 11155111 for Sepolia testnet, etc.)
        """
        self.api_key = api_key
        self.chainid = chainid
        self.base_url = "https://api.etherscan.io/api"
        self.session = requests.Session()
        self.session.params.update({
            "apikey": self.api_key,
            "chainid": self.chainid  # Required for v2 API
        })
        
    def get_gas_prices(self) -> Optional[Dict]:
        """
        Fetch current gas prices using Etherscan v2 API.
        
        The v2 API requires the 'chainid' parameter.
        
        Returns:
            A dictionary containing gas price information, or None if the request fails.
            Expected response structure:
            {
                "status": "1",
                "message": "OK",
                "result": {
                    "LastBlock": "12345678",
                    "SafeGasPrice": "20",
                    "ProposeGasPrice": "22",
                    "FastGasPrice": "24",
                    "suggestBaseFee": "19.5",
                    "gasUsedRatio": "0.5,0.6,0.7"
                }
            }
        """
        params = {
            "module": "gastracker",
            "action": "gasoracle"
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                print("✓ Gas prices fetched successfully")
                return data
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse JSON response: {e}")
            return None
    
    def get_token_balance(self, contract_address: str, wallet_address: str) -> Optional[Dict]:
        """
        Fetch token balance for a specific wallet and contract address.
        
        The v2 API requires the 'chainid' parameter.
        
        Args:
            contract_address: The token contract address
            wallet_address: The wallet address to check
            
        Returns:
            A dictionary containing token balance information, or None if the request fails.
            Expected response structure:
            {
                "status": "1",
                "message": "OK",
                "result": "123456789000000000000"
            }
        """
        params = {
            "module": "account",
            "action": "tokenbalance",
            "contractaddress": contract_address,
            "address": wallet_address,
            "tag": "latest"
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                print("✓ Token balance fetched successfully")
                return data
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse JSON response: {e}")
            return None
    
    def get_eth_balance(self, wallet_address: str) -> Optional[Dict]:
        """
        Fetch ETH balance for a specific wallet address.
        
        The v2 API requires the 'chainid' parameter.
        
        Args:
            wallet_address: The wallet address to check
            
        Returns:
            A dictionary containing ETH balance information, or None if the request fails.
            Expected response structure:
            {
                "status": "1",
                "message": "OK",
                "result": "123456789000000000000"
            }
        """
        params = {
            "module": "account",
            "action": "balance",
            "address": wallet_address,
            "tag": "latest"
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                print("✓ ETH balance fetched successfully")
                return data
            else:
                print(f"✗ API returned error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse JSON response: {e}")
            return None


def format_gas_prices(data: Dict) -> str:
    """
    Format gas price data into a readable string.
    
    Args:
        data: The API response containing gas price information
        
    Returns:
        A formatted string with gas price details
    """
    if not data or "result" not in data:
        return "No gas price data available"
    
    result = data["result"]
    lines = [
        "\n=== Current Gas Prices (Gwei) ===",
        f"Safe Gas Price:    {result.get('SafeGasPrice', 'N/A')} Gwei",
        f"Propose Gas Price: {result.get('ProposeGasPrice', 'N/A')} Gwei",
        f"Fast Gas Price:    {result.get('FastGasPrice', 'N/A')} Gwei",
        f"Last Block:        {result.get('LastBlock', 'N/A')}",
    ]
    
    suggest_base_fee = result.get('suggestBaseFee')
    if suggest_base_fee is not None:
        lines.append(f"Suggested Base Fee: {suggest_base_fee} Gwei")
    
    return "\n".join(lines)


def format_balance(balance_wei: str, decimals: int = 18) -> str:
    """
    Convert balance from wei to a more readable format.
    
    Args:
        balance_wei: The balance in wei as a string
        decimals: Number of decimals for the token (default 18 for ETH)
        
    Returns:
        Formatted balance string
    """
    try:
        balance = int(balance_wei) / (10 ** decimals)
        return f"{balance:.6f}"
    except (ValueError, TypeError):
        return "Invalid balance"


def main():
    """
    Main function demonstrating Etherscan v2 API usage.
    """
    print("=" * 60)
    print("Etherscan v2 API Example - Proper chainid Parameter Usage")
    print("=" * 60)
    
    # Initialize API client with chainid=1 (Ethereum mainnet)
    # IMPORTANT: The chainid parameter is required for v2 API
    api = EtherscanAPI(api_key="YourApiKeyToken", chainid=1)
    
    print(f"\nUsing chainid: {api.chainid} (Ethereum Mainnet)")
    print("\nNote: Replace 'YourApiKeyToken' with your actual API key for real usage.\n")
    
    # Example 1: Fetch gas prices
    print("\n" + "-" * 60)
    print("Example 1: Fetching Gas Prices")
    print("-" * 60)
    gas_data = api.get_gas_prices()
    if gas_data:
        print(format_gas_prices(gas_data))
    
    # Example 2: Fetch token balance
    print("\n" + "-" * 60)
    print("Example 2: Fetching Token Balance")
    print("-" * 60)
    
    # Example addresses (USDT contract and Vitalik's address)
    usdt_contract = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    example_wallet = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    print(f"Contract: {usdt_contract}")
    print(f"Wallet:   {example_wallet}")
    
    token_data = api.get_token_balance(usdt_contract, example_wallet)
    if token_data:
        balance_wei = token_data.get("result", "0")
        # USDT has 6 decimals, not 18
        balance = format_balance(balance_wei, decimals=6)
        print(f"\nToken Balance: {balance} USDT")
    
    # Example 3: Fetch ETH balance
    print("\n" + "-" * 60)
    print("Example 3: Fetching ETH Balance")
    print("-" * 60)
    
    print(f"Wallet: {example_wallet}")
    
    eth_data = api.get_eth_balance(example_wallet)
    if eth_data:
        balance_wei = eth_data.get("result", "0")
        balance = format_balance(balance_wei, decimals=18)
        print(f"\nETH Balance: {balance} ETH")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print("✓ All API calls include the required 'chainid' parameter")
    print("✓ JSON responses are properly parsed and handled")
    print("✓ Error handling is implemented for network and parsing issues")
    print("\nChain IDs Reference:")
    print("  - 1: Ethereum Mainnet")
    print("  - 11155111: Sepolia Testnet")
    print("  Note: Goerli testnet (chainid: 5) has been deprecated")
    print("=" * 60)


if __name__ == "__main__":
    main()
