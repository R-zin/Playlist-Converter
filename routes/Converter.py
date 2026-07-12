from uuid import uuid4
from celery.result import AsyncResult
from fastapi import APIRouter,HTTPException,Depends
from services.tasks import convert
from sqlalchemy.orm import Session
from routes.Authentication import CLIENT_ID,CLIENT_SECRET
from services.Spotify_Service import Spotify
#from ..services.logger import log_playlist
from services.AppleParser import AppleParser
from services.database import SessionLocal
from services.dbmodel import SpotifyPlaylist
import httpx
import base64
from services.redis_file import client
from datetime import datetime, timedelta
from services.dbmodel import SpotifyAdmin
import asyncio

spotify = Spotify()
appleParser = AppleParser()
router = APIRouter()
st = CLIENT_ID + ':' + CLIENT_SECRET
auth_head = base64.b64encode(st.encode()).decode()

def db_connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_new_access_token(refresh_token:str):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://accounts.spotify.com/api/token",
                headers={"Content-Type": "application/x-www-form-urlencoded",
                         "Authorization": f"Basic {auth_head}"},
                data={"grant_type": "refresh_token",
                      "refresh_token": refresh_token }
            )
            print(res.text)
            if res.status_code == 200:
                return res.json()["access_token"]
    except Exception as e:
        raise HTTPException(status_code=404,detail=e)


@router.post("/convert/apple-music-to-spotify")
async def convert_playlist(apple_music_playlist_url:str,playlist_name:str,description:str):
    try:
        task = convert.delay(apple_music_playlist_url,playlist_name,description)
        return {
            "task_id":task.id,
            "status":"PENDING"
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=e)



@router.get("/status/{task_id")
def get_status(task_id:str):
    task = AsyncResult(task_id)

    return {
        "state":task.state,
        "result":task.result,
    }








