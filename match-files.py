import xml.etree.ElementTree as ET
import sys
import os
from internetarchive import upload
from datetime import datetime
import re
import unicodedata
import json

if len(sys.argv) != 3:
    print("missing args")
    exit(1)
nao_ouvo_dir = sys.argv[1]
episodes_path = sys.argv[2]


tree = ET.parse('feed.xml')
root = tree.getroot()
items = root[0].findall("item")
# load secrets
access_key = os.getenv("S3_ACCESS_KEY")
secret_key = os.getenv("S3_SECRET_KEY")

def match(items):
    episodes = read_episodes()

    for item in items:
        title = item.find("title").text
        description = item.find("description").text
        pubDate = item.find("pubDate").text

        slug = create_slug(title)
       
        print("uploading " + title + " : " + slug)
        if slug in episodes["missing"] or slug in episodes["uploaded"]:
            print("skipping: " + slug)
            continue

        md = {
            'collection': 'opensource_audio',
            'title': title,
            'mediatype': 'audio',
            'date': format_date(pubDate),
            'description': description,
            'language': 'Portuguese',
            'creator': 'Não Ouvo',
        }

        file = os.path.join(nao_ouvo_dir, title + ".mp3")

        if os.path.isfile(file) == False:
            print("missing: "+ file)
            exit(1)

        if ia_upload(slug, file, md)[0].status_code != 200:
            print("failed upload: " + slug)
            episodes["failed"].append(slug)
            save_episodes(episodes)
            continue

        episodes["uploaded"].append(slug)
        print("uploaded: " + slug)
        save_episodes(episodes)


def create_slug(text):
    normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    cleaned = re.sub(r'[^a-zA-Z0-9]+', '-', normalized)
    slug = cleaned.strip('-').lower()
    return slug


def format_date(date):
    dt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
    formatted_date = dt.strftime("%Y-%m-%d")
    return formatted_date

def read_episodes():
    if os.stat(episodes_path).st_size == 0:
        print("Error: JSON file is empty.")
        exit(1)

    with open(episodes_path, "r", encoding="utf-8") as f:
        eps = json.load(f)
    return eps

def save_episodes(episodes):
    with open(episodes_path, "w", encoding="utf-8") as f:
        json.dump(episodes, f, indent=4, ensure_ascii=False)

def ia_upload(slug, upload_file, md):
    r = upload(slug, files=[upload_file], metadata=md, access_key = access_key, secret_key = secret_key)
    return r

match(items)
