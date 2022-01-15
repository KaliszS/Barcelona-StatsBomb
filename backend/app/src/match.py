from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import MatchModel
import json

router = APIRouter()
matchCollection = db["matches"]
matches_file_path = "app/data/11/"
seasons = [1, 2, 4, 21, 22, 23, 24, 25, 26, 27, 27, 38, 39, 40, 41, 42, 90]

@router.post("/json", status_code=status.HTTP_201_CREATED)
async def add_matches():

    for s in seasons:
        with open(matches_file_path + str(s) + ".json") as file:
            matches= json.load(file)
            for match in matches:
                match_dict = {
                    "_id": ,
                    "home": {"team": match["home_team"]["home_team_name"], "score": match["home_score"]},
                    "away": {"team": match["away_team"]["away_team_name"], "score": match["away_score"]},
                    "competition": match["competition"]["competition_id"],
                    "season": str(match["competition"]["competition_id"]) + "." + str(match["season"]["season_id"])
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
