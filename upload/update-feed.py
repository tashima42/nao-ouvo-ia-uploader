import argparse
from sys import dont_write_bytecode
from episodes_file import read_episodes, save_episodes
from feed import feed_tree
from slug import create_slug
import urllib.request
from lxml import html
import os

parser = argparse.ArgumentParser(description="Nao Ouvo update feed CLI")

parser.add_argument("--episodesfile", required=True, type=str, help="Episode JSON file")
parser.add_argument("--feedfile", required=True, type=str, help="Feed file")

args = parser.parse_args()

episodes_path = args.episodesfile
feed_path = args.feedfile

def download_pages(episodes_path):
    episodes = read_episodes(episodes_path)
    uploaded = episodes["uploaded"]
    urls = {}

    pages = os.listdir("pages")

    for episode in uploaded:
        page = f"{episode}.html"
        if page not in pages:
            with urllib.request.urlopen(f"https://archive.org/download/{episode}") as response:
                if response.getcode() != 200:
                    print("failed to get download file: ", episode)
                html_content = response.read().decode('utf-8')  # Decode bytes to string
            
            with open(f"pages/{episode}.html", "w", encoding="utf-8") as file:
                file.write(html_content)
        else:
            with open(f"pages/{episode}.html", "r", encoding="utf-8") as file:
                html_content = file.read()

        html_tree = html.fromstring(html_content)
        href = html_tree.find("body").find("div").find("main").find("div").find("div").find("table").find("tbody")[1].find("td").find("a").values()[0]
            
        url = f"https://archive.org/download/{episode}/{href}"
        urls[episode] = url

    episodes["urls"] = urls
    save_episodes(episodes_path, episodes)


def update(episodes_path, feed_path):
    episodes = read_episodes(episodes_path)
    urls = episodes["urls"]

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

        if slug not in urls:
            continue

        url = urls.get(slug)

        if url is None:
            print("episode file not found: " , title)
            exit(1)

        enclosure = item.find("enclosure")

        if enclosure is None:
            print("enclosure not found: ", title)
            exit(1)

        enclosure.set("url", url)


    tree.write("new_feed.xml", "utf-8")

update(episodes_path, feed_path)
#download_pages(episodes_path)
