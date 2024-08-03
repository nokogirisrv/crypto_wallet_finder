# Crypto wallet finder
Crypto Finder is a Python script designed to generate cryptocurrency addresses and check their transaction history across multiple blockchains. This project is for educational purposes only. With this project you can see how strong and secured seed phrase is.

## Features

- Generates Ethereum, Binance Smart Chain, and Bitcoin addresses using mnemonics.
- Checks transaction history for each generated address on:
  - Ethereum using Etherscan API.
  - Binance Smart Chain using BscScan API.
  - Bitcoin using Blockstream API.
- Stores mnemonics and transaction information in JSON files.
- Avoids processing duplicate mnemonics by maintaining a history of processed mnemonics.

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip` package manager

### Required Python Libraries

To run this project, you need to install the following Python libraries:

```bash
pip install requests eth-account mnemonic bip32utils
```

## JSON Files

- data.json: Stores transaction data for addresses with activity.
- processed_mnemonics.json: Tracks mnemonics that have been processed to avoid duplication.

## Important Notes
- This script is for educational purposes and should not be used for malicious activities.
- Ensure you have permission to use any third-party services, such as Etherscan or BscScan, with their respective API keys.

# Troubleshooting
- If you encounter a JSONDecodeError, ensure that your JSON files (data.json and processed_mnemonics.json) are correctly formatted. Initialize them with empty lists [] if they are missing or empty.

## Contributing
- Contributions are welcome! If you have any improvements or suggestions, feel free to submit a pull request or open an issue.


## Acknowledgments
- [Etherscan API](https://etherscan.io/apis)
- [BscScan API](https://bscscan.com/apis)
- [Blockstream API](https://blockstream.info/api/)
