#!/usr/bin/env python3
#
# wekan_type.py

"""wekan_type.py
   talks to the wekan database (default at 172.16.2.2)
   and looks for the type of an object and optionally
   changes it.
   Can be used to recover a wekan board that accidentially
   ended up with type template-container.
   (c) Kurt Garloff <kurt@garloff.de>, 07/2023
   SPDX-License-Identifier: CC-BY-SA-4.0
"""

import sys
import os
import pymongo

MONGOHOST = "mongodb://172.16.2.2"


def get_client(connstr=MONGOHOST):
    "Connect to mongo database"
    return pymongo.MongoClient(connstr)


def get_boards(client):
    "Return list of wekan board documents"
    return client.wekan.boards


def get_type(board, title):
    "Return type of board board with title title"
    return board.find_one({"title": title})["type"]


def set_type(board, title, newtype):
    "Change type of board board with title title to newtype"
    doc = board.find_one({"title": title})
    oldtp = doc["type"]
    if oldtp == newtype:
        print(f"No change needed, type of {title} already {oldtp}")
        return
    # doc["type"] = newtype
    board.update_one({"title": title}, {"$set": {"type": newtype}})
    print(f"... updated to {newtype}")


def usage():
    "Usage information (help)"
    print("Usage: wekan_type.py [-h MONGOIP] TITLE [NEWTYPE]")
    print("Displays type of board with title TITLE")
    print(" in wekan mongo database at IP address MONGOIP.")
    print("If NEWTYPE is passed, the type will be changed to NEWTYPE.")
    sys.exit(1)


def main(argv):
    "Main entry point"
    if len(argv) < 1:
        usage()
    connstr = MONGOHOST
    if "MONGOHOST" in os.environ:
        connstr = f"mongodb://{os.environ['MONGOHOST']}"
    if argv[0] == "-h":
        connstr = f"mongodb://{argv[1]}"
        argv = argv[2:]
    title = argv[0]
    client = get_client(connstr)
    boards = get_boards(client)
    print(f"Type of board {title}: {get_type(boards, title)}")
    if len(argv) > 1:
        set_type(boards, title, argv[1])
    client.close()


if __name__ == "__main__":
    main(sys.argv[1:])
