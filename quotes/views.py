from django.shortcuts import render
import random

# Define Quotes and Images Lists (Global Scope)
quotes = [
    "Since day one, since the first time I touched the pen, I wanted to be the best at what I do.",
    "Whenever I make music, it reflects where I'm at mentally.",
    "As long as my music is real, it's no limit to how many ears I can grab."
]

images = [
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fnypost.com%2F2022%2F05%2F13%2Fwhy-kendrick-lamar-is-the-greatest-rapper-of-his-generation%2F&psig=AOvVaw1mhHX5mDpOHgKyTeRxT7DD&ust=1727209405409000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCNDr9cfy2YgDFQAAAAAdAAAAABAR",
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.eonline.com%2Fnews%2Fkendrick_lamar&psig=AOvVaw1mhHX5mDpOHgKyTeRxT7DD&ust=1727209405409000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCNDr9cfy2YgDFQAAAAAdAAAAABAZ",
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.britannica.com%2Fbiography%2FKendrick-Lamar&psig=AOvVaw1mhHX5mDpOHgKyTeRxT7DD&ust=1727209405409000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCNDr9cfy2YgDFQAAAAAdAAAAABAp"
]

# Views for the quotes app

def quote(request):
  """
  This view displays a random quote and image.
  """
  # Select random quote and image index
  random_index = random.randint(0, len(quotes) - 1)
  random_quote = quotes[random_index]
  random_image = images[random_index]

  context = {
      'quote': random_quote,
      'image': random_image,
  }

  return render(request, 'quote.html', context)

def show_all(request):
  """
  This view displays all quotes and images.
  """
  context = {
      'quotes': quotes,
      'images': images,
  }

  return render(request, 'show_all.html', context)

def about(request):
  """
  This view displays the about page.
  """
  # Replace this with your actual information about the person
  about_text = """
  This application displays quotes from [Famous Person Name].
  [Famous Person Name] was [Brief Biography].
  This application was created by [Your Name].
  """

  context = {
      'about_text': about_text,
  }

  return render(request, 'about.html', context)