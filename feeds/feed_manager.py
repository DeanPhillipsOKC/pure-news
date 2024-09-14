import feedparser as fp
from dateutil import parser as date_parser

class FeedManager:
    def __init__(self):
        self.feeds = {
            "The Associated Press: Politics": "https://rss.app/feeds/mb2uFhZzuSM4Ahyq.xml",
            "The Associated Press: US News": "https://rss.app/feeds/jrqfJ92O5hi18GdT.xml",
            "The Atlantic: News": "http://feeds.feedburner.com/TheAtlantic",
            "The Atlantic: Politics": "http://feeds.feedburner.com/AtlanticPoliticsChannel",
            "NPR: News": "http://www.npr.org/rss/rss.php?id=1001",
            "NPR: Politics": "http://www.npr.org/rss/rss.php?id=1014",
            "Reuters: Tech": "https://rss.app/feeds/U0pObtwFzbniWFsZ.xml",
            "Reuters: World Politics": "https://rss.app/feeds/hMAwZwfz5VFehf2a.xml",
            "Snopes: Politics": "https://rss.app/feeds/grUEfl6E3YpIZwlq.xml",
            "Vox: Politics": "http://www.vox.com/rss/politics/index.xml",
        }

    def get_feed(self, feed_name):
        feed = fp.parse(self.feeds[feed_name])
        
        # Sort entries by the 'published' field in descending order (most recent first)
        sorted_entries = sorted(
            feed.entries,
            key=lambda entry: date_parser.parse(entry.published),
            reverse=True
        )

        feed.entries = sorted_entries
        return feed

    def get_feed_names(self):
        return list(self.feeds.keys())
