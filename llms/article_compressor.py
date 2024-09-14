# llm_utils.py
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

class ArticleCompressor:
    def __init__(self):
        self.llm = self._create_llm()
        self.output_parser = self._create_output_parser()
        self.prompt_template = self._create_prompt_template()
        self.chain = self._create_filter_chain()

    def _create_llm(self):
        return ChatOpenAI(temperature=0)

    def _create_output_parser(self):
        return StrOutputParser()

    def _create_prompt_template(self):
        chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template("""
                    You are a news compressor.  Take the article and get rid of as many characters / tokens as possible
                    without changing the meaning, or omitting any important information.  You can eliminate unnecessary prose,
                    use smaller synonyms, etc."""
                                                          ),
                HumanMessagePromptTemplate.from_template("\nArticle: {article}")
            ]
        )
        return chat_template

    def _create_filter_chain(self):
        return self.prompt_template | self.llm | self.output_parser
    
    @st.cache_resource(ttl=86400)
    def get_compressed_article(_self, paragraphs):
        print(f'Character count before compression: {len(paragraphs)}')
        compressed_article = _self.chain.invoke({"article": paragraphs})
        print(f'Character count after compression: {len(compressed_article)}')
        print(f'Compression rate: {round((len(compressed_article) / len(paragraphs)) * 100, 2)}%')

        return compressed_article