from celery import Celery
from celery import shared_task
from channels.layers import get_channel_layer
import asyncio
import celery
import time
import urllib
import requests
import urllib.parse
import http.client
from bs4 import BeautifulSoup
import json


@shared_task(bind=True)
def add(self,x,y):
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    URL = "http://localhost:8000/chat/lobby/"
    page = requests.get(URL)
    results=page.text
    print(results)
    data=results
    payload=json.loads(results)
    count=1
    for data in payload.get('title'):
        print(data)
    loop.run_until_complete(channel_layer.group_send("chat_lobby", {
        'type': 'chat_message',
        'message': data,
    }))
    return 'Done'