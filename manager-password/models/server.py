from typing import Optional
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import BaseModel, Field, GetJsonSchemaHandler

class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetJsonSchemaHandler):
        return {'type': 'string'}


class ServerBaseCreate(BaseModel):
    name: str
    hostname: str
    port: int
    username: str
    password: str
   


class ServerResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    hostname: str
    port: int
    username: str
    owner_id: PyObjectId
   

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}