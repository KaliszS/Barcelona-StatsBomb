from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import Match
from statsbombpy import sb

router = APIRouter()

@router.post("/{competition_id}/{season_id}/matches", status_code=status.HTTP_201_CREATED)
async def add_games(competition_id, season_id):
    games = sb.matches(competition_id=competition_id, season_id=season_id).loc[:, ["match_id", "match_date", "home_team", "away_team", "home_score", "away_score", "competition_stage"]]
    with db.session() as session:
        cypher = ""
        for i in range(0, len(games)):
            cypher += (
                f"MERGE ( :Match {{"
                f"match_id: {games.iloc[i]['match_id']}, "
                f"match_date: date('{games.iloc[i]['match_date']}'), "
                f"home_team: '{games.iloc[i]['home_team']}', "
                f"away_team: '{games.iloc[i]['away_team']}', "
                f"home_score: {games.iloc[i]['home_score']}, "
                f"away_score: {games.iloc[i]['away_score']}, "
                f"competition_id: {competition_id}, "
                f"competition_stage: '{games.iloc[i]['competition_stage']}', "
                f"season_id: {season_id}"
                f"}}) "
            )
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Matches added"})

@router.delete("/matches", status_code=status.HTTP_200_OK)
async def delete_games():
    with db.session() as session:
        cypher = "MATCH (n :Match) DETACH DELETE n"
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Matches deleted"})

@router.post("/matches_in_seasons", status_code=status.HTTP_201_CREATED)
async def  matches_in_seasons():
    with db.session() as session:
        cypher = (
            f"MATCH (s :Season), (m :Match)"
            f"WHERE s.season_id = m.season_id AND s.competition_id = m.competition_id "
            f"CREATE (s)<-[:WAS_PLAYED_IN]-(m)"
        )

        session.run(query=cypher)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Seasons and matches connected"})