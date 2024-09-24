from django.shortcuts import render
import random
from typing import Dict, Any

# Define Quotes and Images Lists (Global Scope)
quotes = [
    "Since day one, since the first time I touched the pen, I wanted to be the best at what I do.",
    "Whenever I make music, it reflects where I'm at mentally.",
    "As long as my music is real, there's no limit to how many ears I can grab."
]

images = [
    "https://www.google.com/imgres?q=kendrick%20lamar%20photos&imgurl=https%3A%2F%2Fakns-images.eonline.com%2Feol_images%2FEntire_Site%2F202488%2Frs_1200x1200-240908095312-1200-kendrick-lamar-super-bowl-2025-cjh-090824.jpg%3Ffit%3Daround%257C660%3A372%26output-quality%3D90%26crop%3D660%3A372%3Bcenter%2Ctop&imgrefurl=https%3A%2F%2Fwww.eonline.com%2Fnews%2Fkendrick_lamar&docid=TMJSml3A65OpCM&tbnid=PEJYMPYb62V4DM&vet=12ahUKEwi61IOP4NuIAxVmD1kFHVbHEq8QM3oECG8QAA..i&w=660&h=372&hcb=2&ved=2ahUKEwi61IOP4NuIAxVmD1kFHVbHEq8QM3oECG8QAA",
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fopen.spotify.com%2Fartist%2F2YZyLoL8N0Wb9xBt1NhZWg&psig=AOvVaw2gabS-u_0SABHU5RHdSRH4&ust=1727273171077000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCMjThrvg24gDFQAAAAAdAAAAABAE",
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fnypost.com%2F2022%2F05%2F13%2Fwhy-kendrick-lamar-is-the-greatest-rapper-of-his-generation%2F&psig=AOvVaw2gabS-u_0SABHU5RHdSRH4&ust=1727273171077000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCMjThrvg24gDFQAAAAAdAAAAABAJ"
]

# Views for the quotes app

def get_random_quote_and_image() -> Dict[str, Any]:
    """
    Selects a random quote and its corresponding image.

    Returns:
        A dictionary containing a random quote and image.
    """
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
