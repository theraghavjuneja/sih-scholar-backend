from pydantic import BaseModel,Field
from typing import List
class WriterInfo(BaseModel):
    author_id:str
class CitationStats(BaseModel):
    all:int
    since2019:int
class Article(BaseModel):
    title:str
    authors:str
    publication:str
    cited_by:str=Field(alias="citedBy")
    year:str
    url:str
class CoAuthor(BaseModel):
    name:str
    affiliation:str
    email:str
class GraphData(BaseModel):
    year:int
    publications:int
class Stats(BaseModel):
    h_index: str = Field(alias="hIndex")
    i10_index: str = Field(alias="i10Index")
    citations: str
    documents: str
    citations_per_document: str = Field(alias="citationsPerDocument")
class AuthorProfile(BaseModel):
    scholar_id:str=Field(alias="scholaID")
    name:str
    affiliation:str
    veriied_email:str=Field(alias="verifiedEmail")
    interests: List[str]
    citation_stats: CitationStats = Field(alias="citationStats")
    articles: List[Article]
    co_authors: List[CoAuthor] = Field(alias="coAuthors")
    graph_data: List[GraphData] = Field(alias="graphData")
    ai_description: str = Field(alias="aiDescription")
    stats: Stats