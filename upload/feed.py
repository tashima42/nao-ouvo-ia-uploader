import xml.etree.ElementTree as ET

def feed_tree(file):
    return ET.parse(file)

def feed_items(tree):
    root = tree.getroot()
    return root[0].findall("item")

