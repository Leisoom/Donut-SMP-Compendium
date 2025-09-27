from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

api_key = os.getenv("API_KEY")

class Player(BaseModel):
    name: str
    platform: str
    broken_blocks: int
    deaths: int
    kills: int
    mobs_killed: int
    money: float
    money_made_from_sell: float
    money_spent_on_shop: int
    placed_blocks: int
    playtime: int
    shards: int

@app.get("/leaderboard/{page_number}", )
async def display_leaderboard_by_page(page_number: int):
    data = requests.get(f"https://api.donutsmp.net/v1/leaderboards/money/{page_number}",headers={'Authorization': f"Bearer {api_key}"}).json()

    player_list = []

    for player in data['result']:
        player_data = requests.get(f"https://api.donutsmp.net/v1/stats/{player['username']}",headers={'Authorization': f"Bearer {api_key}"}).json()

        player_json = player_data['result']
        platform = "bedrock" if player['username'].startswith(".") else "java"

        player_response = Player(
            name = player['username'], 
            platform=platform,
            broken_blocks= player_json['broken_blocks'],
            deaths=player_json['deaths'],
            kills=player_json['kills'],
            mobs_killed=player_json['mobs_killed'],
            money= player_json['money'],
            money_made_from_sell= player_json['money_made_from_sell'],
            money_spent_on_shop= player_json['money_spent_on_shop'],
            placed_blocks=player_json['placed_blocks'],
            playtime=player_json['playtime'],
            shards=player_json['shards']
        )

        player_list.append(player_response)

    return player_list

@app.get("/player/{player_name}", response_model=Player)
async def display_player_stats(player_name : str,):
    data = requests.get(f"https://api.donutsmp.net/v1/stats/{player_name}",headers={'Authorization': f"Bearer {api_key}"}).json()
    
    if(data["status"] == 500):
        raise HTTPException(status_code=404, detail="player not found")
    
    player_json = data['result']
    platform = "bedrock" if player_name.startswith(".") else "java"

    player_response = Player(
            name = player_name, 
            platform=platform,
            broken_blocks= player_json['broken_blocks'],
            deaths=player_json['deaths'],
            kills=player_json['kills'],
            mobs_killed=player_json['mobs_killed'],
            money= player_json['money'],
            money_made_from_sell= player_json['money_made_from_sell'],
            money_spent_on_shop= player_json['money_spent_on_shop'],
            placed_blocks=player_json['placed_blocks'],
            playtime=player_json['playtime'],
            shards=player_json['shards']
            )

    return player_response