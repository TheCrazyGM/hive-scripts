#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "python-dotenv",
# ]
# ///

import os

from nectar.account import Account
from nectar.hive import Hive
from nectar.wallet import Wallet


def remove_account_authorizations(account):
    """Remove all account authorizations for active and posting keys."""
    for key_type in ["active", "posting"]:
        for auth in account[key_type]["account_auths"]:
            print(f"Removing authorization for {auth[0]}")
            account.disallow(auth[0])


def main():
    # Retrieve WIF keys from environment variables
    try:
        posting_wif = os.environ["POSTING_WIF"]
        active_wif = os.environ["ACTIVE_WIF"]
    except KeyError:
        print("Error: Missing WIF keys in environment variables")
        return

    # Initialize Hive blockchain instance
    hive = Hive(nodes="https://api.hive.blog", keys=[posting_wif, active_wif])

    # Get account details
    wallet = Wallet(blockchain_instance=hive)
    author = wallet.getAccountFromPrivateKey(active_wif)
    account = Account(author, blockchain_instance=hive)

    # Remove account authorizations
    remove_account_authorizations(account)


if __name__ == "__main__":
    main()
