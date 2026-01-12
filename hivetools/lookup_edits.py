#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "python-dotenv",
# ]
# ///


from nectar import Hive
from nectar.account import Account
from nectar.comment import Comment

hive = Hive(nodes="https://anyx.io")


def get_comment_and_replies(authorperm):
    # Connect to the hive blockchain

    # Extract author and permlink from authorperm
    author, permlink = authorperm.split("/")

    # Get the comment
    comment = Comment(authorperm, hive=hive)

    return comment


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <authorperm>")
        sys.exit(1)

    authorperm = sys.argv[1]
    comment = get_comment_and_replies(authorperm)
    created = comment.get("created")
    updated = comment.get("updated")
    author = comment.get("author")
    snap = Account(author, blockchain_instance=hive)
    snap_range = snap.history(start=created, stop=updated, only_ops=["comment"])
    print(f"Author   : {comment['author']}")
    print(f"Permlink : {comment['permlink']}")
    print(f"created  : {created}")
    print(f"updated  : {updated}")
    print()

    print("History  :")
    for x in snap_range:
        if x["permlink"] == comment["permlink"]:
            print(f"{x['trx_id']}" + "=" * 20)
            print(x["body"])
