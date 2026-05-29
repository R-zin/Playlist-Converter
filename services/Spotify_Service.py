from fastapi import HTTPException

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

    async def create_playlist(self,token:str,playlist_name:str,description:str,public:bool):
        async with httpx.AsyncClient() as client:
            content = {"name":playlist_name,
                       "description":description,
                       "public":public}
            headers = {"Authorization" : f"Bearer {token}",
                       "Content-Type": "application/json"
                       }

            response = await client.post("https://api.spotify.com/v1/me/playlists",
                                         json=content,
                                         headers=headers)
            if response.status_code not in[200.201]:
                raise HTTPException(status_code=500,detail=response.text)
            return response.json()











    
