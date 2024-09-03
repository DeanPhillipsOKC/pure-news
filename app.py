from typing import Set
import streamlit as st
from feeds import FeedManager
from articles import ArticleProcessor
from llms import LLMManager
from streamlit_extras.stylable_container import stylable_container

# AP: url =  "https://rss.app/feeds/SyIisu9HESEvayPf.xml"

class PureNewsApp:

    def __init__(self) -> None:
        self.feed_manager = FeedManager()
        self.article_processor = ArticleProcessor()
        self.llm_manager = LLMManager()
        self.processed_titles: Set[str] = set()

    def _get_article_toggle_session_state_key_name(self, button_caption):
        return f'article_opened_{button_caption}'

    def _toggle_article_opened(self, button_caption):
        key = self._get_article_toggle_session_state_key_name(button_caption)
        st.session_state[key] = not st.session_state[key] 

    def _initialize_button_state(self, entry_title: str) -> None:
        button_state_key = self._get_article_toggle_session_state_key_name(entry_title)
        if button_state_key not in st.session_state:
            st.session_state[button_state_key] = False

    def _load_article_insights(self, feed_entry):
        bar = st.progress(0)
        paragraphs = self.article_processor.fetch_article_contents(feed_entry.link)
        bar.progress(50)
        filtered_article = self.llm_manager.get_filtered_article(paragraphs)
        bar.progress(100)
        st.markdown("#### TL/DR")
        st.markdown(filtered_article.tldr)
        
        st.markdown("#### Essential Facts")
        st.markdown(filtered_article.essential_facts)

        st.markdown(f"[Original Article]({feed_entry.link})")

    def _was_article_already_added(self, article_title):
        return article_title in self.processed_titles

    def _display_feed_entry(self, feed_entry):
        if self._was_article_already_added(feed_entry.title):
            return

        self._initialize_button_state(feed_entry.title)

        with stylable_container(
            key="button_left_align_text",
            css_styles="button { justify-content: left; }"
        ):
            st.button(
                f"{feed_entry.title}", 
                use_container_width=True, 
                on_click=self._toggle_article_opened, 
                args=(feed_entry.title,)
            )

        self.processed_titles.add(feed_entry.title)

        if st.session_state[self._get_article_toggle_session_state_key_name(feed_entry.title)]:
            self._load_article_insights(feed_entry)

    def main(self):
        st.set_page_config(page_title="PureNews", page_icon="📰", layout="wide")
        st.title("PureNews")

        feed_name = st.sidebar.selectbox("Select a feed", list(self.feed_manager.get_feed_names()))
        feed = self.feed_manager.get_feed(feed_name)

        for entry in feed.entries:
            self._display_feed_entry(entry)

if __name__ == "__main__":
    app = PureNewsApp()
    app.main()

