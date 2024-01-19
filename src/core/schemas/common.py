from pydantic import BaseModel


class ExceptionResponse(BaseModel):
    detail: str


class LoginInput(BaseModel):
    google_token: str
    role: str | None = None


class LoginOutput(BaseModel):
    token: str
