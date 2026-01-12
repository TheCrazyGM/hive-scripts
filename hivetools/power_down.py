#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "python-dotenv",
# ]
# ///


import os
from datetime import datetime
from pprint import pprint

from nectar import Hive
from nectar.account import Account
from nectar.wallet import Wallet
from dotenv import load_dotenv


def kill_the_power():
    # Get all availble VESTS to powerdown right now and make it into a string that the withdraw can handle
    avail_vests = a.get_effective_vesting_shares()
    vests_str = f"{avail_vests / 1e6} VESTS"
    print(f"[Powering Down {vests_str}]")
    pprint(a.withdraw_vesting(vests_str))


def kill_em_all():
    # Get all delegate and set them to 0
    deleg = a.get_vesting_delegations()
    for x in deleg:
        delegatee = x["delegatee"]
        print(f"[Dropping delegation to {delegatee} to 0]")
        pprint(a.delegate_vesting_shares(delegatee, 0))
    # See how long before they can be powered down, including the ones just done and all others
    expiring = a.get_expiring_vesting_delegations()
    for x in expiring:
        now = datetime.now()
        then = datetime.strptime(x["expiration"], "%Y-%m-%dT%H:%M:%S")
        when = then - now
        if then > now:
            # TODO: no idea how to get the previous delgatee
            print(f"[{when} until delegation free for power down on ID:{x['id']}]")


if __name__ == "__main__":
    load_dotenv()
    # Ask the User for the Active Key to start the whole process
    active_wif = os.getenv("ACTIVE_WIF")

    # Set all sytem variables (steem connection, wallet, username, and account)
    hv = Hive(node="https://api.hive.blog", keys=[active_wif], nobroadcast=False)
    w = Wallet(blockchain_instance=hv)
    usr = w.getAccountFromPrivateKey(active_wif)
    a = Account(usr, blockchain_instance=hv)

    # Queue Metal Music Here
    kill_em_all()
    kill_the_power()
