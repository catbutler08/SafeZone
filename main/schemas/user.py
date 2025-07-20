from pydantic import BaseModel, EmailStr, Field

class UserIn(BaseModel):
    name: str
    email: EmailStr
    username: str = Field(...)
    password: str = Field(...)
    telephone: str

class UserOut(BaseModel):
    username: str
    name: str
    email: EmailStr
    role: str = "Protecter"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
