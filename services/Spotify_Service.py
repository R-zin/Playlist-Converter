import asyncio
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
        if not query:
            return None
        best = process.extractOne(target,tuple(query.keys()))
        if not best:
            return None
        return query[best[0]]

    async def find_song(self,name: str,token:str):
        res = {}
        headers = {"Authorization":f"Bearer {token}"}
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
        return res
    async def search_songs_parellel(self,song_names:List[str],token:str):
        tasks = [self.find_song(name,token) for name in song_names]
        results = await asyncio.gather(*tasks,return_exceptions=True)
        song_uri = []
        for name,result in zip(song_names,results):
            best_uri = await self.best_one(name,result)
            song_uri.append(best_uri)
        return song_uri

    async def add_tracks_to_playlist(self,headers:dict,uri_list:List[str],playlist_id:str):

        async with httpx.AsyncClient() as client:
            response = client.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/items",
                                          headers=headers, json={"uris":uri_list})


    async def create_playlist(self,token:str,playlist_name:str,description:str,songs:List[str]):
        headers = {"Authorization":f"Bearer {token}"}
        song_uris = await self.search_songs_parellel(songs,token)
        async with httpx.AsyncClient() as client:
            content = {"name":playlist_name,
                       "description":description,
                       "public":True}
            response = await client.post("https://api.spotify.com/v1/me/playlists",
                                         json=content,
                                         headers=headers)
            url = response.json()["external_urls"]["spotify"]
            playlist_id = response.json()["id"]
            batches = [song_uris[i:i+100] for i in range(0, len(song_uris), 100)]

            await asyncio.gather(*[self.add_tracks_to_playlist(headers,batch,playlist_id) for batch in batches])
            return url







    
