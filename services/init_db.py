from database import engine,Base
from dbmodel import SpotifyAdmin,SpotifyPlaylist

Base.metadata.create_all(bind=engine)

print("Tables created")

