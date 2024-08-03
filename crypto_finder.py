import requests
from eth_account import Account
import json
from mnemonic import Mnemonic
import bip32utils

def append_to_json(file_path, data):
    """Appends new data to a JSON file."""
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


# Constants for file paths and API keys
DATA_FILE_PATH = 'DATA_FILE_PATH'
PROCESSED_MNEMONICS_FILE_PATH = 'PROCESSED_MNEMONICS_FILE_PATH'
ETHERSCAN_API_KEY = 'ETHERSCAN_API_KEY'
BSCSCAN_API_KEY = 'BSCSCAN_API_KEY'


def check_transactions(address, api_key):
    """Checks Ethereum transactions for a given address."""
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['status'] == '1' and data['message'] == 'OK' and len(data['result']) > 0:
            print(f"The address '{address}' has transactions.")
            new_data = {"phrase": phrase, "address": address, "chain": "ETH"}
            append_to_json(DATA_FILE_PATH, new_data)
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving Ethereum transactions: {e}")


def check_bsc_transactions(address, api_key):
    """Checks BSC transactions for a given address."""
    url = f"https://api.bscscan.com/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "1" and len(data["result"]) > 0:
            print(f"The address {address} has transactions.")
            new_data = {"phrase": phrase, "address": address, "chain": "BSC"}
            append_to_json(DATA_FILE_PATH, new_data)
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving BSC transactions: {e}")


def btc_address(phrase):
    """Generates a Bitcoin address from a mnemonic phrase."""
    mnemon = Mnemonic('english')
    seed = mnemon.to_seed(phrase)

    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    child_key = root_key.ChildKey(0).ChildKey(0)
    return child_key.Address()


def check_btc_transactions(address):
    """Checks Bitcoin transactions for a given address."""
    url = f"https://blockstream.info/api/address/{address}/txs"

    try:
        response = requests.get(url)
        response.raise_for_status()
        transactions = response.json()

        if transactions:
            print(f"The address {address} has transactions.")
            new_data = {"phrase": phrase, "address": address, "chain": "BTC"}
            append_to_json(DATA_FILE_PATH, new_data)
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving Bitcoin transactions: {e}")


# Load already processed mnemonics from the JSON file
try:
    with open(PROCESSED_MNEMONICS_FILE_PATH, 'r') as json_file:
        processed_mnemonics = set(json.load(json_file))
except FileNotFoundError:
    processed_mnemonics = set()

# Loop for generating addresses and checking transactions
for i in range(100000):
    print("Loop iteration:", i)
    Account.enable_unaudited_hdwallet_features()
    acct, mnemonic = Account.create_with_mnemonic(num_words=24)
    address = acct.address
    phrase = mnemonic

    # Check if the mnemonic has already been processed
    if phrase in processed_mnemonics:
        print("Mnemonic already processed, skipping.")
        continue

    # Add the mnemonic to the processed set
    processed_mnemonics.add(phrase)

    # Save the updated set of processed mnemonics to the JSON file
    with open(PROCESSED_MNEMONICS_FILE_PATH, 'w') as json_file:
        json.dump(list(processed_mnemonics), json_file, indent=4)

    # Check transactions for the address
    check_transactions(address, ETHERSCAN_API_KEY)
    check_bsc_transactions(address, BSCSCAN_API_KEY)
    address_btc = btc_address(phrase)
    check_btc_transactions(address_btc)
