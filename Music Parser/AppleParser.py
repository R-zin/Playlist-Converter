import httpx
import asyncio
from bs4 import BeautifulSoup
class AppleParser:
    playlist_url = None
    def __init__(self):
        pass
    def set_url(self,url):
        self.playlist_url = url

    async def parse_playlist_meta(self):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(self.playlist_url,headers={"User-Agent":"Mozilla/5.0"})
                print(res.text) #test
                soup = BeautifulSoup(res.text,"html.parser")
                playlist_name = soup.find("meta",{"name":"apple:title"})['content']
                song_count = soup.find("meta",{"property":"music:song_count"})['content']
                print(playlist_name)
                print(song_count)
        except Exception as e:
            print(e.__cause__)

s = AppleParser()
s.set_url("https://music.apple.com/in/playlist/malayalam-hits/pl.60dd84ecb1e14bf4b4ac9994fb18882f")
asyncio.run(s.parse_playlist_meta())
