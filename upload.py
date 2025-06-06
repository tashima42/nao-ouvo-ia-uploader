import xml.etree.ElementTree as ET
import sys
import os
from internetarchive import upload
from datetime import datetime
import re
import unicodedata
import json
import argparse
from filelock import Timeout, FileLock

parser = argparse.ArgumentParser(description="Nao Ouvo Internet Archive upload CLI")

parser.add_argument("episodesdir", type=str, help="Episodes directory path")
parser.add_argument("--episodesfile", required=True, type=str, help="Episode JSON file")
parser.add_argument("--lockfile", required=True, type=str, help="Episodes lock file")
parser.add_argument("--include", nargs="+", default=[], help="Start with slug prefix")
parser.add_argument("--ignore", nargs="+", default=[], help="Ignore start with slug prefix")

args = parser.parse_args()

nao_ouvo_dir = args.episodesdir
episodes_path = args.episodesfile
lock_path = args.lockfile
include = args.include
ignore = args.ignore
# load secrets
access_key = os.getenv("S3_ACCESS_KEY")
secret_key = os.getenv("S3_SECRET_KEY")

tree = ET.parse('feed.xml')
root = tree.getroot()
items = root[0].findall("item")

lock = FileLock(lock_path, timeout=5)

def match(items):
    for item in items:
        title = item.find("title").text
        description = item.find("description").text
        pubDate = item.find("pubDate").text

        slug = create_slug(title)

        skip = False

        for prefix in include:
            if slug.startswith(prefix) == False:
                skip = True
        
        for prefix in ignore:
            if slug.startswith(prefix):
                skip = True

        if skip:
            continue

        lock.acquire()
        try:
            episodes = read_episodes()
        finally:
            lock.release()
       
        if slug in episodes["missing"] or slug in episodes["uploaded"] or slug in episodes["uploading"]:
            print("skipping: " + slug)
            continue

        lock.acquire()
        try:
            episodes = read_episodes()
            episodes["uploading"].append(slug)
            save_episodes(episodes)
        finally:
            lock.release()

        print("uploading " + title + " : " + slug)

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

        try:
            ia_upload(slug, file, md)
        except Exception as e:
            print(f"Failed to upload {slug}: {e}")

            lock.acquire()
            try:
                episodes = read_episodes()
                episodes["failed"].append(slug)
                save_episodes(episodes)
            finally:
                lock.release()

        lock.acquire()
        try:
            episodes = read_episodes()
            episodes["uploaded"].append(slug)
            episodes["uploading"].remove(slug)
            print("uploaded: " + slug)
            save_episodes(episodes)
        finally:
            lock.release()


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
        json.dump(episodes, f, indent=2, ensure_ascii=False)

def ia_upload(slug, upload_file, md):
    r = upload(slug, files=[upload_file], metadata=md, access_key = access_key, secret_key = secret_key)
    return r

match(items)
