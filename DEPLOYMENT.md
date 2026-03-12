# Deployment Guide

This guide covers deploying the Enterprise AI Agent to an AWS EC2 instance.

## 1. Provision EC2 Instance
- Launch an Ubuntu 22.04 LTS instance (t3.medium or larger recommended for reasonable API response times).
- In the security group, open ports:
  - `8000` (FastAPI Server)
  - `3000` (Grafana Dashboard)
  - `22` (SSH for access)

## 2. Server Setup
SSH into your instance and install Docker:
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

## 3. Clone and Run
Clone the repository:
```bash
git clone https://github.com/Eshwar-143sai/My_Ai_agent.git
cd My_Ai_agent
```

Set up your `.env` file with the necessary provider keys (OpenAI, Anthropic):
```bash
nano .env
```

Execute the deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 4. Verification
- **API Status:** `http://<EC2_PUBLIC_IP>:8000/docs`
- **Grafana Metrics:** `http://<EC2_PUBLIC_IP>:3000` (Default login: `admin` / `admin`)
