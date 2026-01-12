#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "python-dotenv",
# ]
# ///

import os
from typing import Optional, Tuple

from nectar import Hive
from nectar.account import Account
from nectar.constants import resource_execution_time
from nectar.rc import RC
from nectar.wallet import Wallet
from dotenv import load_dotenv


def setup_hive() -> Tuple[Hive, Account]:
    """Setup Hive connection and return hive instance and account."""
    wif = os.getenv("ACTIVE_WIF")
    if not wif:
        raise ValueError("No active WIF found in environment")

    hive = Hive(node="https://api.hive.blog", keys=wif)
    account = Account(
        Wallet(blockchain_instance=hive).getAccountFromPrivateKey(wif),
        blockchain_instance=hive,
    )
    return hive, account


def check_claimable_accounts() -> None:
    """Check how many accounts can be claimed with current RC."""
    try:
        hive, account = setup_hive()
        rc = RC(blockchain_instance=hive)

        # Get current mana and claim cost
        current_mana = int(account.get_rc_manabar()["current_mana"])
        claim_cost = hive.get_rc_cost(
            rc.get_resource_count(
                tx_size=300,
                execution_time_count=resource_execution_time[
                    "claim_account_operation_exec_time"
                ],
                new_account_op_count=1,
            )
        )

        # Calculate and display results
        can_claim = current_mana // claim_cost if claim_cost > 0 else 0
        print(f"Current RC mana: {current_mana:,}")
        print(f"Cost per account: {claim_cost:,}")
        print(f"You can claim approximately {can_claim:,} accounts")

    except Exception as e:
        print(f"Error checking claimable accounts: {e}")


def claim_account() -> Optional[dict]:
    """Claim a HIVE account if sufficient RC is available."""
    try:
        hive, account = setup_hive()

        # Get mana before claim
        mana_before = int(account.get_rc_manabar()["current_mana"])
        print(f"Mana before claim: {mana_before:,} RC")

        # Attempt account claim
        tx = hive.claim_account(creator=account.name, fee=None)

        # Get mana after claim and calculate cost
        mana_after = int(account.get_rc_manabar()["current_mana"])
        print(f"Mana after claim: {mana_after:,} RC")
        print(f"Mana cost: {mana_before - mana_after:,} RC")

        return tx

    except Exception as e:
        print(f"Claim account error: {e}")
        return None


def main() -> None:
    """Check claimable accounts and optionally claim one."""
    load_dotenv()

    check_claimable_accounts()

    if input("\nWould you like to claim an account? (y/N): ").lower() == "y":
        claim_account()


if __name__ == "__main__":
    main()
