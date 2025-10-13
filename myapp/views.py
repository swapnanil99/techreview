# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_POST
import json

@ensure_csrf_cookie
def home(request):
    """Render main homepage and ensure CSRF cookie is sent."""
    return render(request, 'myapp/index.html')


@csrf_protect
@require_POST
def track_price(request):
    """Handle AJAX POST requests for tracking price."""
    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request type'}, status=400)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        amazon_link = data.get('link')

        if not amazon_link:
            return JsonResponse({'error': 'Amazon link is required'}, status=400)
            
        if "/dp/" not in amazon_link:
            return JsonResponse({'error': 'Invalid Amazon link format'}, status=400)

        try:
            asin = amazon_link.split("/dp/")[1][:10]
            if len(asin) < 10:
                return JsonResponse({'error': 'Invalid ASIN in Amazon link'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Cannot extract ASIN from link'}, status=400)

        # Generate realistic dummy data based on ASIN for demo purposes
        import random
        random.seed(hash(asin) % 1000)  # Consistent data for same ASIN
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        base_price = random.randint(1000, 10000)
        prices = []
        
        for i in range(12):
            variation = random.randint(-500, 500)
            price = max(100, base_price + variation + (i * 50))  # Slight trend
            prices.append(price)

        return JsonResponse({
            'asin': asin,
            'months': months,
            'prices': prices,
            'min': min(prices),
            'max': max(prices),
            'link': amazon_link,
            'current_price': prices[-1]  # Current price (last month)
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data received'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
