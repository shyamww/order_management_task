from django.contrib import admin
from .models import Order, OrderMetrics

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user_id')
    readonly_fields = ('created_at', 'updated_at', 'processing_start_time', 'processing_end_time')

@admin.register(OrderMetrics)
class OrderMetricsAdmin(admin.ModelAdmin):
    list_display = ('total_orders', 'pending_orders', 'processing_orders', 
                   'completed_orders', 'average_processing_time', 'last_updated')
    readonly_fields = ('last_updated',)
