from notion.client import NotionClient
from datetime import datetime
from dateutil.parser import parse as date_parser
import feedparser, json

with open("config.json") as f:
    config = json.load(f)


def addArticleToNotion(title, link, source):
    # Note this may expire and need to be manually refreshed
    client = NotionClient(token_v2=config["settings"]["notion_token"])
    cv = client.get_collection_view(config["settings"]["notion_url"])

    print(f"sending {title} {link} {source} to Notion")
    row = cv.collection.add_row()
    row.title = title
    row.link = link
    row.source = source
    row.date_added = datetime.today().date()


def publishFeedToNotion(source, feed_url, just_today=True):
    print(f"Fetching posts from {source}")
    d = feedparser.parse(feed_url)
    for entry in d.entries:
        date = getTimeFromEntry(entry)
        if just_today:
            if date.date() < datetime.today().date():
                break

        addArticleToNotion(entry.get("title"), entry.get("link"), source)


def getTimeFromEntry(entry):
    # lethian has no publish field so doing this manually
    possible_field_names = ["pubDate", "published", "updated"]
    for field_name in possible_field_names:
        raw_time = entry.get(field_name, None)
        if raw_time is not None:
            break

    if raw_time is None:
        print(f"Could not parse time from {entry}")
        return datetime.today()

    return date_parser(raw_time)


for source, feed_url in config["feeds"].items():
    publishFeedToNotion(source, feed_url)
