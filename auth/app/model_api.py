from pydantic import BaseModel, Field, EmailStr


class RecipientData(BaseModel):
    id: str  # recipient id
    email: EmailStr
    priority: int = 1
    message_data: str


class ConfirmLetter(BaseModel):
    """Основная форма хранимого события"""

    sender_service: str = Field(default='auth_backend')
    event_name: str = 'welcome'
    event_type: str = 'email'
    description: str = Field(default='send a confirmation email')
    recipient_data: RecipientData | None
