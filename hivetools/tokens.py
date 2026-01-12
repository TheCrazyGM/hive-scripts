#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "hiveengine",
#     "prettytable",
# ]
# ///


from nectar import Hive
from hiveengine.api import Api
from hiveengine.wallet import Wallet as heWallet
from prettytable import PrettyTable

ACCOUNT = "thecrazygm"


def dump_all():
    api = Api(url="https://engine.thecrazygm.com/")
    hv = Hive(nodes="https://api.hive.blog")
    usr = ACCOUNT
    hew = heWallet(account=usr, api=api, blockchain_instance=hv)
    tokens = hew.get_balances()

    # Create a PrettyTable to display token balances
    table = PrettyTable()
    table.field_names = [
        "Symbol",
        "Balance",
        "Stake",
        "Pending Unstake",
        "Delegations In",
        "Delegations Out",
        "Pending Undelegations",
    ]

    table.sortby = "Balance"
    table.reversesort = True
    table.align["Symbol"] = "l"
    table.align["Balance"] = "r"
    table.align["Stake"] = "r"
    table.align["Pending Unstake"] = "r"
    table.align["Delegations In"] = "r"
    table.align["Delegations Out"] = "r"
    table.align["Pending Undelegations"] = "r"

    for token in tokens:
        symbol = token["symbol"]
        balance = float(token["balance"])
        stake = float(token["stake"])
        pendingUnstake = float(token["pendingUnstake"])
        delegationsIn = float(token["delegationsIn"])
        delegationsOut = float(token["delegationsOut"])
        pendingUndelegations = float(token["pendingUndelegations"])

        # Only add to table if balance is greater than 0
        if (
            balance > 0
            or stake > 0
            or pendingUnstake > 0
            or delegationsIn > 0
            or delegationsOut > 0
            or pendingUndelegations > 0
        ):
            table.add_row(
                [
                    symbol,
                    balance,
                    stake,
                    pendingUnstake,
                    delegationsIn,
                    delegationsOut,
                    pendingUndelegations,
                ]
            )

    # Print the table if it's not empty
    if len(table._rows) > 0:
        print(table)
    else:
        print("No tokens with balance found.")

    return None


if __name__ == "__main__":
    dump_all()
