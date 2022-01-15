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

#id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class TeamScoreModel(BaseModel):
    team: str
    score: int

class CompetitionModel(BaseModel):
    competition_id: int = Field(alias="_id")
    competition_name: str = Field(...)
    country_name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "16",
                "competition_name": "Champions League",
                "country_name": "Europe",
            }
        }


class UpdateCompetitionModel(BaseModel):
    competition_name: Optional[str]
    country_name: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "competition_name": "Champions League",
                "country_name": "Europe",
            }
        }

class SeasonModel(BaseModel):
    season_id: str = Field(alias="_id")
    season_name: str = Field(...)
    competition: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "16.1",
                "season_name": "2017/2018",
                "competition": "16",
            }
        }


class UpdateSeasonModel(BaseModel):
    season_name: Optional[str]
    country_name: Optional[str]
    competition: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "season_name": "2017/2018",
                "competition": {"$ref": "competitions", "$id": "16"},
            }
        }

class MatchModel(BaseModel):
    match_id: int = Field(alias="_id")
    home: TeamScoreModel = Field(...)
    away: TeamScoreModel = Field(...)
    competition: int = Field(...)
    season: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "266989",
                "home": {"team": "FC Barcelona", "score": 3},
                "away": {"team": "Real Madrid", "score": 1},
                "competition": "11",
                "season": "11.2",
            }
        }
