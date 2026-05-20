from fastapi import APIRouter,HTTPException,Header
from ..services.Spotify_Service import Spotify
router = APIRouter()

@router.post("/convert/apple-music-to-spotify")
async def convert(apple_music_playlist_url:str,playlist_name:str,authorization:str = Header()):
    try:
        if not Spotify.check(authorization):
            raise HTTPException(status_code=401,detail="Invalid Token")
        Spotify.create_playlist()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))








