from http.client import HTTPException
from wsgiref import headers
from rapidfuzz import process
from typing import List
import httpx
class Spotify:
    def __init__(self):
        pass
    async def check(self,authorization):
        if not authorization.startswith("Bearer "):
            return False
        access_token = authorization.split(" ")[1]
        headers = {
            "Authorization":f"Bearer {access_token}"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.spotify.com/v1/me",
                                        headers=headers)
            if response.status_code != 200:
                return False
            else:
                return True
    async def best_one(self,target,query:dict):
        q = query.keys()
        best = process.extractOne(target,q)
        return query[best[0]]

    async def find_song(self,name: str):
        res = {}
        async with httpx.AsyncClient() as client:
            payload = {
                "q":name,
                "type":"track",
                "limit":10
            }
            response = await client.get("https://api.spotify.com/v1/search",headers=headers,params=payload)
            if response.status_code == 200:
                for i in response.json()["tracks"]["items"]:
                    res[i["name"]] = i["uri"]







    async def create_playlist(self,token:str,playlist_name:str,description:str,public:bool,songs:List[str]):
        async with httpx.AsyncClient() as client:
            content = {"name":playlist_name,
                       "description":description,
                       "public":public}
            response = await client.post("https://api.spotify.com/v1/me/playlists",
                                         data=content,
                                         headers=f"Bearer {token}")
            url = response["external_urls"]["spotify"]
            playlist_id = response["id"]
            for i in songs:
                song =







    
