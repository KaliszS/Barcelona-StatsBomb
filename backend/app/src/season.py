from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import SeasonModel, UpdateSeasonModel
import json
from statsbombpy import sb

router = APIRouter()
seasonsCollection = db["seasons"]

@router.post("/json", status_code=status.HTTP_201_CREATED)
async def add_seasons():
    comp = sb.competitions().loc[:, ["competition_id", "competition_name", "season_id", "season_name"]]
    for i in range(0, len(comp)):
        if comp.iloc[i]['competition_name'] in ["FA Women's Super League", "Women's World Cup"]:
            continue

        season_dict = {
            "_id": str(comp.iloc[i]["competition_id"]) + "." + str(comp.iloc[i]["season_id"]),
            "season_name": comp.iloc[i]["season_name"],
            "competition": int(comp.iloc[i]["competition_id"])
        }

        if await seasonsCollection.find_one({"_id": season_dict["_id"]}):
            continue
        else:
            await seasonsCollection.insert_one(season_dict)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Seasons added"})


@router.get("/",)
async def get_all_seasons():
    seasons = await seasonsCollection.find().to_list(100)
    return seasons


@router.delete("/", response_description="Delete all seasons")
async def delete_all_seasons():
    await seasonsCollection.delete_many({})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Seasons deleted"})
