from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CompetitionModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    competition_id: int = Field(...)
    season_id: int = Field(...)
    competition_name: str = Field(...)
    country_name: str = Field(...)
    season_name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "competition_id": "16",
                "season_id": "4",
                "competition_name": "Champions League",
                "country_name": "Europe",
                "season_name": "2018/2019",
            }
        }


class UpdateCompetitionModel(BaseModel):
    competition_id: Optional[int]
    season_id: Optional[int]
    competition_name: Optional[str]
    country_name: Optional[str]
    season_name: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "competition_id": "16",
                "season_id": "4",
                "competition_name": "Champions League",
                "country_name": "Europe",
                "season_name": "2018/2019",
            }
        }
