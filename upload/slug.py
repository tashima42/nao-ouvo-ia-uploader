import re
import unicodedata

def create_slug(text):
    normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    cleaned = re.sub(r'[^a-zA-Z0-9]+', '-', normalized)
    slug = cleaned.strip('-').lower()
    return slug
