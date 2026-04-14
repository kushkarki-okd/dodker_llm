from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate ,login as auth_login
import requests
from .models import chat,message
from django.http import JsonResponse
from .forms import signupform,loginform

def create_chat(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    Chat=chat.objects.create(user=request.user)

    return JsonResponse({
            "chat_id": Chat.id
        })

def chat_page(request, chat_id):
    from .models import chat as ChatModel, message as MessageModel

    Chat = get_object_or_404(ChatModel, id=chat_id)
    all_chats = ChatModel.objects.filter(user=request.user).order_by('-created_at')  # ← for sidebar
    Messages = MessageModel.objects.filter(chat=Chat).order_by('created_at')

    return render(request, 'chat_page.html', {
        'chats': all_chats,      
        'messages': Messages,    
        'current_chat': Chat     
    })

def send_message(request, chat_id):

    Chat = get_object_or_404(chat, id=chat_id, user=request.user)

    user_input = request.POST.get('message')

    if not user_input:
        return JsonResponse({"error": "Empty message"})

    # Save user message
    message.objects.create(
        chat=Chat,
        sender="user",
        content=user_input
    )
    if message.objects.filter(chat=Chat).count() == 1:
        Chat.title=user_input[:30]
        Chat.save()

    
    msgs = message.objects.filter(chat=Chat).order_by('-created_at')[:5]
    msgs = reversed(msgs)

    prompt = "You are a helpful assistant.\n\n"

    for m in msgs:
        if m.sender == "user":
            prompt += f"User: {m.content}\n"
        else:
            prompt += f"Assistant: {m.content}\n"

    prompt += "Assistant:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        ai_reply = response.json().get('response', 'No reply')
    except:
        ai_reply = "AI Error"

    # Save bot reply
    message.objects.create(
        chat=Chat,
        sender="bot",
        content=ai_reply
    )

    return JsonResponse({
        "reply": ai_reply,
        'chat_title':Chat.title
    })

def signup(request):

    if request.method=='POST':
        form = signupform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        
        form=signupform()

    return render(request, 'signup.html',{'form':form})



def login(request):
    if request.method=='POST':
        form = loginform(request, data=request.POST)
        if form.is_valid():
            print('form is valied')
            user = form.get_user() 
            if user is not None:
                print ('login successful')

                auth_login(request,user)
                Chat = chat.objects.create(user=user)  
                return redirect('chat_page', chat_id=Chat.id)  

    else:
        form=loginform()    
    return render(request,'login.html',{'form':form})
        