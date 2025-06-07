import os
import json

def read_episodes(episodes_path):
    if os.stat(episodes_path).st_size == 0:
        print("Error: JSON file is empty.")
        exit(1)

    with open(episodes_path, "r", encoding="utf-8") as f:
        eps = json.load(f)
    return eps

def save_episodes(episodes_path, episodes):
    with open(episodes_path, "w", encoding="utf-8") as f:
        json.dump(episodes, f, indent=2, ensure_ascii=False)
