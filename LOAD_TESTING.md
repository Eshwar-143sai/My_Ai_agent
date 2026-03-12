# Load Testing the AI Enterprise Agent

This project uses **Locust** to simulate concurrent users and test the reliability and latency of the LLM pipelines and FastAPI endpoints.

## 1. Setup

Ensure you have locust installed:
```bash
pip install locust
```

## 2. Running Locust

Start the Locust web server locally:
```bash
locust -f locustfile.py
```

Then, open your browser and navigate to `http://localhost:8089`.

## 3. Configuration

In the Locust web interface, you can configure:
- **Number of peak users**
- **Spawn rate** (users spawned per second)
- **Host address** (e.g., `http://localhost:8000`)

Locust will report:
- Total Requests generated
- Requests Per Second (RPS)
- Median / 95th Percentile Response Time
- Failures

Run this test to ensure your API handles concurrency when bound to heavy LangGraph operations!
