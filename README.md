# 🛡️ Full-Stack IDS System

A full-stack **Intrusion Detection System (IDS)** built as a group project. It captures live network traffic, detects attacks using rule-based heuristics, and displays real-time alerts on a web dashboard.

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────┐
│              Full-Stack IDS System               │
│                                                  │
│  ┌─────────────┐     HTTP/WS      ┌───────────┐  │
│  │  Frontend   │ ◄──────────────► │  Backend  │  │
│  │ React+Vite  │                  │  FastAPI  │  │
│  └─────────────┘                  └─────┬─────┘  │
│                                         │ HTTP    │
│                                   ┌─────▼──────┐  │
│                                   │Cybersecurity│ │
│                                   │IDS Engine   │ │
│                                   │(Scapy)      │ │
│                                   └────────────┘  │
└──────────────────────────────────────────────────┘
```

## 📦 Modules

| Module | Tech Stack | Description |
|---|---|---|
| [`backend/`](./backend/README.md) | FastAPI, PostgreSQL, SQLAlchemy | REST API server, authentication, WebSocket broadcaster |
| [`cybersecurity/`](./cybersecurity/README.md) | Python, Scapy | Live packet sniffer and rule-based attack detector |
| [`frontend/`](./frontend/README.md) | React 19, Vite, Recharts | Real-time IDS monitoring dashboard |

## 🚀 Quick Start

> Each module has its own detailed README with setup instructions. Follow the order below for a full system startup.

### 1. Start the Backend
```bash
cd backend
pip install -r requirements.txt
# Configure your .env file (see backend/README.md)
uvicorn run:app --reload
```

### 2. Start the IDS Engine
```bash
cd cybersecurity
pip install -r requirements.txt
sudo python3 main.py          # root required for raw packet capture
```

### 3. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔗 Default Ports

| Service | URL |
|---|---|
| Backend API | `http://localhost:8000` |
| Frontend Dashboard | `http://localhost:5173` |
| WebSocket | `ws://localhost:8000/ws/` |

## 🌿 Git Branches

This repository uses feature branches per team member:

| Branch | Responsibility |
|---|---|
| `main` | Stable, merged code |
| `backend` | Backend API development |
| `cybersecurity` | IDS detection engine |
| `frontend` | React dashboard |
| `v1` | First release snapshot |

## 🤝 Contributing

Each team member should work on their respective branch and open a pull request into `main` when a feature is complete.
