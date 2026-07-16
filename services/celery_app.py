from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv("../.env")
REDIS_URL = os.getenv("REDIS_URL")


app = Celery("celery_app")
celery = Celery('Playlist_converter',
                    broker=REDIS_URL,
                    backend=REDIS_URL,)

celery.conf.update(task_serializer='json',
                       accept_content=['json'],
                       result_serializer='json',
                       timezone='UTC')
