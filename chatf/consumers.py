import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class ChatConsumer(WebsocketConsumer):
 def connect(self):
     self.room_name = self.scope['url_route']['kwargs']['room_name']
     print('connected')
     self.room_group_name = 'chat_%s' % self.room_name
# Join room group
     async_to_sync(self.channel_layer.group_add)(
       self.room_group_name,
       self.channel_name
        )
     async_to_sync(self.channel_layer.group_send)(
     self.room_group_name,
   {
   'type': 'online_status',
   'message': self.scope['user'].username
  }
 )
     self.accept()
 def disconnect(self, close_code):
# Leave room group
   async_to_sync(self.channel_layer.group_discard)(
    self.room_group_name,
    self.channel_name
   )
# Receive message from WebSocket
 def receive(self, text_data):
     text_data_json = json.loads(text_data)
     print(self.scope['user'])
     message = text_data_json['message']
# Send message to room group
     async_to_sync(self.channel_layer.group_send)(
     self.room_group_name,
   {
   'type': 'chat_message',
   'message': message
  }
 )
# Receive message from room group
 def chat_message(self, event):
     message = event['message']
     # Send message to 
     self.send(text_data=json.dumps({
     'message': message
     }))
  
 def online_status(self,event):
    message = event['message']
    print(message)
    self.send(text_data=json.dumps({'message':message}))