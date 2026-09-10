import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCDYoGUf9Yx3wzJT_w-AF7_w"
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHANNEL = "@Hossana360"

RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
STATE_FILE = "last_video.txt"


def get_latest_video():

    data = urllib.request.urlopen(RSS_URL).read()
    root = ET.fromstring(data)

    ns = {
        "yt": "http://www.youtube.com/xml/schemas/2015"
    }

    entry = root.find(
        "{http://www.w3.org/2005/Atom}entry"
    )

    if entry is None:
        return None

    author = entry.find(
        "{http://www.w3.org/2005/Atom}author/"
        "{http://www.w3.org/2005/Atom}name"
    )

    if author is not None:
        print("YouTube channel:", author.text)

    video_id = entry.find(
        "yt:videoId",
        ns
    ).text

    title = entry.find(
        "{http://www.w3.org/2005/Atom}title"
    ).text

    return video_id, title


def send_to_telegram(video_id, title):

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    message = (
        "🎬 <b>NEW VIDEO — HOSSANA 360°</b>\n\n"
        f"<b>{title}</b>\n\n"
        f'▶️ <a href="{video_url}">Watch on YouTube</a>'
    )

    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_TOKEN}/sendMessage"
    )

    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHANNEL,
        "text": message,
        "parse_mode": "HTML"
    }).encode()

    urllib.request.urlopen(
        url,
        data=data
    )


def main():

    print("Checking HOSSANA 360° for a new video...")

    latest = get_latest_video()

    if not latest:
        print("No video found.")
        return

    video_id, title = latest

    print("Latest video:", title)

    if os.path.exists(STATE_FILE):

        with open(STATE_FILE, "r") as f:
            last_video = f.read().strip()

        if last_video == video_id:
            print("No new video.")
            return

    send_to_telegram(
        video_id,
        title
    )

    with open(STATE_FILE, "w") as f:
        f.write(video_id)

    print(
        "New HOSSANA 360° video posted:",
        title
    )


if __name__ == "__main__":
    main()
