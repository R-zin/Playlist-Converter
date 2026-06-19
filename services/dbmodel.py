from sqlalchemy import Column, Integer, Text, String, ARRAY
from database import Base

class SpotifyAdmin(Base):
    __tablename__ = "spotify_admin"
    id = Column(Integer,primary_key=True)
    refresh_token = Column(Text,nullable=False)
    spotify_user_id = Column(Text,nullable=False)
class SpotifyPlaylist(Base):
    __tablename__ = "spotify_playlist"
    id = Column(String,primary_key=True)
    playlist_name = Column(String,nullable=False)
    trackno = Column(Integer,nullable=False)
    playlist_link = Column(String,nullable=False)
    song_list = Column(ARRAY(Text),nullable=False)

