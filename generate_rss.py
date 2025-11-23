import json
import os
from datetime import datetime
from urllib.parse import quote

# Load global metadata
with open("metadata.json") as f:
    meta = json.load(f)

episodes_dir = "episodes"
metadata_dir = "metadata"

# List of MP3 files
mp3_files = sorted([
    f for f in os.listdir(episodes_dir)
    if f.endswith(".mp3")
])

items = ""
for mp3 in mp3_files:
    base = mp3.rsplit(".", 1)[0] # Remove .mp3 extension
    meta_file = f"{base}.json" # Corresponding metadata file name
    meta_path = os.path.join(metadata_dir, meta_file)

    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"No metadata JSON found for {mp3}")

    # Load episode metadata
    with open(meta_path) as f:
        m = json.load(f)

    # Convert pubDate
    dt = datetime.fromisoformat(m["pubDate"].replace("Z", "+00:00"))
    pubdate_rfc822 = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

    url = f"{meta['site_url']}/episodes/{quote(mp3)}"

    items += f"""
    <item>
        <title>{m["title"]}</title>
        <description><![CDATA[{m["description"]}]]></description>
        <enclosure url="{url}" type="audio/mpeg" />
        <guid>{url}</guid>
        <pubDate>{pubdate_rfc822}</pubDate>
        <itunes:duration>{m["duration"]}</itunes:duration>
        <itunes:explicit>{"yes" if m["explicit"] else "no"}</itunes:explicit>
    </item>
    """

# Build RSS feed
rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel>
    <title>{meta['title']}</title>
    <description>{meta['description']}</description>
    <link>{meta['site_url']}</link>
    <language>{meta['language']}</language>
    {items}
</channel>
</rss>
"""

with open("feed.xml", "w") as f:
    f.write(rss)
