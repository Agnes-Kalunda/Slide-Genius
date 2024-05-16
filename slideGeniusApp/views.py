from django.shortcuts import render
from django.http import JsonResponse
import os
import openai


openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        if not user_input:  # Check for empty input
            return JsonResponse({'error': 'Please enter a message'})

        # Initial interaction or handle topic input based on chat history
        if 'topic' not in request.session:  
            request.session['topic'] = user_input  
            return JsonResponse({'chatgpt_response': "How many slides would you like for the topic: '{}'?".format(user_input)})
        else:
            # Check if expecting number of slides
            if user_input.isdigit(): 
                num_slides = int(user_input)
                
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Create a summary presentation about '{request.session['topic']}' consisting of {num_slides} slides.",
                    max_tokens=1000 
                )
                chatgpt_response = response.choices[0].text.strip()
                # Logic to handle or display generated slide content
                request.session['slide_content'] = chatgpt_response
                del request.session['topic']  
                return JsonResponse({'chatgpt_response': chatgpt_response})
            else:
                return JsonResponse({'error': 'Please enter a valid number of slides'})


    return render(request, 'index.html')
