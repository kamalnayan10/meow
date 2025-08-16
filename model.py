from pydantic import BaseModel

class Response(BaseModel):
    command: str
    description: list[str]