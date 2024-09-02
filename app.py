import feedparser as fp
import streamlit as st
from bs4 import BeautifulSoup
import requests
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from feeds import FeedManager

# AP: url =  "https://rss.app/feeds/SyIisu9HESEvayPf.xml"

class PureNewsApp:

    def __init__(self) -> None:
        self.feed_manager = FeedManager()

    def fetch_article_contents(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        article_contents = ""
        for paragraph in paragraphs:
            article_contents += paragraph.get_text()
        return article_contents

    def create_llm(self):
        return ChatOpenAI(model="gpt-4o")

    def create_output_parser(self):
        return StrOutputParser()

    def create_prompt_template(self):
        chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template("""
                                                        You are a news filter.  Take the text of the article and decompose it to a set of essential facts.
                                                        It should be as concise as possible while deliverying any important context.  There should be no hyperbole,
                                                        conjecture, cynicism, or bias.  A list of bullet points would be a good way to represent the filtered article.  
                                                        
                                                        Please also create a TL;DR summary that is about a paragraph long that summarizes the article concisely.

                                                        If this is a political post, please also include a fictional take on the article from a fictional conversative
                                                        named Connie.  She is an intellectually honest, highly educated conservative that is very well informed.

                                                        If this is a political post, please also include a fictional take on the article from a fictional liberal
                                                        named Libby.  She is an intellectually honest, highly educated progressive that is very well informed.

                                                        If this is a political post, please also include a fictional take on the article from a fictional moderate
                                                        named Newt.  He is an intellectually honest, highly educated moderate that is very well informed.

                                                        Please use markdown format for your output"""),
                HumanMessagePromptTemplate.from_template("\nArticle: {article}")
            ]
        )

        return chat_template

    def get_filter_chain(self):
        prompt = self.create_prompt_template()
        llm = self.create_llm()
        output_parser = self.create_output_parser()

        chain = prompt | llm | output_parser

        return chain 

    @st.cache_resource(ttl=86400)
    def get_filtered_article(self, _chain, paragraphs):
        return _chain.invoke({"article": paragraphs})

    def get_article_toggle_session_state_key_name(self, button_caption):
        return f'article_opened_{button_caption}'

    def toggle_article_opened(self, button_caption):
        key = self.get_article_toggle_session_state_key_name(button_caption)
        st.session_state[key] = not st.session_state[key] 

    def main(self):
        st.set_page_config(
            page_title="PureNews",
            page_icon="📰",
            layout="centered"
        )

        feed_name = st.sidebar.selectbox("Select a feed", list(self.feed_manager.get_feed_names()))

        feed_url = self.feed_manager.get_feed(feed_name)

        feed = fp.parse(feed_url)

        chain = self.get_filter_chain()

        st.title("PureNews")

        # st.write([entry.title for entry in feed.entries])

        processed_titles = set()

        with st.empty():
            with st.container():

                for entry in feed.entries:

                    if entry.title not in processed_titles:

                        button_state_key = self.get_article_toggle_session_state_key_name(entry.title)
                        # Create state for button
                        if button_state_key not in st.session_state:
                            st.session_state[button_state_key] = False

                        btn = st.button(f"{entry.title}", use_container_width=True, on_click=self.toggle_article_opened, args=(f'{entry.title}',))

                        processed_titles.add(entry.title)

                        if st.session_state[button_state_key]:
                            bar = st.progress(0)
                            paragraphs = self.fetch_article_contents(entry.link)
                            bar.progress(50)
                            filtered_article = self.get_filtered_article(chain, paragraphs)
                            bar.progress(100)
                            st.markdown(filtered_article)
                            st.markdown(f"[Original Article]({entry.link})")

if __name__ == "__main__":
    app = PureNewsApp()
    app.main()

