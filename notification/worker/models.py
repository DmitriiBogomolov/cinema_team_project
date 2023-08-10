from pydantic import BaseModel, EmailStr


class EmailNewsletter(BaseModel):
    id: str
    email: EmailStr
    event_name: str
