import httpx
class Spotify:
    def __init__(self):
        pass
    async def create_playlist(self,token:str,playlist_name:str,description:str,public:bool):
        async with httpx.AsyncClient() as client:
            content = {"name":playlist_name,
                       "description":description,
                       "public":public}
            response = await client.post("https://api.spotify.com/v1/me/playlists",
                                         data=content,
                                         headers=f"Bearer {token}")






    
