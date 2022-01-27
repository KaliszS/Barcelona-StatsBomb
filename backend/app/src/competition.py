from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import CompetitionModel, UpdateCompetitionModel
import json
from statsbombpy import sb

router = APIRouter()
competitionsCollection = db["competitions"]

@router.post("/competitions", status_code=status.HTTP_201_CREATED)
async def add_competitions():
    comp = sb.competitions().loc[:, ["competition_id", "competition_name", "country_name"]]
    for i in range(0, len(comp)):
            if comp.iloc[i]['competition_name'] in ["FA Women's Super League", "Women's World Cup"]:
                continue

            comp_dict = {
                "_id": int(comp.iloc[i]["competition_id"]),
                "competition_name": comp.iloc[i]["competition_name"],
                "country_name": comp.iloc[i]["country_name"]
            }

            if await competitionsCollection.find_one({"_id": comp_dict["_id"]}):
                continue
            else:
                await competitionsCollection.insert_one(comp_dict)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Competitions added"})


@router.get("/",)
async def get_all_competitions():
    competitions = await competitionsCollection.find().to_list(100)
    return competitions


@router.delete("/", response_description="Delete all competitions")
async def delete_all_competitions():
    await competitionsCollection.delete_many({})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "All competitions deleted"})
