import feedparser as fp
from dateutil import parser as date_parser

class FeedManager:
    def __init__(self):
        self.feeds = {
            "The Atlantic Politics": "http://feeds.feedburner.com/AtlanticPoliticsChannel",
            "BBC U.S. Election": "https://rss.app/feeds/gn8XLqZTeImTjrmW.xml",
            "NPR News": "http://www.npr.org/rss/rss.php?id=1001",
            "NPR Politics": "http://www.npr.org/rss/rss.php?id=1014",
            "Vox Politics": "http://www.vox.com/rss/politics/index.xml",
            "Washington Post Politics": "https://feeds.washingtonpost.com/rss/politics?itid=lk_inline_manual_2",
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
