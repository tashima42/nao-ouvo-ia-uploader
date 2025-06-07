import os
import argparse
from episodes_file import read_episodes, save_episodes
from slug import create_slug

parser = argparse.ArgumentParser(description="Nao Ouvo Internet Archive upload CLI")

parser.add_argument("episodesdir", type=str, help="Episodes directory path")
parser.add_argument("--episodesfile", required=True, type=str, help="Episode JSON file")

args = parser.parse_args()

nao_ouvo_dir = args.episodesdir
episodes_path = args.episodesfile

def generate_expected(episodes_path, nao_ouvo_dir):
    expected_episodes = {}

    files = os.listdir(nao_ouvo_dir)
    for file in files:
        title = file.split(".mp3")[0]
        expected_episodes[create_slug(title)] = file
    episodes = read_episodes(episodes_path)

    episodes["expected"] = expected_episodes
    save_episodes(episodes_path, episodes)

def compare_expected(episodes_path):
    episodes = read_episodes(episodes_path)

    expected = episodes["expected"]
    uploaded = episodes["uploaded"]
    
    for ep in expected:
        if ep not in uploaded:
            print("missing: " + ep + " - " + expected[ep])

generate_expected(episodes_path, nao_ouvo_dir)
compare_expected(episodes_path)
