# Etherscan v2 API Integration Guide

This repository demonstrates the correct usage of Etherscan v2 API with the required `chainid` parameter.

## Problem Statement

The Etherscan v2 API requires a `chainid` parameter for all API calls. Without this parameter, you'll encounter errors like:

```
Missing chainid parameter (required for v2 api)
```

## Solution

The `etherscan_api_example.py` script demonstrates how to properly make API calls with the `chainid` parameter included.

## Prerequisites

```bash
pip install requests
```

## Usage

1. Get your API key from [Etherscan](https://etherscan.io/myapikey)

2. Replace `'YourApiKeyToken'` in the script with your actual API key:
   ```python
   api = EtherscanAPI(api_key="YOUR_ACTUAL_API_KEY", chainid=1)
   ```

3. Run the script:
   ```bash
   python3 etherscan_api_example.py
   ```

## Key Features

### 1. Gas Price Fetching
Fetches current gas prices with proper `chainid` parameter:
```python
params = {
    "module": "gastracker",
    "action": "gasoracle",
    "apikey": self.api_key,
    "chainid": self.chainid  # Required for v2 API
}
```

### 2. Token Balance Checking
Fetches ERC-20 token balances with proper `chainid` parameter:
```python
params = {
    "module": "account",
    "action": "tokenbalance",
    "contractaddress": contract_address,
    "address": wallet_address,
    "tag": "latest",
    "apikey": self.api_key,
    "chainid": self.chainid  # Required for v2 API
}
```

### 3. ETH Balance Checking
Fetches ETH balances with proper `chainid` parameter:
```python
params = {
    "module": "account",
    "action": "balance",
    "address": wallet_address,
    "tag": "latest",
    "apikey": self.api_key,
    "chainid": self.chainid  # Required for v2 API
}
```

## Chain ID Reference

- **1**: Ethereum Mainnet
- **5**: Goerli Testnet (deprecated)
- **11155111**: Sepolia Testnet
- **137**: Polygon Mainnet
- **80001**: Polygon Mumbai Testnet

## JSON Response Handling

The script includes proper JSON response parsing and error handling:

```python
try:
    response = requests.get(self.base_url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if data.get("status") == "1":
        print("✓ Request successful")
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
```

## Example Output

```
============================================================
Etherscan v2 API Example - Proper chainid Parameter Usage
============================================================

Using chainid: 1 (Ethereum Mainnet)

------------------------------------------------------------
Example 1: Fetching Gas Prices
------------------------------------------------------------
✓ Gas prices fetched successfully

=== Current Gas Prices (Gwei) ===
Safe Gas Price:    20 Gwei
Propose Gas Price: 22 Gwei
Fast Gas Price:    24 Gwei
Last Block:        12345678
Suggested Base Fee: 19.5 Gwei

------------------------------------------------------------
Example 2: Fetching Token Balance
------------------------------------------------------------
✓ Token balance fetched successfully

Token Balance: 123.456789 USDT

------------------------------------------------------------
Example 3: Fetching ETH Balance
------------------------------------------------------------
✓ ETH balance fetched successfully

ETH Balance: 1.234567 ETH

============================================================
Summary:
============================================================
✓ All API calls include the required 'chainid' parameter
✓ JSON responses are properly parsed and handled
✓ Error handling is implemented for network and parsing issues
============================================================
```

## Important Notes

1. **Always include `chainid` parameter**: This is mandatory for Etherscan v2 API
2. **Use the correct chain ID**: Make sure to use the appropriate chain ID for your network
3. **Handle JSON responses**: Always check the `status` field in the response
4. **Error handling**: Implement proper error handling for network and parsing issues
5. **API key**: Replace the placeholder API key with your actual key for production use

## Additional Resources

- [Etherscan API Documentation](https://docs.etherscan.io/)
- [Etherscan API Keys](https://etherscan.io/myapikey)
- [EIP-155: Chain ID Specification](https://eips.ethereum.org/EIPS/eip-155)
