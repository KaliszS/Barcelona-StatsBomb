from fastapi import FastAPI
from app.src import tournament, game, player
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

app.include_router(tournament.router, prefix="/tournament", tags=["Tournament"])
app.include_router(game.router, prefix="/game", tags=["Game"])
app.include_router(player.router, prefix="/player", tags=["Player"])
