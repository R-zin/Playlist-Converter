
from fastapi import APIRouter,HTTPException,Depends,Header
from fastapi.params import Header
from fastapi.security import OAuth2AuthorizationCodeBearer
from datetime import datetime, timedelta
from services.database import SessionLocal
from uuid import uuid4
from services.dbmodel import SpotifyAdmin
import httpx
import os
import base64
import urllib.parse
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/callback"
SCOPES = {
    "playlist-modify-public":"Modify playlist",
    "playlist-modify-private": "modify private playlist",
    "user-read-private":"Read private playlist"
}
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
ADMIN_KEY = os.getenv("ADMIN_KEY")
oauth_scheme = OAuth2AuthorizationCodeBearer(SPOTIFY_AUTH_URL,SPOTIFY_TOKEN_URL,scopes=SCOPES)
async def verify_admin(x_admin_key:str = Header(None)):
    if not ADMIN_KEY:
        raise HTTPException(status_code=401,detail="Admin key not provided")
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403,detail="Admin Unauthorized")
    return True
router = APIRouter()

@router.get("/login")
async def spotify_login(admin:bool = Depends(verify_admin)):
    #Add state paramater with random UUID and store locally (next feature) (Prevents CORS Attack)
    params = {
        "response_type": 'code',
      "client_id": CLIENT_ID,
      "scope": " ".join(SCOPES.keys()),
      "redirect_uri": REDIRECT_URI,
    }
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?"
        f"{urllib.parse.urlencode(params)}"
    )
    #return RedirectResponse(auth_url)
    return {
        "authorization_url":auth_url
    }

@router.get("/callback")
async def spotify_callback(code:str):
    print(code)
    async with httpx.AsyncClient() as client:
        try:
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
                expires_in = data["expires_in"]
                s = SessionLocal()
                admin = SpotifyAdmin(
                    id=str(uuid4()),
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expires_at=datetime.now() + timedelta(seconds=expires_in),
                )
                s.add(admin)
                s.commit()
                s.refresh(admin)
                return {"access_token":access_token,
                        "refresh_token":refresh_token,
                        "expires_in":expires_in}
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))

