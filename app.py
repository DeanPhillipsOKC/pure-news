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

    def get_article_toggle_session_state_key_name(self, button_caption):
        return f'article_opened_{button_caption}'

    def toggle_article_opened(self, button_caption):
        key = self.get_article_toggle_session_state_key_name(button_caption)
        st.session_state[key] = not st.session_state[key] 

    def main(self):
        st.set_page_config(
            page_title="PureNews",
            page_icon="📰",
            layout="wide"
        )

        feed_name = st.sidebar.selectbox("Select a feed", list(self.feed_manager.get_feed_names()))

        feed = self.feed_manager.get_feed(feed_name)

        st.markdown(
            """
        <style>
            button .st-emotion-cache-1sy6v2f {
                justify-content: left;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.title("PureNews")
        processed_titles = set()

        with st.empty():
            with st.container():

                for entry in feed.entries:

                    if entry.title not in processed_titles:

                        button_state_key = self.get_article_toggle_session_state_key_name(entry.title)
                        # Create state for button
                        if button_state_key not in st.session_state:
                            st.session_state[button_state_key] = False

                        with stylable_container(
                            key="button_left_align_text",
                            css_styles="""
                                button {
                                    justify-content: left;
                                }"""
                        ):
                            btn = st.button(f"{entry.title}", use_container_width=True, on_click=self.toggle_article_opened, args=(f'{entry.title}',))

                        processed_titles.add(entry.title)

                        if st.session_state[button_state_key]:
                            bar = st.progress(0)
                            paragraphs = self.article_processor.fetch_article_contents(entry.link)
                            bar.progress(50)
                            filtered_article = self.llm_manager.get_filtered_article(paragraphs)
                            bar.progress(100)
                            st.markdown("#### TL/DR")
                            st.markdown(filtered_article.tldr)
                            
                            st.markdown("#### Essential Facts")
                            st.markdown(filtered_article.essential_facts)

                            st.markdown(f"[Original Article]({entry.link})")

if __name__ == "__main__":
    app = PureNewsApp()
    app.main()

