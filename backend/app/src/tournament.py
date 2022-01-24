from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import Competition, Season
from statsbombpy import sb

router = APIRouter()

@router.post("/competitions", status_code=status.HTTP_201_CREATED)
async def add_competitions():
    comp = sb.competitions().loc[:, ["competition_id", "competition_name", "country_name"]]
    with db.session() as session:
        cypher = ""
        for i in range(0, len(comp)):
            if comp.iloc[i]['competition_name'] in ["FA Women's Super League", "Women's World Cup"]:
                continue
            cypher += (
                f"MERGE ( :Competition {{"
                f"competition_id: {comp.iloc[i]['competition_id']}, "
                f"competition_name: '{comp.iloc[i]['competition_name']}', "
                f"country_name: '{comp.iloc[i]['country_name']}'"
                f"}}) "
            )

        
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Competitions added"})

@router.delete("/competitions", status_code=status.HTTP_200_OK)
async def delete_competitions():
    with db.session() as session:
        cypher = "MATCH (n :Competition) DETACH DELETE n"
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Competitions deleted"})

@router.post("/seasons", status_code=status.HTTP_201_CREATED)
async def add_seasons():
    comp = sb.competitions().loc[:, ["competition_id", "competition_name", "season_id", "season_name"]]
    with db.session() as session:
        cypher = ""
        for i in range(0, len(comp)):
            if comp.iloc[i]['competition_name'] in ["FA Women's Super League", "Women's World Cup"]:
                continue
            cypher += (
                f"MERGE ( :Season {{"
                f"competition_id: {comp.iloc[i]['competition_id']}, "
                f"season_id: {comp.iloc[i]['season_id']}, "
                f"season_name: '{comp.iloc[i]['season_name']}'"
                f"}}) "
            )

        
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Seasons added"})

@router.delete("/seasons", status_code=status.HTTP_200_OK)
async def delete_seasons():
    with db.session() as session:
        cypher = "MATCH (n :Season) DETACH DELETE n"
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Seasons deleted"})

@router.post("/seasons_in_competitions", status_code=status.HTTP_201_CREATED)
async def  seasons_in_competitions():
    with db.session() as session:
        cypher = (
            f"MATCH (s :Season), (c :Competition)"
            f"WHERE s.competition_id = c.competition_id "
            f"CREATE (s)-[:IS_PART_OF]->(c)"
        )

        session.run(query=cypher)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Seasons and competitions connected"})

