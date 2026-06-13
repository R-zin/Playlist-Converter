from fastapi import APIRouter,HTTPException,Header
from ..services.Spotify_Service import Spotify
from ..services.logger import log_playlist
from ..services.AppleParser import AppleParser
import asyncio

spotify = Spotify()
appleParser = AppleParser()
router = APIRouter()

@router.post("/convert/apple-music-to-spotify")
async def convert(apple_music_playlist_url:str,playlist_name:str,authorization:str = Header()):
    try:
        apple_playlist = asyncio.run(appleParser.parse_playlist_meta(apple_music_playlist_url))
        if not apple_playlist:
            raise Exception
        res = await spotify.create_playlist(apple_playlist.songs)

        await log_playlist(apple_music_playlist_url,res)
        return {
            "playlist_url":res
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))








