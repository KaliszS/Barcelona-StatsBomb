from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import CompetitionModel, UpdateCompetitionModel
import json

router = APIRouter()
competitionsCollection = db["competitions"]
competitions_file_path = "app/data/competitions.json"

@router.post("/competitions", status_code=status.HTTP_201_CREATED)
async def add_competitions():

    with open(competitions_file_path) as file:
        competitions= json.load(file)
        for competition in competitions:
            comp_dict = {
                "competition_id": competition["competition_id"],
                "season_id": competition["season_id"],
                "competition_name": competition["competition_name"],
                "country_name": competition["country_name"],
                "season_name": competition["season_name"]}
            competitionsCollection.insert_one(comp_dict)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Competitions added"})

@router.post(
    "/",
    response_description="Create a new competition",
    response_model=CompetitionModel,
)
async def create_competition(competition: CompetitionModel = Body(...)):
    competition = jsonable_encoder(competition)
    new_competition = await competitionsCollection.insert_one(competition)
    created_competition = await competitionsCollection.find_one(
        {"_id": new_competition.inserted_id}
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=created_competition
    )


@router.get(
    "/",
    response_description="List all competitions",
    response_model=List[CompetitionModel],
)
async def get_all_competitions():
    competitions = await competitionsCollection.find().to_list(100)
    return competitions


@router.get(
    "/{season_id}",
    response_description="Get a competition season by id",
    response_model=CompetitionModel,
)
async def get_competition(season_id: int):
    if competition := await competitionsCollection.find_one({"season_id": season_id}):
        return competition

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Competition season with id {season_id} not found",
    )


@router.put(
    "/{season_id}",
    response_description="Update a competition season by id",
    response_model=CompetitionModel,
)
async def update_competition(
    season_id: int, competition: UpdateCompetitionModel = Body(...)
):
    if competition := await competitionsCollection.find_one_and_update(
        {"season_id": season_id}, {"$set": competition}, return_document=True
    ):
        return competition

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Competition season with id {season_id} not found",
    )


@router.delete("/{season_id}", response_description="Delete a competition season by id")
async def delete_competition(season_id: int):
    if competition := await competitionsCollection.find_one_and_delete(
        {"season_id": season_id}
    ):
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Competition season with id {season_id} not found",
    )
