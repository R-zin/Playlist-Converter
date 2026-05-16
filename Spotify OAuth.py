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
SCOPES

@router.get('/login')
async def spotify_login():
    
