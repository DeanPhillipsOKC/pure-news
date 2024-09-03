import requests
from bs4 import BeautifulSoup
import streamlit as st
from pydantic import BaseModel, Field

class ArticleProcessor:
    @staticmethod
    @st.cache_resource
    def fetch_article_contents(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        article_contents = "".join(paragraph.get_text() for paragraph in paragraphs)
        return article_contents

class ArticleInsights(BaseModel):
    tldr: str = Field(description="The TL;DR summary of an article")
    essential_facts: str = Field(description="A markdown formatted bulletted list of the articles essential facts.")
    link: str = Field(description="A link to the original article.")