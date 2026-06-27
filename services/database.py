import os
from email import message

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    engine = create_engine(DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

except Exception as e:
    if not DATABASE_URL:
        raise HTTPException(status_code=500,detail="DATABASE URL NOT SETUP")
    else:
        raise HTTPException(status_code=500,detail=str(e))

Base = declarative_base()