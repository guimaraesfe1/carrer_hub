from pydantic import BaseModel


class InscriptionUpdateSchema(BaseModel):
    why: str


class InscriptionCreateSchema(BaseModel):
    why: str
