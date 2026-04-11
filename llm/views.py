from django.shortcuts import render, redirect,get_object_or_404
import requests
from .models import chat,message
from django.http import JsonResponse

def create_chat(request):

    if request.user.is_authentacated:
        return redirect('login')
    
    Chat=chat.objects.create(user=request.user)

    return JsonResponse({
            "chat_id": chat.id
        })


def chat_page(request,chat_id):
    Chat =get_object_or_404(chat,id=chat_id)
    Message=message.objects.filter(Chat=Chat)
    return render (request,'chat_page.html',{
        'Chat':Chat,
        'Message':Message
    })


def send_message(request, chat_id):

    # yesla ceh ai lai help hos further predict garna lai vanera history ba ta message linxa 
    chat = get_object_or_404(chat, id=chat_id, user=request.user)

    # get user message
    user_input = request.POST.get('message')


    message.objects.create(
        chat=chat,
        sender="user",
        text=user_input
    )
# yeslaey database bata filter garca caht id ame retrive garxa latest to old
    msgs = message.objects.filter(chat=chat).order_by('-created_at')[:5]
    msgs = reversed(msgs)  # correct order ma reverse garxa because llm le bujdina so old to latest ma change garaxa
 #yesle che prompt banaunxa hai tw 
    prompt = "You are a helpful assistant.\n\n"

    for m in msgs:
        if m.sender == "user":
            prompt += f"User: {m.text}\n"
        else:
            prompt += f"Assistant: {m.text}\n"

    prompt += "Assistant:"

  #backend ma ollama lai pathauxa hai tw 
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
#ai le replay denxa 
    ai_reply = response.json()['response']

#tyo ai tko replay save garxa 
    message.objects.create(
        chat=chat,
        sender="bot",
        text=ai_reply
    )

    return JsonResponse({
        "reply": ai_reply
    })