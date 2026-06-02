from pydantic import BaseModel


class InteractionResponse(BaseModel):
    status: str
