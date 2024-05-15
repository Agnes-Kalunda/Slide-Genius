from django.shortcuts import render
import openai
from django.shortcuts import redirect

def index(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        num_slides = int(request.POST.get('num_slides', 3))

        # ChatGPT API call with the topic and get the slide content
        response = openai.Completion.create(
            engine="",
            prompt=f"Create a presentation on {topic} with {num_slides} slides.",
            max_tokens=500
        )
        slide_content = response.choices[0].text.strip()

        #  presentation file path here
        presentation_file_path = ""

        return render(request, 'index.html', {
            'presentation_file_path': presentation_file_path,
            'slide_content': slide_content.split('\n'),
            'num_slides': num_slides,
            'current_slide': 1  # Initial slide
        })

    return render(request, 'index.html')



def next_slide(request):
    if request.method == 'POST':
        current_slide = int(request.POST.get('current_slide', 1))
        num_slides = int(request.POST.get('num_slides', 1))

        next_slide = current_slide + 1 if current_slide < num_slides else num_slides
        return redirect('index')
    return redirect('index')  

def previous_slide(request):
    if request.method == 'POST':
        current_slide = int(request.POST.get('current_slide', 1))

        previous_slide = current_slide - 1 if current_slide > 1 else 1
        return redirect('index')
    return redirect('index')