import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

# List of webcam page URLs and corresponding iframe identifiers
webcams = [
    {"url": "https://www.ipcamlive.com/6111a4f6c1edf", "alias": "6111a4f6c1edf", "title": "Large Indoor Playroom A"},
    {"url": "https://www.ipcamlive.com/6111a4ba3af5d", "alias": "6111a4ba3af5d", "title": "Large Indoor Playroom B"},
    {"url": "https://www.ipcamlive.com/6111a0d8eab5c", "alias": "6111a0d8eab5c", "title": "Large Outdoor A Yard"},
    {"url": "https://www.ipcamlive.com/6111a564d8891", "alias": "6111a564d8891", "title": "Large Outdoor B Yard"},
    {"url": "https://www.ipcamlive.com/6111a56d46881", "alias": "6111a56d46881", "title": "Large Outdoor A & B Yard"},
    {"url": "https://www.ipcamlive.com/6111a5c92d45e", "alias": "6111a5c92d45e", "title": "Large Outdoor Side Yard"},
    {"url": "https://www.ipcamlive.com/6111a4ed630c7", "alias": "6111a4ed630c7", "title": "Smalls Indoor Playroom"},
    {"url": "https://www.ipcamlive.com/6111a440ef275", "alias": "6111a440ef275", "title": "Smalls Outdoor Yard"}
]

# Function to retrieve the token from the HTML source
def get_token_from_html(html):
    match = re.search(r"var token = '(.*?)';", html)
    if match:
        return match.group(1)
    return None

# Read the original index.html
with open("index.html", "r") as file:
    html_content = file.read()

# Iterate over each webcam, fetch the page, retrieve the token, and update the iframe
for webcam in webcams:
    response = requests.get(webcam["url"])
    if response.status_code == 200:
        token = urllib.parse.quote(get_token_from_html(response.text))
        print(f"Token for {webcam['title']}: {token}")
        if token:
            # Replace the token in the iframe URL
            iframe_pattern = (rf'<iframe src="https://www\.ipcamlive\.com/player/player\.php\?alias={webcam["alias"]}&autoplay=1&&token=[^"]*" ' 
                              rf'title="{webcam["title"]}"></iframe>')
            new_iframe = (f'<iframe src="https://www.ipcamlive.com/player/player.php?alias={webcam["alias"]}&autoplay=1&&token={token}" ' 
                          f'title="{webcam["title"]}"></iframe>')
            html_content = re.sub(iframe_pattern, new_iframe, html_content)

# Write the updated HTML back to the file
with open("index.html", "w") as file:
    file.write(html_content)

print("Tokens updated successfully!")
