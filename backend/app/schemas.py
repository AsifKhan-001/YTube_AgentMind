from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChatRequest(BaseModel):
    youtube_url: str
    message: str  # can be a question, "generate notes", or "make flashcards" — the graph decides

class ChatResponse(BaseModel):
    answer: str
    pdf_download_url: Optional[str] = None
    flashcards: Optional[list] = None