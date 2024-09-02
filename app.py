import feedparser as fp
import streamlit as st
from bs4 import BeautifulSoup
import requests
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# AP: url =  "https://rss.app/feeds/SyIisu9HESEvayPf.xml"

url = "https://rss.app/feeds/gn8XLqZTeImTjrmW.xml"

feed = fp.parse(url)

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
                                                      You are a news filter.  Take the text of the article and decompose it to a set of facts.
                                                      It should be as concise as possible while giving the full story.  There should be no hyperbole,
                                                      conjecture, cynicism, or bias.  It should just be the facts as reported in a police report.  If
                                                      an opinion is needed to get the full story (e.g. an eye whitness account) then it should be very
                                                      clear that it is an opinion, and not a fact.  A list of bullet points would be a good way to 
                                                      represent the filtered article.  
                                                      
                                                      Please include a score at the end of the summary that indicates
                                                      the amount of vitriole, cynicism, or partisan language used in the original article.  It should be 
                                                      greated using standard A, B, C, D, and F where A is the best and F is very irresponsible journalism.  
                                                      After the score include a very concise rationale for why you picked that score.  Remember you are
                                                      grading the original article and not your summary.  
                                                      
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

@st.cache_resource
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
 
    chain = get_filter_chain()

    for entry in feed.entries:

        button_state_key = get_article_toggle_session_state_key_name(entry.title)
        # Create state for button
        if button_state_key not in st.session_state:
            st.session_state[button_state_key] = False

        btn = st.button(f"{entry.title}", use_container_width=True, on_click=toggle_article_opened, args=(f'{entry.title}',))
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

