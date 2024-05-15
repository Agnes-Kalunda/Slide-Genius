from django.shortcuts import render
import openai

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
