from fastapi import APIRouter,HTTPException
from fastapi.responses import  RedirectResponse
import httpx
import os
import base64
import urllib.parse
from uuid import uuid4
from dotenv import load_dotenv
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/spotify/callback"
SCOPES = (
    "playlist-modify-public "
    "playlist-modify-private "
    "user-read-private"
)
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

router = APIRouter()
async def spotify_login():
    #Add state paramater with random UUID and store locally (next feature) (Prevents CORS Attack)
    params = {
        "client_id":CLIENT_ID,
        "response_type":"code",
        "redirect_uri":REDIRECT_URI,
        "scope":SCOPES
    }
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?"
        f"{urllib.parse.urlencode(params)}"
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def spotify_callback(code:str):
    async with httpx.AsyncClient() as client:
        st = CLIENT_ID + ':' + CLIENT_SECRET
        url_b64_str = base64.urlsafe_b64encode(st.encode()).decode()
        auth_head = 'Basic ' + url_b64_str
        response = await client.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type":"authorization_code",
                "code":code,
                "redirect_uri":REDIRECT_URI
            },
            headers={
                "Authorization": auth_head
            }
        )