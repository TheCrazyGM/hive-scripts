#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "hive-nectar",
#     "prettytable",
# ]
# ///

"""
Simplified Hive Notifications Viewer with prettytable
"""

import os
import sys

from nectar import Hive
from nectar.account import Account
from nectar.exceptions import AccountDoesNotExistsException, MissingKeyError
from nectar.wallet import Wallet
from prettytable import PrettyTable

NODES = ["https://api.hive.blog", "https://api.syncad.com"]


def get_wif():
    return os.getenv("POSTING_WIF")


def connect_to_hive(wif=None):
    try:
        if wif:
            hive = Hive(keys=wif, node=NODES)
            wallet = Wallet(blockchain_instance=hive)
            account_name = wallet.getAccountFromPrivateKey(wif)
            account = Account(account_name, blockchain_instance=hive)
            return hive, account
        else:
            return Hive(node=NODES), None
    except (AccountDoesNotExistsException, MissingKeyError) as e:
        print(f"Error connecting to account: {e}", file=sys.stderr)
        return None, None


def extract_notification_details(notif):
    date = notif.get("date", "N/A")
    if hasattr(date, "strftime"):
        date = date.strftime("%Y-%m-%d %H:%M:%S")

    sender = "N/A"
    data_str = "N/A"
    msg = notif.get("msg", "")
    url = notif.get("url", "")
    notif_type = notif.get("type", "")

    if "@" in msg:
        parts = msg.split()
        for part in parts:
            if part.startswith("@") and len(part) > 1:
                sender = part
                break

    if sender == "N/A" and url and url.startswith("@"):
        sender = url.split("/")[0]

    if msg:
        if notif_type == "vote":
            if "voted on your post" in msg:
                if "($" in msg and ")" in msg:
                    amount = msg.split("($")[1].split(")")[0]
                    data_str = f"voted {amount} on your post"
                else:
                    data_str = "voted on your post"
        elif notif_type == "mention":
            if "mentioned you" in msg:
                if "and" in msg and "others" in msg:
                    others_count = msg.split("and ")[1].split(" others")[0]
                    data_str = f"mentioned you and {others_count} others"
                else:
                    data_str = "mentioned you"
        elif notif_type == "reply":
            if "replied to your" in msg:
                data_str = "replied to your post"
            elif "replied to you" in msg:
                data_str = "replied to you"
        elif notif_type == "reblog":
            if "reblogged your post" in msg:
                data_str = "reblogged your post"
        if data_str == "N/A":
            data_str = msg

    if data_str == "N/A" and url:
        if "/" in url:
            post_title = url.split("/", 1)[1]
            data_str = f"re: {post_title}"

    return sender, date, data_str


def main():
    account_name = "thecrazygm"
    wif = get_wif()

    hive, account = connect_to_hive(wif)
    if not hive:
        print("Failed to connect to Hive.", file=sys.stderr)
        return 1

    if not account:
        # No key provided, create account object for a public account
        account = Account(account_name, blockchain_instance=hive)
    else:
        # If connected with WIF, but want different account, replace here if needed
        account_name = account.name

    try:
        notifications = account.get_notifications(only_unread=True, limit=100)
    except Exception as e:
        print(f"Failed to fetch notifications: {e}", file=sys.stderr)
        return 1

    if not notifications:
        print(f"No notifications found for @{account_name}.")
        return 0

    table = PrettyTable()
    table.field_names = ["#", "Type", "From", "Data", "Date"]
    table.align["Data"] = "l"
    table.align["From"] = "l"

    for i, notif in enumerate(notifications, 1):
        sender, date, data_str = extract_notification_details(notif)
        table.add_row([i, notif.get("type", "N/A"), sender, data_str, date])

    print(f"Notifications for @{account_name} (up to 100):\n")
    print(table)

    return 0


if __name__ == "__main__":
    sys.exit(main())
