from fastapi import APIRouter,HTTPException

router = APIRouter()

@router.post("/convert/apple-music-to-spotify")
async def convert(apple_music_playlist_url:str):

