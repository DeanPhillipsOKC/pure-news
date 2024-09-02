import feedparser as fp
import streamlit as st
from bs4 import BeautifulSoup
import requests
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# AP: url =  "https://rss.app/feeds/SyIisu9HESEvayPf.xml"

feeds = {
    "BBC U.S. Election": "https://rss.app/feeds/gn8XLqZTeImTjrmW.xml",
    "Washington Post Politics": "https://feeds.washingtonpost.com/rss/politics?itid=lk_inline_manual_2"
}

def fetch_article_contents(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all('p')
    article_contents = ""
    for paragraph in paragraphs:
        article_contents += paragraph.get_text()
    return article_contents

def create_llm():
    return ChatOpenAI(model="gpt-4o")

def create_output_parser():
    return StrOutputParser()

def create_prompt_template():
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template("""
                                                      You are a news filter.  Take the text of the article and decompose it to a set of essential facts.
                                                      It should be as concise as possible while deliverying any important context.  There should be no hyperbole,
                                                      conjecture, cynicism, or bias.  A list of bullet points would be a good way to represent the filtered article.  
                                                      
                                                      Please also create a TL;DR summary that is about a paragraph long that summarizes the article concisely.

                                                      Please also include a summary of how a conservative might view this news.

                                                      Please also include a summary of how a liberal or progressive might view this news.

                                                      Please also include a summary of how a centrist, or impartial person might view this news.
                                                      
                                                      Please also rate the original article on a scale between 0 and 100.  0 is ultra left leaning.  100 is ultra right 
                                                      leaning.50 is perfectly unbiased.  Also include qualifying words such as slightly, moderately, or extremely
                                                      right or left leaning to help understand the score.

                                                      Please use markdown format for your output"""),
            HumanMessagePromptTemplate.from_template("\nArticle: {article}")
        ]
    )

    return chat_template

def get_filter_chain():
    prompt = create_prompt_template()
    llm = create_llm()
    output_parser = create_output_parser()

    chain = prompt | llm | output_parser

    return chain 

@st.cache_resource(ttl=86400)
def get_filtered_article(_chain, paragraphs):
    return _chain.invoke({"article": paragraphs})

def get_article_toggle_session_state_key_name(button_caption):
    return f'article_opened_{button_caption}'

def toggle_article_opened(button_caption):
    key = get_article_toggle_session_state_key_name(button_caption)
    st.session_state[key] = not st.session_state[key] 

def main():
    st.set_page_config(
        page_title="PureNews",
        page_icon="📰",
        layout="centered"
    )
 
    feed_name = st.sidebar.selectbox("Select a feed", list(feeds.keys()))

    feed_url = feeds[feed_name]

    feed = fp.parse(feed_url)

    chain = get_filter_chain()

    st.title("PureNews")

    # st.write([entry.title for entry in feed.entries])

    processed_titles = set()

    with st.empty():
        with st.container():

            for entry in feed.entries:

                if entry.title not in processed_titles:

                    button_state_key = get_article_toggle_session_state_key_name(entry.title)
                    # Create state for button
                    if button_state_key not in st.session_state:
                        st.session_state[button_state_key] = False

                    btn = st.button(f"{entry.title}", use_container_width=True, on_click=toggle_article_opened, args=(f'{entry.title}',))

                    processed_titles.add(entry.title)

                    if st.session_state[button_state_key]:
                        bar = st.progress(0)
                        paragraphs = fetch_article_contents(entry.link)
                        bar.progress(50)
                        filtered_article = get_filtered_article(chain, paragraphs)
                        bar.progress(100)
                        st.markdown(filtered_article)
                        st.markdown(f"[Original Article]({entry.link})")

if __name__ == "__main__":
    main()

