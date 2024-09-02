# feeds.py
import feedparser as fp

class FeedManager:
    def __init__(self):
        self.feeds = {
            "The Atlantic Politics": "http://feeds.feedburner.com/AtlanticPoliticsChannel",
            "BBC U.S. Election": "https://rss.app/feeds/gn8XLqZTeImTjrmW.xml",
            "NPR Politics": "http://www.npr.org/rss/rss.php?id=1014",
            "Vox Politics": "http://www.vox.com/rss/politics/index.xml",
            "Washington Post Politics": "https://feeds.washingtonpost.com/rss/politics?itid=lk_inline_manual_2",
        }

    def get_feed(self, feed_name):
        return fp.parse(self.feeds[feed_name])

    def get_feed_names(self):
        return list(self.feeds.keys())
