from fastapi import APIRouter,HTTPException,Header
from ..services.Spotify_Service import Spotify

spotify = Spotify()
router = APIRouter()

@router.post("/convert/apple-music-to-spotify")
async def convert(apple_music_playlist_url:str,playlist_name:str,authorization:str = Header()):
    try:
        await spotify.create_playlist()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))








