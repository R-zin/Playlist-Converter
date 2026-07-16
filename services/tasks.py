from uuid import uuid4
import base64
from services.celery_app import celery
from services.database import SessionLocal
from services.Spotify_Service import Spotify
from services.AppleParser import AppleParser
from services.dbmodel import SpotifyAdmin, SpotifyPlaylist
from fastapi import HTTPException
import httpx
from routes.Authentication import CLIENT_ID,CLIENT_SECRET
from datetime import datetime, timedelta
import asyncio

spotify = Spotify()
appleParser = AppleParser()

st = CLIENT_ID + ':' + CLIENT_SECRET
auth_head = base64.b64encode(st.encode()).decode()

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

async def convert_playlist_async(apple_music_playlist_url:str,playlist_name:str,description:str):
    db = SessionLocal()
    try:
        apple_playlist = appleParser.parse_playlist_meta(apple_music_playlist_url)
        admin = db.query(SpotifyAdmin).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        token = None
        if datetime.now() >= admin.expires_at:
            token = await get_new_access_token(str(admin.refresh_token))
            admin.access_token = token
            admin.expires_at = datetime.now() + timedelta(seconds=3600)
            db.commit()
        else:
            token = admin.access_token
        res = spotify.create_playlist(token=str(token), playlist_name=playlist_name, songs=apple_playlist.songs,
                                      description=description)
        entry = SpotifyPlaylist(id=str(uuid4()), playlist_name=playlist_name, trackno=len(apple_playlist.songs),
                                playlist_link=res, song_list=apple_playlist.songs)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return {
            "playlist_url": res
        }
    except Exception as e:
        raise HTTPException(status_code=404,detail=e)
    finally:
        db.close()

@celery.task()
def convert(apple_music_playlist_url,playlist_name,description):
    return asyncio.run(convert_playlist_async(apple_music_playlist_url,playlist_name,description))

