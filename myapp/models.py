from django.db import models
from django.utils import timezone

class PriceHistory(models.Model):
    asin = models.CharField(max_length=10, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    title = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    url = models.URLField(max_length=1000, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['asin', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.asin} - ₹{self.price} ({self.timestamp.strftime('%Y-%m-%d')})"
