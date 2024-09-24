from django.shortcuts import render
import random
from typing import Dict, Any
from django.urls import reverse

# Define Quotes and Images Lists (Global Scope)
quotes = [
    "Since day one, since the first time I touched the pen, I wanted to be the best at what I do.",
    "Whenever I make music, it reflects where I'm at mentally.",
    "As long as my music is real, there's no limit to how many ears I can grab."
]

images = [
    "https://www.google.com/imgres?q=kendrick%20lamar%20photos%20good%20quality&imgurl=https%3A%2F%2Fwallpapers.com%2Fimages%2Fhd%2Fkendrick-lamar-close-up-photography-v6h66gs4en54vd2k.jpg&imgrefurl=https%3A%2F%2Fwallpapers.com%2Fkendrick-lamar-pictures&docid=WoJuv_GFNeTxXM&tbnid=2kMtJIfNGWBoyM&vet=12ahUKEwjSt8jqh9yIAxWbGFkFHXnQLBsQM3oECBgQAA..i&w=1920&h=1280&hcb=2&ved=2ahUKEwjSt8jqh9yIAxWbGFkFHXnQLBsQM3oECBgQAA",
    "https://www.google.com/imgres?q=kendrick%20lamar%20photos%20good%20quality&imgurl=https%3A%2F%2Fwww.hotnewhiphop.com%2Fimages%2Fv2%2F2024%2F04%2Fkendrick-lamar-good-kid-maad-city-scaled.jpg&imgrefurl=https%3A%2F%2Fpartnersco.me%2Fdeabgcvshop%2F795087-kendrick-lamar-good-kid-maad-city-milestone-hip-hop-news&docid=GIyD_XuzgXdgtM&tbnid=LwmHU6IyM8E4qM&vet=12ahUKEwjSt8jqh9yIAxWbGFkFHXnQLBsQM3oECDgQAA..i&w=2560&h=1707&hcb=2&itg=1&ved=2ahUKEwjSt8jqh9yIAxWbGFkFHXnQLBsQM3oECDgQAA",
    "https://www.google.com/imgres?q=kendrick%20lamar%20photos%20good%20quality&imgurl=https%3A%2F%2Ffootwearnews.com%2Fwp-content%2Fuploads%2F2022%2F04%2Fkendrick-lamar.jpg&imgrefurl=https%3A%2F%2Ffootwearnews.com%2Ffashion%2Fcelebrity-style%2Fkendrick-lamar-paris-crochet-vest-parachute-pants-1203360576%2F&docid=ou__l4g-3wELRM&tbnid=E1gYL_YZ-yYHSM&vet=12ahUKEwjSt8jqh9yIAxWbGFkFHXnQLBsQM3oECCMQAA..i&w=1024&h=697&hcb=2&ved=2ahUKEwjSt8jqh9yIAxWbGFkFHXnQLBsQM3oECCMQAA"
]


# Views for the quotes app

def get_random_quote_and_image() -> Dict[str, Any]:
    index = random.randint(0, len(quotes) - 1)
    return {
        'quote': quotes[index],
        'image': images[index],
    }


def quote(request) -> render:
    """
    This view displays a random quote and image.
    """
    context = get_random_quote_and_image()
    return render(request, 'quote.html', context)

def show_all(request) -> render:
    """
    This view displays all quotes and images.
    """
    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, 'show_all.html', context)

def about(request) -> render:
    """
    This view displays the about page.
    """
    about_text = (
        "This application displays quotes from [Famous Person Name]. "
        "[Famous Person Name] was [Brief Biography]. "
        "This application was created by [Your Name]."
    )

    context = {
        'about_text': about_text,
    }
    return render(request, 'about.html', context)
