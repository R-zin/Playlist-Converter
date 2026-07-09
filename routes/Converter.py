from uuid import uuid4

from fastapi import APIRouter,HTTPException,Depends
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
async def convert(apple_music_playlist_url:str,playlist_name:str,description:str,db: Session = Depends(db_connect)):
    try:
        apple_playlist = await appleParser.parse_playlist_meta(apple_music_playlist_url)
        admin = db.query(SpotifyAdmin).first()
        if not admin:
            raise HTTPException(status_code=404,detail="Admin not found")
        token = None
        if datetime.now() >= admin.expires_at:
            token = await get_new_access_token(str(admin.refresh_token))
            admin.access_token = token
            admin.expires_at = datetime.now() + timedelta(seconds=3600)
            db.commit()
        else:
            token = admin.access_token
        res = await spotify.create_playlist(token=str(token),playlist_name=playlist_name,songs=apple_playlist.songs,description=description)
        entry = SpotifyPlaylist(id=str(uuid4()),playlist_name=playlist_name,trackno=len(apple_playlist.songs),playlist_link=res,song_list=apple_playlist.songs)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return {
            "playlist_url":res
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=e)








