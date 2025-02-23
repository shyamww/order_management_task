# Order Processing System

A Django-based backend system for processing e-commerce orders with asynchronous queue processing and metrics reporting.

## Setup Instructions

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Orders

1. Create Order
```bash
POST /api/orders/
Content-Type: application/json

{
    "user_id": "user123",
    "item_ids": [1, 2, 3],
    "total_amount": 99.99
}
```

2. Get Order Status
```bash
GET /api/orders/{order_id}/status/
```

3. List All Orders
```bash
GET /api/orders/
```


```bash
# curl to create new order
curl -X POST http://localhost:8000/api/orders/ \
     -H "Content-Type: application/json" \
     -d '{"user_id": "user44", "item_ids": [1, 2, 3], "total_amount": 90.99}'
```

```bash
# curl for single order status check
curl http://localhost:8000/api/orders/{order_id}/status/
```

```bash
# curl for monitoring metrics
curl http://localhost:8000/api/metrics/
```





### Metrics

1. Get System Metrics
```bash
GET /api/metrics/
```

## Design Decisions and Trade-offs

1. **In-Memory Queue**
   - Using Python's built-in Queue for simplicity
   - Trade-off: Not persistent across server restarts
   - Alternative: Could use Redis/RabbitMQ for production

2. **Database**
   - Using SQLite for development
   - Can be easily switched to PostgreSQL/MySQL for production

3. **Concurrency**
   - Using threading for queue processing
   - Trade-off: Limited by Python's GIL
   - Alternative: Could use Celery for distributed task processing

4. **Metrics**
   - Storing in database for persistence
   - Trade-off: Additional database operations
   - Alternative: Could use Redis for faster access

## Assumptions

1. Orders are processed in FIFO order
2. Processing time is simulated (1-5 seconds)
3. System runs on a single server
4. No authentication required (add JWT/OAuth for production)
5. Order IDs are UUID4 if not provided

## Load Testing

To test the system's ability to handle 1,000 concurrent orders:

```bash
# Using curl for testing
for i in {1..1000}; do
    curl -X POST http://localhost:8000/api/orders/ \
    -H "Content-Type: application/json" \
    -d '{"user_id":"test_user","item_ids":[1,2],"total_amount":99.99}' &
done
```
