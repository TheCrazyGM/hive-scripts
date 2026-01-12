#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "python-dotenv",
# ]
# ///

import os
from pprint import pprint

from nectar import Hive
from nectar.account import Account
from nectar.wallet import Wallet
from dotenv import load_dotenv

load_dotenv()
active_wif = os.getenv("ACTIVE_WIF")

hv = Hive(node="https://api.hive.blog", keys=[active_wif])
w = Wallet(blockchain_instance=hv)
usr = w.getAccountFromPrivateKey(active_wif)
a = Account(usr, blockchain_instance=hv)
deleg = a.get_vesting_delegations()
for x in deleg:
    delegatee = x["delegatee"]
    print(f"[Dropping delegation to {delegatee} to 0]")
    pprint(a.delegate_vesting_shares(delegatee, 0))
