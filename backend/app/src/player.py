from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional, List
from app.utils.db import db
from app.utils.schema import Country, Team, Player
from statsbombpy import sb

router = APIRouter()

@router.post("/players", status_code=status.HTTP_201_CREATED)
async def add_players_from_all_matches():
    data = []
    with db.session() as session:
        cypher = f"MATCH (m :Match) RETURN m.match_id as match"
        result = session.run(query=cypher)
        data = result.data()

    for i in range(0, len(data)):
        await add_players(data[i]['match'])

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Players added"})

      # with db.session() as session:
    #     cypher = f"MATCH (s :Season) RETURN s.season_id as season, s.competition_id as competition"
    #     result = session.run(query=cypher)
    #     data = result.data()
        
    # return [list(d.values()) for d in data]

@router.post("/{match_id}/players", status_code=status.HTTP_201_CREATED)
async def add_players(match_id):
    players = sb.lineups(match_id=match_id)["Barcelona"].loc[:, ["player_id", "player_name", "country"]]
    with db.session() as session:
        cypher = ""
        for i in range(0, len(players)):
            cypher += (
                f"MERGE ( :Player {{"
                f"player_id: {players.iloc[i]['player_id']}, "
                f"player_name: '{players.iloc[i]['player_name']}', "
                f"team: '{'Barcelona'}', "
                f"country: '{players.iloc[i]['country']}'"
                f"}}) "
            )
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Players added"})

@router.delete("/players", status_code=status.HTTP_200_OK)
async def delete_players():
    with db.session() as session:
        cypher = "MATCH (n :Player) DETACH DELETE n"
        session.run(query=cypher)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Players deleted"})

@router.post("/players_in_teams", status_code=status.HTTP_201_CREATED)
async def players_in_teams():
    with db.session() as session:
        cypher = (
            f"MATCH (p :Player), (t :Team)"
            f"WHERE p.team = t.team_name "
            f"CREATE (t)<-[:PLAYS_FOR]-(p)"
        )

        session.run(query=cypher)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Players and teams connected"})

@router.post("/{match_id}/dribbles", status_code=status.HTTP_201_CREATED)
async def add_dribbles(match_id):
    events = sb.events(match_id=match_id, split=True, flatten_attrs=False)["dribbles"].loc[:, ["player", "team", "minute"]]
    with db.session() as session:
        cypher = ""
        for i in range(0, len(events)):
            cypher = (
                f"MATCH (p :Player), (m :Match) "
                f"WHERE p.player_name = '{events.iloc[i]['player']}' AND m.match_id = {match_id} "
                f"CREATE (p)-[:DRIBLLES {{"
                f"team: '{events.iloc[i]['team']}', "
                f"minute: {events.iloc[i]['minute']}"
                f"}}]->(m) "
            )
            session.run(query=cypher)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Dribbles added"})

@router.post("/{match_id}/shots", status_code=status.HTTP_201_CREATED)
async def add_shots(match_id):
    events = sb.events(match_id=match_id, split=True, flatten_attrs=False)["shots"].loc[:, ["player", "team", "minute"]]
    with db.session() as session:
        cypher = ""
        for i in range(0, len(events)):
            cypher = (
                f"MATCH (p :Player), (m :Match) "
                f"WHERE p.player_name = '{events.iloc[i]['player']}' AND m.match_id = {match_id} "
                f"CREATE (p)-[:SHOTS {{"
                f"team: '{events.iloc[i]['team']}', "
                f"minute: {events.iloc[i]['minute']}"
                f"}}]->(m) "
            )
            session.run(query=cypher)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Shots added"})

@router.post("/{match_id}/passes", status_code=status.HTTP_201_CREATED)
async def add_passes(match_id):
    events = sb.events(match_id=match_id, split=True, flatten_attrs=False)["dribbles"].loc[:, ["player", "team", "minute"]]
    with db.session() as session:
        cypher = ""
        for i in range(0, len(events)):
            cypher = (
                f"MATCH (p :Player), (m :Match) "
                f"WHERE p.player_name = '{events.iloc[i]['player']}' AND m.match_id = {match_id} "
                f"CREATE (p)-[:PASSES {{"
                f"team: '{events.iloc[i]['team']}', "
                f"minute: {events.iloc[i]['minute']}"
                f"}}]->(m) "
            )
            session.run(query=cypher)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Passes added"})

@router.post("/{match_id}/events")
async def add_events(match_id):
    await add_passes(match_id)
    await add_dribbles(match_id)
    await add_shots(match_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Events added"})