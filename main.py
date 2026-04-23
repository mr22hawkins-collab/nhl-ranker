import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from rank_players import rank_players

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.get("/players/centres")
def get_centres():
    centres, _, _ = rank_players()
    result = centres.sort_values("rank")[["rank", "name", "team", "position", "goals_per_60", "assists_per_60", "ixG_per_60", "xGFpct", "corsiPct", "plusMinus", "faceoffPct", "rank_score"]]
    return result.to_dict(orient="records")

@app.get("/players/wingers")
def get_wingers():
    _, wingers, _ = rank_players()
    result = wingers.sort_values("rank")[["rank", "name", "team", "position", "goals_per_60", "assists_per_60", "ixG_per_60", "xGFpct", "corsiPct", "plusMinus", "hits", "rank_score"]]
    return result.to_dict(orient="records")

@app.get("/players/defensemen")
def get_defensemen():
    _, _, defensemen = rank_players()
    result = defensemen.sort_values("rank")[["rank", "name", "team", "position", "goals_per_60", "assists_per_60", "ixG_per_60", "xGFpct", "corsiPct", "plusMinus", "blocks", "rank_score"]]
    return result.to_dict(orient="records")

@app.get("/players/{name}")
def get_player(name: str):
    centres, wingers, defensemen = rank_players()
    all_players = pd.concat([centres, wingers, defensemen])
    player = all_players[all_players["name"].str.lower() == name.lower()]
    if player.empty:
        return {"error": "Player not found"}
    return player.iloc[0].to_dict()