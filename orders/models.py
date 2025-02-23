from django.db import models
import json

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
    ]

    order_id = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100)
    _item_ids = models.TextField(db_column='item_ids', default='[]')  # Store as JSON string
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processing_start_time = models.DateTimeField(null=True, blank=True)
    processing_end_time = models.DateTimeField(null=True, blank=True)

    @property
    def item_ids(self):
        return json.loads(self._item_ids)

    @item_ids.setter
    def item_ids(self, value):
        self._item_ids = json.dumps(value)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

class OrderMetrics(models.Model):
    total_orders = models.IntegerField(default=0)
    pending_orders = models.IntegerField(default=0)
    processing_orders = models.IntegerField(default=0)
    completed_orders = models.IntegerField(default=0)
    average_processing_time = models.FloatField(default=0.0)  # in seconds
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order Metrics'
        verbose_name_plural = 'Order Metrics'