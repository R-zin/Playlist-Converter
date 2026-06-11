from fastapi import APIRouter,HTTPException,Header
from ..services.Spotify_Service import Spotify
from ..services.logger import log_playlist

spotify = Spotify()
router = APIRouter()

@router.post("/convert/apple-music-to-spotify")
async def convert(apple_music_playlist_url:str,playlist_name:str,authorization:str = Header()):
    try:
        res = await spotify.create_playlist()
        await log_playlist(apple_music_playlist_url,res)
        return {
            "playlist_url":res
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))








