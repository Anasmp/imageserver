from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str 
    password:str
    class Config:
        orm_mode = True
        allow_population_by_field_name = True