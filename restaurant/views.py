from django.shortcuts import render, redirect
from django.utils import timezone
import random
import datetime

def main(request):
    context = {
        'restaurant_name': 'El Coqui',
        'location': '123 Main St, Manhattan, NY',
        'hours_of_operation': {
            'Monday': {'open': '9:00 AM', 'close': '10:00 PM'},
            'Tuesday': {'open': '9:00 AM', 'close': '10:00 PM'},
            'Wednesday': {'open': '9:00 AM', 'close': '10:00 PM'},
            'Thursday': {'open': '9:00 AM', 'close': '10:00 PM'},
            'Friday': {'open': '9:00 AM', 'close': '11:00 PM'},
            'Saturday': {'open': '10:00 AM', 'close': '11:00 PM'},
            'Sunday': {'open': '10:00 AM', 'close': '9:00 PM'},
        },
        'images': [
            'images/pernilyarroz.jpg',
            'images/bistec.jpg',
            'images/empanadas.jpg',
        ],
    }
    return render(request, 'main.html', context)


def order(request):
    daily_special = {
        'name': 'Pollo Guisado',
        'description': 'Tender chicken stew with a side of rice and beans.',
        'price': '8.99'
    }
    
    context = {
        'daily_special': daily_special
    }
    
    return render(request, 'order.html', context)


def confirmation(request):
    if request.method == 'POST':
        ordered_items = []
        total_price = 0

        # Define menu items and their prices
        menu_items = {
            'Bistec Encebollado': 12.99,
            'Empanadas': 3.00,
            'Pernil con Arroz': 10.99,
            'Daily Special': 8.99
        }

        # Check for ordered items and calculate the total price
        for item, price in menu_items.items():
            if item in request.POST.getlist('items'):  # Check if the item was selected
                # Get the quantity from the form or default to 1
                quantity = int(request.POST.get(f'{item.lower().replace(" ", "-")}-quantity', 1))
                item_total = price * quantity
                ordered_items.append({'name': item, 'price': item_total, 'quantity': quantity})
                total_price += item_total

        # Customer Information
        customer_name = request.POST.get('name', '')
        customer_phone = request.POST.get('phone', '')
        customer_email = request.POST.get('email', '')
        special_instructions = request.POST.get('instructions', '')

        # Calculate the ready time (30-60 minutes from now)
        current_time = timezone.now()
        ready_time_offset = datetime.timedelta(minutes=random.randint(30, 60))
        ready_time = (current_time + ready_time_offset).strftime('%I:%M %p')

        # Context for the template
        context = {
            'ordered_items': ordered_items,
            'total_price': f"{total_price:.2f}",  # Format the total price to 2 decimal places
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ready_time': ready_time,
        }

        return render(request, 'confirmation.html', context)
    else:
        # Redirect to the order page if accessed directly
        return redirect('order')
