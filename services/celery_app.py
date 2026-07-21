from celery import Celery
import os
from pathlib import Path
from dotenv import load_dotenv
REDIS_URL = os.getenv("REDIS_URL")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


app = Celery("celery_app")


celery = Celery('Playlist_converter',
                    broker=REDIS_URL,
                    backend=REDIS_URL,
                include=['services.tasks'])

celery.conf.update(task_serializer='json',
                       accept_content=['json'],
                       result_serializer='json',
                       timezone='UTC')
