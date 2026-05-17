from fastapi import APIRouter
import httpx
import dotenv
import os
import urllib.parse

from langchain_community.document_loaders.googledrive import SCOPES

router = APIRouter()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URL = ""
COPES = (
    "playlist-modify-public"
    "playlist-modify-private"
    "user-read-private"
)

@router.get('/login')
async def spotify_login():
    
