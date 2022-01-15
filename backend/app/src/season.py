from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import SeasonModel, UpdateSeasonModel
import json

router = APIRouter()
seasonsCollection = db["seasons"]
competitions_file_path = "app/data/competitions.json"

@router.post("/json", status_code=status.HTTP_201_CREATED)
async def add_seasons():

    with open(competitions_file_path) as file:
        seasons= json.load(file)
        for season in seasons:
            season_dict = {
                "_id": str(season["competition_id"]) + "." + str(season["season_id"]),
                "season_name": season["season_name"],
                "competition": season["competition_id"]
            }

            if await seasonsCollection.find_one({"_id": season_dict["_id"]}):
                continue
            else:
                await seasonsCollection.insert_one(season_dict)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Seasons added"})


@router.get(
    "/",
    response_description="List all seasons",
    response_model=List[SeasonModel],
)
async def get_all_seasons():
    seasons = await seasonsCollection.find().to_list(100)
    return seasons


@router.delete("/", response_description="Delete all seasons")
async def delete_all_seasons():
    await seasonsCollection.delete_many({})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Seasons deleted"})
