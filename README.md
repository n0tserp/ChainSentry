# ChainSentry: On-Chain Anomaly Detector (a n0tserp project)

A simple Python tool to monitor Ethereum wallets for suspicious transactions using the Etherscan API. Detects anomalies like large transfers or dust attacks, with easy extensibility for other chains or alerts.

## Features
- Fetches transaction history via public API.
- Analyzes for anomalies using basic thresholds (e.g., >1 ETH transfers, repeated small txns).
- Modular code for adding more detectors (e.g., phishing patterns).
- Secure: Uses .env for API keys.

## Getting Started

### Prerequisites
- Python 3.8+
- Etherscan API key (free: https://etherscan.io/register)
- A wallet address to monitor

### Installation
1. Clone the repo: `git clone https://github.com/yourusername/ChainSentry.git`
2. Navigate: `cd ChainSentry`
3. Create virtual env: `python3 -m venv venv`
4. Activate: `source venv/bin/activate`
5. Install deps: `python3 -m pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and fill in your API key and wallet address.

### Usage
Run: `python chainsentry.py`

Example output:
Monitoring wallet: 0xab5801a7d398351b8be11c439e05c5b3259aec9b
Fetched 100 transactions.
Anomalies detected:

Large transfer detected: 5.0 ETH at 2023-01-01 12:00:00


## Customization
- Edit thresholds in `analyze_anomalies()` (e.g., change large transfer to >0.5 ETH).
- Add email alerts: Integrate smtplib in `main()`.
- Extend to other chains: Add a new function like `fetch_bitcoin_txns()` using Blockcypher API.

## Contributing
Fork and PR! Ideas: Multi-chain support, real-time webhooks, GUI via Tkinter.

## License
MIT License - feel free to use and build on this. n0tserp
