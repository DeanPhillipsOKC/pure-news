import requests
from bs4 import BeautifulSoup
import streamlit as st

class ArticleProcessor:
    @staticmethod
    @st.cache_resource
    def fetch_article_contents(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        article_contents = "".join(paragraph.get_text() for paragraph in paragraphs)
        return article_contents