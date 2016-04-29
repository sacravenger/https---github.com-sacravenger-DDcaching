from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group


# In consumers.py
from channels import Group

# Connected to websocket.connect
def ws_add(message):
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    Group("chat").send({
        "text": message.content['text'],
    })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
