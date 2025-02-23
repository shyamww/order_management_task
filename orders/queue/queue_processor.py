import queue
import threading
import time
from datetime import datetime
import random
from django.utils import timezone
from orders.models import Order, OrderMetrics

class OrderQueue:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(OrderQueue, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.queue = queue.Queue()
        self.processing_thread = threading.Thread(target=self._process_orders, daemon=True)
        self.processing_thread.start()

    def add_order(self, order):
        self.queue.put(order)

    def _process_orders(self):
        while True:
            try:
                order = self.queue.get(timeout=1)  # 1 second timeout
                self._process_single_order(order)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing order: {e}")

    def _process_single_order(self, order):
        try:
            # Update order to processing status
            order.status = 'PROCESSING'
            order.processing_start_time = timezone.now()
            order.save()

            # Simulate processing time (1-5 seconds)
            processing_time = random.uniform(1, 5)
            time.sleep(processing_time)

            # Update order to completed status
            order.status = 'COMPLETED'
            order.processing_end_time = timezone.now()
            order.save()

            # Update metrics
            self._update_metrics()

        except Exception as e:
            print(f"Error processing order {order.order_id}: {e}")
            order.status = 'PENDING'
            order.save()

    def _update_metrics(self):
        try:
            metrics, created = OrderMetrics.objects.get_or_create(id=1)
            
            # Update order counts
            metrics.total_orders = Order.objects.count()
            metrics.pending_orders = Order.objects.filter(status='PENDING').count()
            metrics.processing_orders = Order.objects.filter(status='PROCESSING').count()
            metrics.completed_orders = Order.objects.filter(status='COMPLETED').count()

            # Calculate average processing time
            completed_orders = Order.objects.filter(
                status='COMPLETED',
                processing_start_time__isnull=False,
                processing_end_time__isnull=False
            )
            
            if completed_orders.exists():
                total_processing_time = sum(
                    (order.processing_end_time - order.processing_start_time).total_seconds()
                    for order in completed_orders
                )
                metrics.average_processing_time = total_processing_time / completed_orders.count()
            
            metrics.save()

        except Exception as e:
            print(f"Error updating metrics: {e}")

# Initialize queue
order_queue = OrderQueue()
