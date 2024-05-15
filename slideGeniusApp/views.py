import os
from django.shortcuts import render
import openai
from django.http import JsonResponse

openai.api_key = os.getenv('OPENAI_API_KEY')

# Create your views here.
def home (request):
    return render(request , "index.html" )

def chat_view(request) :
    if request.method == 'POST':
        user_input = request.POST.get('message')
        response = openai.Completion.create(
            engine ="",
            prompt=user_input,
            max_token=150
        )
        chatgpt_response = response = response.choices[0].text.strip()
        return JsonResponse({
            'user_input': user_input,
            'chatgpt_response': chatgpt_response
        })
    return render(request, "chat.html")