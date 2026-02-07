# Docs Deployment

*Documentation: E2E Test Documentation*

---

## Deployment Guide

**Source:** http://127.0.0.1:12083/docs/deployment

# Deployment Guide
Deploy AnyDocsMCP to production using Docker or traditional server setups.
## Docker Deployment
The recommended way to deploy is using Docker Compose:
```
version: '3.8'
services:
  anydocs:
    image: anydocs-mcp:latest
    ports:
      - "3000:3000"
    volumes:
      - ./docs:/app/docs
    environment:
      - NODE_ENV=production
      - API_KEY=${API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```
## Environment Variables
Configure the server using these environment variables:
* **NODE\_ENV** - Set to 'production' for optimized performance
* **API\_KEY** - Secret key for API authentication
* **DOCS\_PATH** - Path to documentation directory (default: ./docs)
* **PORT** - Server port (default: 3000)
* **LOG\_LEVEL** - Logging verbosity: debug, info, warn, error
## Production Checklist
Before going to production, verify the following:
```dockerfile
# 1. Build the production image
docker build -t anydocs-mcp:latest .
# 2. Run security scan
docker scan anydocs-mcp:latest
# 3. Test the health endpoint
docker run -d -p 3000:3000 anydocs-mcp:latest
curl http://localhost:3000/health
# 4. Verify search functionality
curl "http://localhost:3000/api/v1/search?q=test"
```
## Monitoring
The server exposes Prometheus-compatible metrics at `/metrics`:
```dockerfile
from prometheus_client import Counter, Histogram
search_requests = Counter('search_total', 'Total search requests')
search_latency = Histogram('search_latency_seconds', 'Search latency')
index_size = Gauge('index_sections_total', 'Total indexed sections')
```
Set up alerts for search latency exceeding 200ms and error rates above 1%.

---

