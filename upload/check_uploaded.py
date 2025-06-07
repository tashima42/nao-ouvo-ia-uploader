import os
from internetarchive import get_item
import json
import argparse

parser = argparse.ArgumentParser(description="Nao Ouvo Internet Archive upload CLI")

parser.add_argument("--episodesfile", required=True, type=str, help="Episode JSON file")

args = parser.parse_args()

episodes_path = args.episodesfile

def check(id):
    return get_item(id).exists

def check_episodes(episodes_path):
    episodes = read_episodes(episodes_path)["uploaded"]

    for episode in episodes:
        if check(episode) == False:
            print("not found: " + episode)

def read_episodes(episodes_path):
    if os.stat(episodes_path).st_size == 0:
        print("Error: JSON file is empty.")
        exit(1)

    with open(episodes_path, "r", encoding="utf-8") as f:
        eps = json.load(f)
    return eps

check_episodes(episodes_path)
