from typing import List, Any
from typing_extensions import Self

from pydantic import BaseModel,Field,field_validator

class parsed_music(BaseModel):
    playlist_name:str
    song_count:int
    songs:List[str]
class ToSpotifyIn(BaseModel):
    playlist_name:str
    token:str
    apple_music_playlist_url:str = Field(...,pattern=r"^https://music\.apple\.com/.+/playlist/.+")
    @field_validator("apple_music_playlist_url")
    @classmethod
    def validate_apple_music_url(cls, value: str):
        if not value.startswith("https://music.apple.com"):
            raise ValueError("Invalid Apple Music URL")
        return value
