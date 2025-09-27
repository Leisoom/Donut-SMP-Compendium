from fastapi import FastAPI,HTTPException
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

api_key = os.getenv("API_KEY")

@app.get("/player/{player_name}", )
async def display_player_stats(player_name : str):

        data = requests.get(f"https://api.donutsmp.net/v1/stats/{player_name}",headers={'Authorization': f"Bearer {api_key}"}).json()
        
        if(data["status"] == 500):
           raise HTTPException(status_code=404, detail="player not found")
        
        player_json = data['result']
        platform = "bedrock" if player_name.startswith(".") else "java"

        player_response = {};
        player_response["name"] = player_name
        player_response["platform"] = platform
        player_response["broken_blocks"] = player_json['broken_blocks']
        player_response["deaths"] = player_json['deaths']
        player_response["kills"] = player_json['kills']
        player_response["mobs_killed"] = player_json['mobs_killed']
        player_response["money"] = player_json['money']
        player_response["money_made_from_sell"] = player_json['money_made_from_sell']
        player_response["money_spent_on_shop"] = player_json['money_spent_on_shop']
        player_response["placed_blocks"] = player_json['placed_blocks']
        player_response["playtime"] = player_json['playtime']
        player_response["shards"] = player_json['shards']

        return player_response