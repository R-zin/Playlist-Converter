from typing import List
from pydantic import BaseModel

class parsed_music(BaseModel):
    playlist_name:str
    song_count:int
    songs:List[str]