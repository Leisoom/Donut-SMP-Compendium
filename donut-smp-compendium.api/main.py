from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

api_key = os.getenv("API_KEY")

@app.get("/", )
async def root():

    player = requests.get("https://api.donutsmp.net/v1/stats/leisoom",headers={'Authorization': f"Bearer {api_key}"});
    player_json = player.json()['result']

    return {'shards' : player_json['deaths']}