# llm_utils.py
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

class LLMManager:
    def __init__(self):
        self.llm = self.create_llm()
        self.output_parser = self.create_output_parser()
        self.prompt_template = self.create_prompt_template()
        self.chain = self.create_filter_chain()

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

                    Please use markdown format for your output"""
                                                          ),
                HumanMessagePromptTemplate.from_template("\nArticle: {article}")
            ]
        )
        return chat_template

    def create_filter_chain(self):
        return self.prompt_template | self.llm | self.output_parser
    
    @st.cache_resource(ttl=86400)
    def get_filtered_article(_self, paragraphs):
        return _self.chain.invoke({"article": paragraphs})
