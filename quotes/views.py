from django.shortcuts import render
import random
from typing import Dict, Any
from django.http import HttpResponse
from django.templatetags.static import static


# Define Quotes and Images Lists (Global Scope)
quotes = [
    "Since day one, since the first time I touched the pen, I wanted to be the best at what I do.",
    "Whenever I make music, it reflects where I'm at mentally.",
    "As long as my music is real, there's no limit to how many ears I can grab."
]

images = [
    static('images/kendrick_lamar1.jpg'),  # Add correct filenames for your static images
    static('images/kendrick_lamar2.jpg'),
    static('images/kendrick_lamar3.jpg')
]

def show_all(request):
    # Zip quotes and images into a list of tuples
    quotes_images = zip(quotes, images)
    context = {
        'quotes_images': quotes_images
    }
    return render(request, 'show_all.html', context)
# ... rest of your code ...

# Views for the quotes app
def get_random_quote_and_image() -> Dict[str, Any]:
    """
    This function returns a random quote and its corresponding image.
    """
    index = random.randint(0, len(quotes) - 1)
    return {
        'quote': quotes[index],
        'image': images[index],  # The image path is already processed by static()
    }

def quote(request) -> HttpResponse:
    """
    This view displays a random quote and image.
    """
    context = get_random_quote_and_image()
    return render(request, 'quote.html', context)

# In views.py


def about(request) -> HttpResponse:
    """
    This view displays the about page.
    """
    about_text = (
        "This application displays quotes from Kendrick Lamar. "
        "Kendrick Lamar is a renowned American rapper and songwriter. "
        "This application was created by Jordan Espinal."
    )

    context = {
        'about_text': about_text,
    }
    return render(request, 'about.html', context)