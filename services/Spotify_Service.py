from http.client import HTTPException

import httpx
class Spotify:
    def __init__(self):
        pass
    def check(self,authorization):
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
            response = await client.post("https://api.spotify.com/v1/me/playlists",
                                         data=content,
                                         headers=f"Bearer {token}")







    
