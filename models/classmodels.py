from pydantic import BaseModel,Field
from typing import List
class WriterInfo(BaseModel):
    author_id:str
class WriterInfo(BaseModel):
    author_id:str
class CitationStats(BaseModel):
    """
    All indicates total number of citations
    & since2019 indicates citations since 2019
    """
    all:int
    since2019:int

class Article(BaseModel):
    """
    title indicates, title of the article
    cited by indicates total citations in that publication
    year indicates when was that publication published

    """
    title:str
    cited_by:str
    year:str
class GraphData(BaseModel):
    """
    year indicates the year of a publication
    publications indicate total no of publication made in that year
    """
    year:int
    publications:int
class Stats(BaseModel):
    h_index: str
    i10_index: str
    citations: str
    publication: str


class AuthorProfile(BaseModel):
    name:str
    affiliation:str
    verified_email:str
    interests: List[str]
    citation_stats: CitationStats
    articles: List[Article]
    graph_data: List[GraphData]
    # ai_description: str = Field(alias="aiDescription")
    stats: Stats