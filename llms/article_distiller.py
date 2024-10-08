# llm_utils.py
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
import streamlit as st
from articles import ArticleInsights

class ArticleDistiller:
    def __init__(self):
        self.llm = self._create_llm()
        self.output_parser = self._create_output_parser()
        self.prompt_template = self._create_prompt_template()
        self.chain = self._create_filter_chain()

    def _create_llm(self):
        return ChatOpenAI(model="gpt-4o")

    def _create_output_parser(self):
        return PydanticOutputParser(pydantic_object=ArticleInsights)

    def _create_prompt_template(self):
        chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template("""
                    You are a news filter.  Take the text of the article and decompose it to a set of individual facts.
                    There should be no hyperbole, conjecture, cynicism, or bias.  A list of bullet points would be a good way 
                    to represent the filtered article.
                    
                    Please also create a TL;DR summary that is about a paragraph long that summarizes the article concisely."""
                                                          ),
                HumanMessagePromptTemplate.from_template("\nArticle: {article}\n\nFormat Instructions: {format_instructions}")
            ]
        )
        return chat_template

    def _create_filter_chain(self):
        return self.prompt_template | self.llm | self.output_parser
    
    @st.cache_resource(ttl=86400)
    def get_filtered_article(_self, paragraphs):
        return _self.chain.invoke({"article": paragraphs, "format_instructions": _self.output_parser.get_format_instructions()})
