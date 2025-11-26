# Flask Demo Application with Prometheus Metrics

A demonstration Flask web application instrumented with Prometheus metrics for observability.

## Features

✅ **5 HTTP Endpoints** with automatic request tracking  
✅ **Prometheus Metrics** exposed on `/metrics`  
✅ **Business Metrics** (orders, revenue)  
✅ **System Metrics** (uptime, active users)  

---

## Quick Start

### 1. Install Dependencies

```bash
cd flask_demo
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The app will start on **http://localhost:8080**

---

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with API documentation |
| `/api/users` | GET | Get list of users (demo data) |
| `/api/orders` | POST | Create an order (generates business metrics) |
| `/api/health` | GET | Health check endpoint |
| `/metrics` | GET | Prometheus metrics endpoint |

---

## Testing the Application

### Get Users
```bash
curl http://localhost:8080/api/users
```

### Create Order
```bash
curl -X POST http://localhost:8080/api/orders
```

### View Metrics
```bash
curl http://localhost:8080/metrics
```

### Health Check
```bash
curl http://localhost:8080/api/health
```

---

## Metrics Exposed

### Request Metrics
- `flask_http_requests_total` - Total HTTP requests by method, endpoint, status
- `flask_http_request_duration_seconds` - Request latency histogram

### Business Metrics
- `app_orders_created_total` - Total orders created
- `app_revenue_total` - Total revenue in USD
- `app_active_users` - Current active users (gauge)

### System Metrics
- `app_info` - Application version and environment info
- `app_uptime_seconds` - Application uptime

---

## Prometheus Query Examples

Once Alloy is scraping this app, you can query in Prometheus:

```promql
# Request rate per second
rate(flask_http_requests_total[1m])

# 95th percentile latency
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket[5m]))

# Total orders created
app_orders_created_total

# Revenue per minute
rate(app_revenue_total[1m]) * 60
```

---

## Next Steps

1. ✅ Application is running
2. Configure Alloy to scrape metrics (see main README)
3. View metrics in Prometheus
4. Create Grafana dashboard

---

## Architecture

```
Flask App :8080 → Alloy :12345 → Prometheus :19090 → Grafana :3000
```

The application exposes metrics which are scraped by Alloy, sent to Prometheus, and visualized in Grafana.
