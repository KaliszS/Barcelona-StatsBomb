from fastapi import FastAPI
from app.src import competition, season, match
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(competition.router, prefix="/competition", tags=["Competition"])
app.include_router(season.router, prefix="/season", tags=["Season"])
app.include_router(match.router, prefix="/match", tags=["Match"])