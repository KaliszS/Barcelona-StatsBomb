from typing import Optional
from pydantic import BaseModel
from datetime import date

class Competition(BaseModel):
    competition_id: int
    competition_name: str
    country_name: str

class Season(BaseModel):
    competition_id: int
    season_id: int
    season_name: str

class Country(BaseModel):
    country_id: int
    country_name: str

class Team(BaseModel):
    team_id: int
    team_name: str
    country_id: int

class Player(BaseModel):
    player_id: int
    player_nickname: str

class Match(BaseModel):
    match_id: int
    season_id: int
    competition_id: int
    match_date: date
    home_team: int
    away_team: int
    home_score: int
    away_score: int
    competition_stage: str


