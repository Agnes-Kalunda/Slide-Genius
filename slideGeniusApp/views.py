from django.shortcuts import render
from django.http import JsonResponse
import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()
        if not user_input:  # Check for empty input
            return JsonResponse({'error': 'Please enter a message'})

        topic = request.session.get('topic')
        if topic is None:  # Initial interaction
            request.session['topic'] = user_input
            return JsonResponse({'chatgpt_response': f"How many slides would you like for the topic: '{user_input}'?"})
        else:
            if user_input.isdigit() and 1 <= int(user_input) <= 20:
                num_slides = int(user_input)
                try:
                    response = openai.Completion.create(
                        engine="gpt-3.5-turbo",
                        prompt=f"Create a summary presentation about '{topic}' consisting of {num_slides} slides.",
                        max_tokens=1000,
                        temperature=0.1
                    )
                    chatgpt_response = response.choices[0].text.strip()
                    request.session.pop('topic', None)  # Clear the topic
                    return JsonResponse({'chatgpt_response': chatgpt_response})
                except Exception as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'error': 'Please enter a valid number of slides (1-20)'})

    return render(request, 'index.html')
