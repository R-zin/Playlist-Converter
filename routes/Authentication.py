
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
@router.post("/login")
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
        auth_head = base64.b64encode(st.encode()).decode()
        response = await client.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type":"authorization_code",
                "code":code,
                "redirect_uri":REDIRECT_URI
            },
            headers={
                "Authorization": f"Basic {auth_head}",
                "content-type": "application/x-www-form-urlencoded"
            }
        )
        if response.status_code == 200:
            data = response.json()
            access_token = data["access_token"]
            refresh_token = data["refresh_token"]
            frontend_url = f"http://localhost:5173/callback?token={access_token}"
            return RedirectResponse(frontend_url)
        else:
            raise HTTPException(status_code=401,detail=f"access token invalid  unauthorized/expired {response}")
