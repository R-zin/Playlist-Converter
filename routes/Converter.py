from fastapi import APIRouter,HTTPException,Header
from services.Spotify_Service import Spotify
#from ..services.logger import log_playlist
from services.AppleParser import AppleParser
from services.database import SessionLocal
from services.dbmodel import SpotifyPlaylist
from services.redis_file import client
import asyncio

spotify = Spotify()
appleParser = AppleParser()
router = APIRouter()
db = SessionLocal()

@router.post("/convert/apple-music-to-spotify")
async def convert(apple_music_playlist_url:str,playlist_name:str,authorization:str = Header()):
    try:
        apple_playlist = asyncio.run(appleParser.parse_playlist_meta(apple_music_playlist_url))
        if not apple_playlist:
            raise Exception
        #token = db.query()
        res = await spotify.create_playlist(token=token,playlist_name=playlist_name,songs=apple_playlist)
        entry = SpotifyPlaylist(playlist_name=playlist_name,trackno=len(apple_playlist.songs),playlist_link=res,song_list=apple_playlist.songs)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return {
            "playlist_url":res
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))








