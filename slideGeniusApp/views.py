from django.shortcuts import render
from django.http import JsonResponse
import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()

        print(f"User input: {user_input}")
        print(f"Session before processing: {request.session.items()}")

        if not user_input:  # Check for empty input
            print("No user input provided.")
            return JsonResponse({'error': 'Please enter a message'})

        # Check if a topic is already set in the session and if the input is not a number
        if 'topic' not in request.session or request.session['topic'] is None or not user_input.isdigit():
            # If a new topic is entered, reset the session
            request.session['topic'] = user_input  # Here, user_input is a string
            print(f"Setting session topic: {user_input}")
            print(f"Session after setting topic: {request.session.items()}")
            return JsonResponse({'chatgpt_response': f"How many slides would you like for the topic: '{user_input}'?"})
        else:
            topic = request.session['topic']
            print(f"Session topic: {topic}")

            # A topic is already set, expect a number of slides
            if user_input.isdigit() and 1 <= int(user_input) <= 20:
                num_slides = int(user_input)  # Here, user_input is converted to an integer
                print(f"Number of slides: {num_slides}")

                try:
                    # Assuming successful interaction with the API
                    response = openai.Completion.create(
                        engine="gpt-3.5-turbo",
                        prompt=f"Create a summary presentation about '{topic}' consisting of {num_slides} slides.",
                        max_tokens=1000,
                        temperature=0.1
                    )
                    chatgpt_response = response.choices[0].text.strip()
                    print(f"ChatGPT response: {chatgpt_response}")

                    request.session.pop('topic')  # Clear the topic after use
                    print(f"Session after popping topic: {request.session.items()}")
                    return JsonResponse({'chatgpt_response': chatgpt_response})
                except Exception as e:
                    print(f"Error from OpenAI API: {str(e)}")
                    return JsonResponse({'error': str(e)})
            else:
                print("Invalid number of slides provided.")
                return JsonResponse({'error': 'Please enter a valid number of slides (1-20)'})
    return render(request, 'index.html')
