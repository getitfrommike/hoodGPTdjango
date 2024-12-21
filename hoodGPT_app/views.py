import os
from django.shortcuts import render
from .forms import OpenAIForm
from decouple import config
from openai import OpenAI  # Import the OpenAI client
import logging

# Instantiate the OpenAI client
client = OpenAI(api_key=config("OPENAI_API_KEY"))  # Pass the API key when creating the client

# Set the OpenAI API key
OpenAI.api_key = config("OPENAI_API_KEY")

logger = logging.getLogger(__name__)

def index(request):
    response_text = None
    if request.method == "POST":
        form = OpenAIForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            try:
                # Create a completion with OpenAI
                completion = client.chat.completions.create(
                    model="gpt-4",  # Specify the model
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                # Extract response content
                response_text = completion.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI API error: {str(e)}")
                response_text = "An error occurred while processing your request."
    else:
        form = OpenAIForm()

    # Render the form and the response
    return render(request, 'hoodGPT_app/index.html', {'form': form, 'response_text': response_text})

def store(request):
    return render(request, 'hoodGPT_app/store.html')
