#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "hiveengine",
#     "python-dotenv",
# ]
# ///

import os
import time

from nectar import Hive
from nectar.wallet import Wallet
from dotenv import load_dotenv

# from hiveengine.tokens import Tokens
from hiveengine.wallet import Wallet as heWallet

DRY_RUN = False
WHITELIST = [
    "INCOME",
    "ARCHON",
    "ARCHONM",
    "ARMERO",
    "BEE",
    "SIM",
    "PIMP",
    "LGN",
    "SWAP.HIVE",
    "SWAP.LTC",
    "SWAP.BTC",
    "SWAP.ETH",
]


def dump_dust():
    load_dotenv()
    ACTIVE_WIF = os.getenv("ACTIVE_WIF")
    send_to = input("Enter destination: ")

    hv = Hive(keys=[ACTIVE_WIF], nodes="https://api.hive.blog", nobroadcast=DRY_RUN)
    w = Wallet(blockchain_instance=hv)
    usr = w.getAccountFromPrivateKey(ACTIVE_WIF)
    hew = heWallet(account=usr, blockchain_instance=hv)
    tokens = hew.get_balances()

    for token in tokens:
        symbol = token["symbol"]
        # info = Tokens().get_token(symbol)
        balance = float(f"{float(token['balance'])}")
        if balance < 1 and balance > 0 and symbol not in WHITELIST:
            print(f"[ Transfering {balance} of {symbol} to {send_to} ]")
            hew.transfer(send_to, balance, symbol, memo="Automatic transfer")
            time.sleep(1)

    return None


if __name__ == "__main__":
    dump_dust()
