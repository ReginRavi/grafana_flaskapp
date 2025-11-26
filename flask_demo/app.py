"""
Flask Demo Application with Prometheus Metrics

This application demonstrates how to instrument a Python Flask app
with Prometheus metrics for observability.
"""

from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest
import time
import random

app = Flask(__name__)

# ==============================================================================
# METRIC DEFINITIONS
# ==============================================================================

# 1. Request Metrics (Standard Observability)
http_requests_total = Counter(
    'flask_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

# 2. Business Metrics (Custom Application Metrics)
orders_created_total = Counter(
    'app_orders_created_total',
    'Total number of orders created'
)

revenue_total = Counter(
    'app_revenue_total',
    'Total revenue in USD'
)

active_users = Gauge(
    'app_active_users',
    'Number of currently active users'
)

# 3. System Metrics (Application Health)
app_info = Info(
    'app',
    'Application information'
)

app_uptime_seconds = Gauge(
    'app_uptime_seconds',
    'Application uptime in seconds'
)

# Set application info
app_info.info({
    'version': '1.0.0',
    'environment': 'development',
    'name': 'flask-demo'
})

# Track start time for uptime calculation
start_time = time.time()

# ==============================================================================
# MIDDLEWARE - Automatic Request Tracking
# ==============================================================================

@app.before_request
def before_request():
    """Record request start time"""
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """Record request metrics after each request"""
    # Calculate request duration
    request_duration = time.time() - request.start_time
    
    # Get endpoint (route) name
    endpoint = request.endpoint or 'unknown'
    
    # Record metrics
    http_requests_total.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=endpoint
    ).observe(request_duration)
    
    # Update uptime
    app_uptime_seconds.set(time.time() - start_time)
    
    return response

# ==============================================================================
# ROUTES / ENDPOINTS
# ==============================================================================

@app.route('/')
def home():
    """Home page endpoint"""
    return jsonify({
        'message': 'Welcome to Flask Demo App with Prometheus Metrics!',
        'endpoints': {
            '/': 'This home page',
            '/api/users': 'Get list of users',
            '/api/orders': 'Create an order (POST)',
            '/api/health': 'Health check',
            '/metrics': 'Prometheus metrics'
        }
    })

@app.route('/api/users')
def get_users():
    """Get users endpoint - simulates database query"""
    # Simulate some processing time
    time.sleep(random.uniform(0.01, 0.1))
    
    # Simulate active users (random for demo)
    active_users.set(random.randint(10, 50))
    
    users = [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
    ]
    
    return jsonify({
        'count': len(users),
        'users': users
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create order endpoint - tracks business metrics"""
    # Simulate some processing time
    time.sleep(random.uniform(0.05, 0.2))
    
    # Simulate order amount (random for demo)
    order_amount = round(random.uniform(10.0, 500.0), 2)
    
    # Simulate occasional errors (10% failure rate)
    if random.random() < 0.1:
        return jsonify({
            'error': 'Payment processing failed'
        }), 500
    
    # Increment business metrics
    orders_created_total.inc()
    revenue_total.inc(order_amount)
    
    order_id = random.randint(1000, 9999)
    
    return jsonify({
        'success': True,
        'order_id': order_id,
        'amount': order_amount,
        'currency': 'USD'
    }), 201

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    uptime = time.time() - start_time
    
    return jsonify({
        'status': 'healthy',
        'uptime_seconds': round(uptime, 2),
        'timestamp': time.time()
    })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("Flask Demo Application with Prometheus Metrics")
    print("=" * 70)
    print("\nStarting server on http://localhost:8080")
    print("\nAvailable endpoints:")
    print("  - http://localhost:8080/           (Home)")
    print("  - http://localhost:8080/api/users  (Get users)")
    print("  - http://localhost:8080/api/orders (Create order - POST)")
    print("  - http://localhost:8080/api/health (Health check)")
    print("  - http://localhost:8080/metrics    (Prometheus metrics)")
    print("\n" + "=" * 70)
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
