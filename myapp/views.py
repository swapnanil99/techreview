# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_POST
import json
import re
import random
from datetime import datetime, timedelta

AFFILIATE_TEMPLATE = "https://www.amazon.in/dp/{product_id}/?linkCode=ll2&tag=techrevie006f-21&linkId=a1ecb441a060cd526b75501f72ae27c0&language=en_IN&ref_=as_li_ss_tl"

@ensure_csrf_cookie
def home(request):
    """Render main homepage and ensure CSRF cookie is sent."""
    return render(request, 'myapp/index.html')



@csrf_protect
@require_POST
def track_price(request):
    """Handle AJAX POST requests for tracking price."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request type'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        url = data.get("link")

        if not url:
            return JsonResponse({"error": "No URL provided"}, status=400)

        # Extract product ID (ASIN) for validation
        match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if not match:
            return JsonResponse({"error": "Invalid Amazon product link"}, status=400)

        # Generate realistic price data for the chart
        import random
        from datetime import datetime, timedelta
        
        # Generate 12 months of price data with good variation
        months = []
        prices = []
        base_price = random.randint(2000, 50000)  # Random base price between 2k-50k
        
        for i in range(12):
            date = datetime.now() - timedelta(days=30*i)
            months.append(date.strftime('%b %Y'))
            # Generate price with good variation (±25%)
            variation = random.uniform(0.75, 1.25)
            price = int(base_price * variation)
            prices.append(price)
        
        # Reverse to show oldest to newest
        months.reverse()
        prices.reverse()
        
        # Ensure we have good min/max differences
        min_price = min(prices)
        max_price = max(prices)
        
        # If difference is too small, adjust some prices
        if max_price - min_price < base_price * 0.15:  # Less than 15% variation
            # Make some prices higher and some lower
            prices[0] = int(min_price * 0.8)  # Lower first price
            prices[6] = int(max_price * 1.2)  # Higher middle price
            prices[11] = int((min_price + max_price) / 2)  # Current price in middle
        
        return JsonResponse({
            "min": min(prices),
            "max": max(prices),
            "months": months,
            "prices": prices,
            "link": url
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data received'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@csrf_protect
@require_POST
def convert_affiliate(request):
    """Convert Amazon link to your affiliate link."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request type'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        url = data.get("link")

        if not url:
            return JsonResponse({"error": "No URL provided"}, status=400)

        # Extract product ID (ASIN)
        match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if not match:
            return JsonResponse({"error": "Invalid Amazon product link"}, status=400)

        product_id = match.group(1)
        affiliate_link = AFFILIATE_TEMPLATE.format(product_id=product_id)

        return JsonResponse({"affiliate_link": affiliate_link})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data received'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
