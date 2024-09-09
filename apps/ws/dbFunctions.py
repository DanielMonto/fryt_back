from channels.db import database_sync_to_async
from apps.chat.models import Chat
from apps.authentication.models import UserOwnModel
from apps.posts.models import Message

def addMessage(chat_id, writer_name, text, consumer):
    writer = UserOwnModel.objects.filter(username = writer_name).first()
    chat = Chat.objects.filter(id = chat_id).first()
    if chat == None:
        consumer.close()
    else:
        message = Message(chat = chat, user= writer, text = text)
        message.save()