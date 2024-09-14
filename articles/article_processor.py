import requests
from bs4 import BeautifulSoup
import streamlit as st

class ArticleProcessor:
    @staticmethod
    @st.cache_resource
    def fetch_article_contents(url):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        paragraphs = soup.find_all('p')
        article_contents = "".join(paragraph.get_text() for paragraph in paragraphs)
        return article_contents