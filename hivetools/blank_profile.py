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
from dotenv import load_dotenv

PROFILE = {}


def get_profile(active_wif, posting_wif):
    try:
        hive_instance = Hive(
            keys=[posting_wif, active_wif], nodes=["https://api.hive.blog"]
        )
        wallet = Wallet(blockchain_instance=hive_instance)
        account_name = wallet.getAccountFromPrivateKey(active_wif)
        account = Account(account_name, blockchain_instance=hive_instance)
        return account_name, account
    except Exception as e:
        print(f"Error getting profile: {e}")
        return None, None


def update_profile(account_name, account):
    try:
        result_json = account.update_account_jsonmetadata(PROFILE, account=account_name)
        result_metadata = account.update_account_metadata(PROFILE, account=account_name)
        print("Update JSON Metadata Result:", result_json)
        print("Update Account Metadata Result:", result_metadata)
    except Exception as e:
        print(f"Error updating profile: {e}")


def main():
    load_dotenv()
    # Ensure environment variables are set
    active_wif = os.getenv("ACTIVE_WIF")
    posting_wif = os.getenv("POSTING_WIF")

    if not active_wif or not posting_wif:
        print("ERROR: Missing environment variables for ACTIVE_WIF or POSTING_WIF.")
        return
    print("WARNING: This will update your profile to be blank.")
    user_input = input("Press 'y' to continue or any other key to abort: ")
    if user_input.lower() != "y":
        print("Operation aborted.")
        return
    account_name, account = get_profile(active_wif, posting_wif)

    if account_name and account:
        update_profile(account_name, account)
    else:
        print("Failed to retrieve account details.")


if __name__ == "__main__":
    main()
