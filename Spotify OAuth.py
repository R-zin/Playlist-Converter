from fastapi import APIRouter
import httpx
router = APIRouter()

@router.get('/login')
async def spotify_login():
