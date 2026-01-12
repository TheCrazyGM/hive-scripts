#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "hive-nectar",
#     "python-dotenv",
# ]
# ///


import os
import re

from nectar import Hive
from nectar.account import Account
from nectar.blockchain import Blockchain
from nectar.comment import Comment
from nectar.instance import set_shared_blockchain_instance
from nectar.utils import construct_authorperm

posting_key = os.environ["POSTING_WIF"]
REGEX = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)"
botname = "thecrazygm"
weight = 100

hive = Hive(node=["https://api.hive.blog"], keys=posting_key)
set_shared_blockchain_instance(hive)
chain = Blockchain()
followees = Account(botname).get_following()


def summon_upvotebot():
    print("[Starting up]")
    while True:
        try:
            for post in chain.stream(opNames="comment", threading=True, thread_num=5):
                mentions = re.findall(REGEX, post["body"])
                comment = Comment(post)
                perm = comment.authorperm
                parent = construct_authorperm(
                    Comment(perm).parent_author, Comment(perm).parent_permlink
                )
                author = post["author"]
                if Comment(perm).is_comment and botname in mentions:
                    print(
                        f"[{author} just mentioned {botname} in {perm} in reply to {parent}]"
                    )
                    if author in followees:
                        Comment(parent).upvote(weight=weight, voter=botname)
                        print(
                            f"[{botname} voted {weight}% on {parent} per {author}'s request]"
                        )
                    else:
                        print(
                            f"[{author} tried to summon {botname} but is not in the whitelist]"
                        )
        except Exception as error:
            print(repr(error))
            continue


if __name__ == "__main__":
    summon_upvotebot()
