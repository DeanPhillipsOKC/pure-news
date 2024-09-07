from pydantic import BaseModel, Field

class ArticleInsights(BaseModel):
    tldr: str = Field(description="The TL;DR summary of an article")
    essential_facts: str = Field(description="A markdown formatted bulletted list of the articles essential facts.")
    link: str = Field(description="A link to the original article.")