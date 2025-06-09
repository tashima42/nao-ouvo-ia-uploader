import argparse
from episodes_file import read_episodes
from feed import feed_tree
from slug import create_slug
import urllib.parse

parser = argparse.ArgumentParser(description="Nao Ouvo update feed CLI")

parser.add_argument("--episodesfile", required=True, type=str, help="Episode JSON file")
parser.add_argument("--feedfile", required=True, type=str, help="Feed file")

args = parser.parse_args()

episodes_path = args.episodesfile
feed_path = args.feedfile

def update(episodes_path, feed_path):
    episodes = read_episodes(episodes_path)
    expected = episodes["expected"]
    missing = episodes["missing"]

    tree = feed_tree(feed_path)
    root = tree.getroot()
    items = root[0].findall("item")

    for item in items:
        title_el = item.find("title")
        if title_el is None:
            print("title not found")
            exit(1)

        title = title_el.text
        slug = create_slug(title)

        if slug in missing:
            continue

        ex = expected.get(slug)

        if ex is None:
            print("episode file not found: " , title)
            exit(1)

        enclosure = item.find("enclosure")

        if enclosure is None:
            print("enclosure not found: ", title)
            exit(1)
            
        url = urllib.parse.quote(f"https://archive.org/download/{slug}/{ex}", safe=':/?[]@!$&\'*+,;=')

        enclosure.set("url", url)

    tree.write("new_feed.xml", "utf-8")

update(episodes_path, feed_path)
