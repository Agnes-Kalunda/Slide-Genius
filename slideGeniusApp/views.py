from django.shortcuts import render
from django.http import JsonResponse
import os
import openai
from pptx import Presentation
from pptx.util import Inches
from django.conf import settings

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_presentation(topic, num_slides):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"Create a summary presentation about '{topic}' consisting of {num_slides} slides.",
        max_tokens=1000,
        temperature=0.1
    )
    slides_content = response.choices[0].text.strip().split('\n')

    prs = Presentation()
    for slide_content in slides_content:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title, content = slide_content.split(':', 1)
        slide.shapes.title.text = title.strip()
        slide.placeholders[1].text = content.strip()

    file_path = os.path.join(settings.MEDIA_ROOT, f"{topic}_presentation.pptx")
    prs.save(file_path)
    return file_path

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()

        if not user_input:
            return JsonResponse({'error': 'Please enter a message'})

        if 'topic' not in request.session or request.session['topic'] is None or not user_input.isdigit():
            request.session['topic'] = user_input
            return JsonResponse({'chatgpt_response': f"How many slides would you like for the topic: '{user_input}'?"})
        else:
            topic = request.session['topic']
            if user_input.isdigit() and 1 <= int(user_input) <= 20:
                num_slides = int(user_input)
                try:
                    presentation_file_path = generate_presentation(topic, num_slides)
                    request.session.pop('topic')
                    return JsonResponse({'chatgpt_response': f"Presentation created! View it here: /media/{os.path.basename(presentation_file_path)}", 'presentation_file_path': f"/media/{os.path.basename(presentation_file_path)}"})
                except Exception as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'error': 'Please enter a number of slides between 1-20'})

    return render(request, 'index.html')
