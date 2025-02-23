from rest_framework import serializers
from orders.models import Order, OrderMetrics
import json

class OrderSerializer(serializers.ModelSerializer):
    item_ids = serializers.ListField(child=serializers.IntegerField(), required=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user_id', 'item_ids', 'total_amount', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def create(self, validated_data):
        item_ids = validated_data.pop('item_ids')
        validated_data['_item_ids'] = json.dumps(item_ids)
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['item_ids'] = json.loads(instance._item_ids)
        return representation

class OrderMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMetrics
        fields = ['total_orders', 'pending_orders', 'processing_orders', 
                 'completed_orders', 'average_processing_time', 'last_updated']