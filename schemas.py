from pydantic import BaseModel

class AuthorCreate(BaseModel):
    name: str

class BookCreate(BaseModel):
    title: str