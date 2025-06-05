import xml.etree.ElementTree as ET
import re
import unicodedata
import urllib.parse

tree = ET.parse('feed.xml')
root = tree.getroot()
items = root[0].findall("item")

html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Não Ouvo (Arquivo da Comunidade)</title>
  <link rel="stylesheet" href="./style.css">
  <link rel="icon" href="./favicon.ico" type="image/x-icon">
</head>

<body>
  <main>
    <h1>Não Ouvo (Arquivo da Comunidade)</h1>
    <div id="episodes">
        {items}
    </div>
  </main>
</body>
</html>
"""
episode_block = """
<div id="{slug}">
  <h2 class="title">{title}</h2>
  <p class="date">{date}</p>
  <p class="description">{description}</p>
    <audio controls>
    <source src="{stream}" type="audio/mpeg">
    Your browser does not support the audio element.
    </audio>
</div>
"""

def create_slug(text):
    normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    cleaned = re.sub(r'[^a-zA-Z0-9]+', '-', normalized)
    slug = cleaned.strip('-').lower()
    return slug

episodes = []

for item in items:
    title = item.find("title").text
    description = item.find("description").text
    date = item.find("pubDate").text

    slug = create_slug(title)
    encoded_slug = urllib.parse.quote(slug)
    encoded_title = urllib.parse.quote(title)

    ep = {
        'slug': slug,
        'title': title,
        'description': description,
        'date': date,
        'stream': f"https://archive.org/serve/{encoded_slug}/{encoded_title}.mp3"
    }
    episodes.append(ep)

items_html = "\n".join([episode_block.format(**ep) for ep in episodes])
final_html = html_template.format(items=items_html)

# Write to file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("HTML file generated: index.html")
