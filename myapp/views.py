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
    try:
        data = json.loads(request.body.decode('utf-8'))
        amazon_link = data.get('link')

        if not amazon_link or "/dp/" not in amazon_link:
            return JsonResponse({'error': 'Invalid Amazon link'}, status=400)

        try:
            asin = amazon_link.split("/dp/")[1][:10]
        except Exception:
            return JsonResponse({'error': 'Cannot extract ASIN'}, status=400)

        # Dummy test data — replace with real API logic later
        months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
        prices = [4999, 4799, 4599, 4899, 5200, 5000, 4800, 4700, 4600, 4500, 4400, 4300]

        return JsonResponse({
            'asin': asin,
            'months': months,
            'prices': prices,
            'min': min(prices),
            'max': max(prices),
            'link': amazon_link
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
