import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# === 1. LOAD .env (your secrets) ===
load_dotenv()

# === 2. GET API KEY & WALLET FROM .env ===
API_KEY = os.getenv('ETHERSCAN_API_KEY')
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')

# === 3. ETHERSCAN V2 API URL (MIGRATED & MULTI-CHAIN READY) ===
BASE_URL = 'https://api.etherscan.io/v2/api'  # V2 base: Unified for 60+ chains

# === 4. FETCH TRANSACTIONS (V2: account module + chainid) ===
def fetch_transactions(address, api_key):
    params = {
        'module': 'account',   # Same as V1 (V2-compatible)
        'action': 'txlist',    # Transaction list (unchanged)
        'address': address,
        'chainid': 1,          # V2 required: 1=Ethereum mainnet (extensible!)
        'page': 1,
        'offset': 100,         # Free tier max
        'sort': 'desc',        # Newest first
        'apikey': api_key
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"Raw API Response: {data}")  # DEBUG: Confirms V2 success

        if data['status'] == '1':
            print(f"SUCCESS: Fetched {len(data['result'])} transactions")
            return data['result']
        else:
            error = data.get('message', 'Unknown')
            result = data.get('result', 'No details')
            print(f"API ERROR: {error} | Result: {result}")
            if 'Invalid API Key' in result:
                print("   → Key issue. Check .env or wait 15 mins after creation.")
            elif 'rate status' in result:
                print("   → Rate limited. Wait 30 secs.")
            elif 'No transactions found' in result:
                print("   → Wallet inactive. Try 0x1db3439a222c519ab44bb1144fc28167b4fa6ee6.")
            return []
    except Exception as e:
        print(f"REQUEST FAILED: {e}")
        return []

# === 5. ANALYZE FOR ANOMALIES ===
def analyze_anomalies(transactions):
    if not transactions:
        return []

    df = pd.DataFrame(transactions)
    df['value_eth'] = pd.to_numeric(df['value']) / 10**18
    df['time'] = pd.to_numeric(df['timeStamp']).apply(datetime.fromtimestamp)

    anomalies = []

    # Large transfers (> 1 ETH)
    large_txns = df[df['value_eth'] > 1]
    for _, row in large_txns.iterrows():
        anomalies.append(f"LARGE: {row['value_eth']:.2f} ETH → {row['time'].strftime('%Y-%m-%d %H:%M')}")

    # Dust attack (many tiny txns in one hour)
    small = df[df['value_eth'] < 0.001]
    hourly = small.groupby(small['time'].dt.hour).size()
    for hour, count in hourly[hourly > 5].items():
        anomalies.append(f"DUST: {count} tiny txns in hour {hour}")

    return anomalies

# === 6. MAIN FUNCTION ===
def main():
    print("=== ChainSentry: On-Chain Anomaly Detector (V2 Migrated) ===\n")

    if not API_KEY:
        print("ERROR: ETHERSCAN_API_KEY missing in .env")
        return
    if not WALLET_ADDRESS:
        print("ERROR: WALLET_ADDRESS missing in .env")
        return

    print(f"Wallet: {WALLET_ADDRESS}")
    print(f"API Key: {API_KEY[:6]}... (hidden)\n")

    txns = fetch_transactions(WALLET_ADDRESS, API_KEY)

    if txns:
        print(f"\nAnalyzing {len(txns)} transactions...\n")
        flags = analyze_anomalies(txns)
        if flags:
            print("ANOMALIES DETECTED:")
            for f in flags:
                print(f"  • {f}")
        else:
            print("No anomalies found. Wallet looks clean.")
    else:
        print("No data to analyze.")

    print("\nDone.")

# === 7. RUN ===
if __name__ == "__main__":
    main()