from sqlalchemy import Column,Integer,Text
from database import Base

class SpotifyAdmin(Base):
    __tablename__ = "spotify_admin"
    id = Column(Integer,primary_key=True)
    refresh_token = Column(Text,nullable=False)
    spotify_user_id = Column(Text,nullable=False)
