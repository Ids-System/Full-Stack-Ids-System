# 🖥️ Frontend — IDS Dashboard

The frontend module of the Full-Stack IDS System. A real-time monitoring dashboard built with React and Vite. It authenticates users, displays live attack data via WebSocket, and provides an admin panel for user management and report exports.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **React 19** | UI framework |
| **Vite 8** | Build tool and dev server |
| **React Router DOM v7** | Client-side routing |
| **Axios** | HTTP client for REST API calls |
| **Recharts** | Charts and data visualizations |
| **Lucide React** | Icon library |
| **React Hot Toast** | Toast notifications |
| **date-fns** | Date formatting utilities |

## 📁 Project Structure

```
frontend/
├── index.html
├── vite.config.js
├── package.json
└── src/
    ├── main.jsx              # React app entry point
    ├── App.jsx               # Router setup and route definitions
    ├── index.css             # Global design system and styles
    ├── App.css               # App-level styles
    ├── api/
    │   ├── axios.js          # Axios instance with base URL and interceptors
    │   └── endpoints.js      # All API call functions
    ├── context/              # React context providers (auth, global state)
    ├── hooks/                # Custom React hooks (WebSocket, data fetching)
    ├── pages/                # Full-page route components
    │   ├── Login.jsx         # Login page
    │   ├── Dashboard.jsx     # Main dashboard with real-time data
    │   ├── AttacksHistory.jsx # Full attack log table
    │   ├── AttackIPs.jsx     # Table of attacker source IPs
    │   ├── AdminPanel.jsx    # Admin: user management + export
    │   └── Profile.jsx       # User profile and password change
    ├── components/           # Reusable UI components
    │   ├── cards/            # Stat/summary cards
    │   ├── charts/           # Recharts wrappers
    │   ├── layout/           # Sidebar, navbar, page layout
    │   ├── tables/           # Data table components
    │   └── ui/               # Generic UI primitives (buttons, modals, etc.)
    └── assets/               # Static assets (images, icons)
```

## ⚙️ Setup & Installation

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment

By default the Axios client points to `http://localhost:8000`. If your backend runs on a different host or port, update `src/api/axios.js`:

```js
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});
```

> `withCredentials: true` is **required** — the backend uses `HttpOnly` cookies for authentication. Without it, cookies will not be sent with cross-origin requests.

### 3. Start the Dev Server
```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

## 📜 Available Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start the Vite development server with HMR |
| `npm run build` | Build the production bundle to `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run `oxlint` for code linting |

## 🗺️ Pages & Routes

| Path | Component | Auth | Description |
|---|---|---|---|
| `/login` | `Login.jsx` | ❌ | Login form |
| `/` or `/dashboard` | `Dashboard.jsx` | ✅ | Real-time stats and live alerts |
| `/attacks` | `AttacksHistory.jsx` | ✅ | Full paginated attack log |
| `/attack-ips` | `AttackIPs.jsx` | ✅ | Source IPs that triggered attacks |
| `/admin` | `AdminPanel.jsx` | ✅ Admin only | User management and PDF report export |
| `/profile` | `Profile.jsx` | ✅ | View profile and change password |

## 🌐 API Integration

All API calls are made through the centralized `src/api/endpoints.js` module.

### Auth
```js
login(data)         // POST /users/login
logout()            // POST /users/logout
getMe()             // GET  /users/me
changePassword(data) // PUT  /users/password
```

### Dashboard
```js
getAttackIPs()      // GET /dashboard/attack-ips
getAttacks()        // GET /dashboard/attacks
getAlerts()         // GET /dashboard/alerts
getBlockedIPs()     // GET /dashboard/block-ips
getStatistics()     // GET /dashboard/statistics
```

### Admin
```js
getAllUsers()        // GET    /admin/users
addUser(data)        // POST   /admin/users
updateRole(data)     // PATCH  /admin/users
deleteUser(data)     // DELETE /admin/users
clearAttackHistory() // DELETE /admin/attack-history
exportReport()       // GET    /admin/export  (returns PDF blob)
```

## ⚡ Real-Time WebSocket

The dashboard connects to `ws://localhost:8000/ws/` for live attack alerts. The WebSocket connection is authenticated via the `access_token` cookie sent automatically with the handshake request (requires `withCredentials`).

When a new attack is detected by the IDS engine and forwarded through the backend, it is pushed to all connected clients immediately without polling.

## 🔐 Authentication Flow

1. User submits credentials on `/login`.
2. Backend sets `access_token` (30 min) and `refresh_token` (30 days) as `HttpOnly` cookies.
3. Axios automatically includes cookies on all subsequent requests.
4. When the access token expires, the app calls `POST /users/refresh` to silently obtain a new one.
5. On logout, both cookies are cleared.

## 🎨 Design System

Styles are written in vanilla CSS. The design system lives in `src/index.css` and defines:

- CSS custom properties for colors, spacing, and typography
- Dark-mode color scheme
- Reusable utility classes for layout and components
- Smooth transitions and hover/focus micro-animations

## 📦 Dependencies

### Runtime
| Package | Version | Use |
|---|---|---|
| `react` | ^19 | Core UI library |
| `react-dom` | ^19 | DOM rendering |
| `react-router-dom` | ^7 | Client-side routing |
| `axios` | ^1.20 | HTTP requests |
| `recharts` | ^3 | Data visualization charts |
| `lucide-react` | ^1.37 | Icon components |
| `react-hot-toast` | ^2.6 | Toast notifications |
| `date-fns` | ^4 | Date/time formatting |

### Dev
| Package | Version | Use |
|---|---|---|
| `vite` | ^8 | Build tool and dev server |
| `@vitejs/plugin-react` | ^6 | Vite React plugin |
| `oxlint` | ^1.79 | JavaScript/JSX linter |
