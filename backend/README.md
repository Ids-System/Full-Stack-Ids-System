# ⚙️ Backend — FastAPI REST API

The backend module of the Full-Stack IDS System. It provides a secure REST API and a real-time WebSocket server for the frontend dashboard. It also exposes an internal engine endpoint for the cybersecurity module to submit detected attacks.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework and REST API |
| **SQLAlchemy** | ORM for database interaction |
| **PostgreSQL** | Relational database (via `psycopg2`) |
| **PyJWT** | JWT-based authentication (access + refresh tokens) |
| **Uvicorn** | ASGI server |
| **WebSockets** | Real-time push alerts to connected clients |
| **ReportLab** | PDF report generation |
| **bcrypt** | Password hashing |

## 📁 Project Structure

```
backend/
├── app/
│   └── main.py             # FastAPI app factory, router registration
├── auth/
│   ├── jwt_token.py        # JWT creation, verification, WS token parsing
│   └── engine_auth.py      # Engine API key authentication
├── db/
│   └── database.py         # SQLAlchemy engine and session setup
├── dependencies/
│   └── auth.py             # Dependency injectors (get_current_user, is_admin)
├── models/                 # SQLAlchemy ORM models
│   ├── Users_models.py
│   ├── Attacks.py
│   ├── Alerts.py
│   ├── Attackips.py
│   ├── Blocked_ips.py
│   ├── statistics.py
│   └── token_models.py     # Token blacklist model
├── routes/                 # API route handlers
│   ├── users_routes.py     # Auth: login, logout, refresh, profile
│   ├── admin.py            # Admin: user management, report export
│   ├── dashboard.py        # Dashboard: attack data endpoints
│   ├── engine.py           # Engine: receive alerts from IDS module
│   └── websockets.py       # WebSocket: real-time client connections
├── schemas/                # Pydantic request/response schemas
├── services/               # Business logic layer
│   ├── user_services.py
│   ├── admin_services.py
│   ├── dashboard_services.py
│   ├── engine_services.py
│   └── report_services.py  # PDF generation logic
├── socket_manager/
│   └── manager.py          # WebSocket connection manager
├── tests/                  # Pytest test suite
├── .env                    # Environment variables (do not commit)
├── requirements.txt        # Python dependencies
└── run.py                  # App entrypoint — creates DB tables and runs app
```

## ⚙️ Setup & Installation

### 1. Create a Virtual Environment
```bash
cd backend
python3 -m venv env
source env/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
DATABASE_URL=postgresql://user:password@localhost:5432/ids_db
ENGINE_KEY=your_engine_api_key_here
```

| Variable | Description |
|---|---|
| `SECRET_KEY` | Secret used to sign JWT tokens |
| `ALGORITHM` | JWT signing algorithm (e.g. `HS256`) |
| `DATABASE_URL` | PostgreSQL connection string |
| `ENGINE_KEY` | Shared key for IDS engine → backend authentication |

### 4. Run the Server
```bash
uvicorn run:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

## 🔐 Authentication

The backend uses **cookie-based JWT authentication** with two tokens:

| Token | Lifetime | Cookie Name |
|---|---|---|
| Access Token | 30 minutes | `access_token` |
| Refresh Token | 30 days | `refresh_token` |

Both cookies are `HttpOnly` and `SameSite=Lax`. The access token is verified on every protected route via the `get_current_user` dependency. Expired access tokens can be refreshed using `POST /users/refresh`.

Token blacklisting is implemented to invalidate refresh tokens on logout.

## 🌐 API Reference

### Auth — `/users`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/users/login` | ❌ | Login with credentials, sets cookies |
| `POST` | `/users/logout` | ✅ | Logout and clear cookies |
| `GET` | `/users/me` | ✅ | Get current user details |
| `PUT` | `/users/password` | ✅ | Change password |
| `POST` | `/users/refresh` | ✅ (refresh cookie) | Refresh access token |

### Dashboard — `/dashboard`

All endpoints require a valid access token.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/dashboard/attack-ips` | List all source IPs that triggered attacks |
| `GET` | `/dashboard/attacks` | Full attack history |
| `GET` | `/dashboard/alerts` | System alerts |
| `GET` | `/dashboard/block-ips` | List of blocked IPs |
| `GET` | `/dashboard/statistics` | Attack count statistics by day |

### Admin — `/admin`

Requires admin role.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/admin/users` | List all users |
| `POST` | `/admin/users` | Add a new user |
| `PATCH` | `/admin/users` | Update a user's role |
| `DELETE` | `/admin/users` | Delete a user |
| `DELETE` | `/admin/attack-history` | Clear all attack history data |
| `GET` | `/admin/export` | Download PDF security report |

### IDS Engine — `/engine`

Authenticated via `X-Engine-Key` header (set `ENGINE_KEY` in `.env`).

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/engine/report` | Receive an attack alert from the IDS engine |

### WebSocket — `/ws`

| Endpoint | Description |
|---|---|
| `ws://localhost:8000/ws/` | Real-time alert stream; authenticated via `access_token` cookie |

## 🗃️ Database Models

| Model | Table | Description |
|---|---|---|
| `User` | `users` | System users with roles (`admin` / `analyst`) |
| `Attacks` | `attacks` | Logged attack events |
| `Alerts` | `alerts` | System-generated alerts |
| `AttackIP` | `attack_ips` | Source IPs that triggered attacks |
| `Blockedips` | `blocked_ips` | Manually or automatically blocked IPs |
| `AttackDays` | `attack_days` | Aggregated daily attack statistics |
| `TokenBlacklist` | `token_blacklist` | Invalidated refresh tokens |

## 🧪 Running Tests

```bash
pytest tests/
```

## 📄 PDF Report

Admins can download a full security report via `GET /admin/export`. The report is generated with ReportLab and includes attack summaries, statistics, and IP listings.
