from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import MatchModel
import json
from statsbombpy import sb

router = APIRouter()
matchCollection = db["matches"]

@router.post("/{competition_id}/{season_id}/matches", status_code=status.HTTP_201_CREATED)
async def add_matches(competition_id, season_id):
    games = sb.matches(competition_id=competition_id, season_id=season_id).loc[:, ["match_id", "match_date", "home_team", "away_team", "home_score", "away_score", "competition_stage"]]
    for i in range(0, len(games)):
        match_dict = {
            "_id": int(games.iloc[i]["match_id"]),
            "match_date": games.iloc[i]["match_date"],
            "home": {"team": games.iloc[i]["home_team"], "score": int(games.iloc[i]["home_score"])},
            "away": {"team": games.iloc[i]["away_team"], "score": int(games.iloc[i]["away_score"])},
            "competition": int(competition_id),
            "competition_stage": games.iloc[i]["competition_stage"],
            "season": str(competition_id) + "." + str(season_id)
        }

        if await matchCollection.find_one({"_id": match_dict["_id"]}):
            continue
        else:
            await matchCollection.insert_one(match_dict)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Matches added"})

@router.get("/", response_description="List all matches", response_model=List[MatchModel])
async def get_all_matches():
    matches = await matchCollection.find().to_list(100)
    return matches

@router.delete("/", response_description="Delete all matches")
async def delete_all_matches():
    await matchCollection.delete_many({})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Matches deleted"})
