from pydantic import BaseModel
class WriterInfo(BaseModel):
    author_id:str
class AuthorProfile(BaseModel):
    scholar_id:str
    name:str
    