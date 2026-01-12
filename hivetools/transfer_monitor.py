#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "dataset",
#     "python-dotenv",
# ]
# ///


import dataset
from nectar import Hive
from nectar.blockchain import Blockchain

# Ask for user ID
hive_id = input("Hive User ID: ")
# hive_id = yournamehere # if you want to hard code it.

hive = Hive(node="https://api.hive.blog")
db = dataset.connect("sqlite:///transactions.db")

# System Variables
blockchain = Blockchain(blockchain_instance=hive)
stream = blockchain.stream(
    opNames=["transfer"], raw_ops=False, threading=True, thread_num=4
)
table = db[hive_id]


# parse json data to SQL insert
def update_db(post):
    try:
        table.insert(dict(post))
        db.commit()
    except Exception as e:
        print(f"[Error: {e} moving on]")
        db.rollback()


def monitor():
    print("[Starting up...]")
    db.begin()
    # Read the live stream and filter out only transfers
    for post in stream:
        if post["to"] == hive_id or post["from"] == hive_id:
            print(f"[Transaction Found from {post['from']} to {post['to']}]")
            update_db(post)


if __name__ == "__main__":
    monitor()
