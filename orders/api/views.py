import logging
import uuid
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from orders.models import Order, OrderMetrics
from orders.api.serializers import OrderSerializer, OrderMetricsSerializer
from orders.queue.queue_processor import order_queue

logger = logging.getLogger(__name__)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'

    def create(self, request, *args, **kwargs):
        try:
            # Log only request.data
            logger.error(f"Request data: {request.data}")

            # Generate a unique order_id if not provided
            if 'order_id' not in request.data:
                request.data['order_id'] = str(uuid.uuid4())

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            
            # Add order to processing queue
            order_queue.add_order(order)
            
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def status(self, request, order_id=None):
        try:
            order = self.get_object()
            return Response({
                'order_id': order.order_id,
                'status': order.status,
                'created_at': order.created_at
            })
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class MetricsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderMetrics.objects.all()
    serializer_class = OrderMetricsSerializer

    def list(self, request, *args, **kwargs):
        # Get or create metrics instance
        metrics, created = OrderMetrics.objects.get_or_create(id=1)
        serializer = self.get_serializer(metrics)
        return Response(serializer.data)
