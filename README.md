## 📺 Project Demo

https://youtu.be/E4rTYlLNCkI

# Chatbot (A.B Deliveries)

Full-stack Hebrew chatbot for customer service and delivery inquiries. FastAPI backend with Google Gemini and a React (Vite) frontend.

## Tech stack

- **Backend:** FastAPI, Uvicorn, Google Generative AI (Gemini), Pydantic, pandas (Excel logging)
- **Frontend:** React 18, Vite, Tailwind CSS, lucide-react

## Features

- Hebrew RTL chat interface with personalized welcome
- Dark mode toggle
- Model selection: Gemini 1.5 Flash (fast) or Gemini 1.5 Pro (advanced)
- Optional Excel conversation logging when user name and phone are provided
- One-command run for backend and frontend

## Project structure

```
.
├── run_app.py              # Start backend + frontend with one command
├── .env.example             # Copy to .env and add GEMINI_API_KEY
├── backend/
│   ├── main.py              # FastAPI app entry (uvicorn main:app)
│   ├── config.py            # CORS, port, env loading
│   ├── models.py            # Pydantic request/response models
│   ├── routers/             # API route handlers (health, chat)
│   ├── services/            # AI (Gemini) and Excel logging
│   ├── requirements.txt
│   └── run.ps1              # Run backend only (Windows)
└── frontend/
    ├── src/
    │   ├── api/             # chatService.js
    │   ├── components/      # WelcomeForm, ChatHeader, MessageList, etc.
    │   ├── hooks/           # useLocalStorage
    │   ├── config.js
    │   ├── constants.js
    │   └── App.jsx
    ├── package.json
    └── vite.config.js
```

## Quick start

From the **project root**:

```bash
python run_app.py
```

- **Backend:** http://localhost:3002  
- **Frontend:** http://localhost:5173  

Press **Ctrl+C** to stop both.

## Prerequisites

- **Python 3** (backend and run script)
- **Node.js & npm** (frontend)
- A **`.env`** file in the project root with:

  ```
  GEMINI_API_KEY=your_key_here
  ```

  Get a key at [Google AI Studio](https://aistudio.google.com/app/apikey).

## Optional: Backend virtual environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cd ..
```

Then run `python run_app.py` from the project root; it will use the backend venv if present.

## Running backend or frontend alone

- **Backend only:** `cd backend`, then `.\run.ps1` (Windows) or:
  ```bash
  python -m uvicorn main:app --host 0.0.0.0 --port 3002
  ```
- **Frontend only:** `cd frontend`, then `npm run dev`.

## Troubleshooting

**"WinError 10013" (socket access forbidden)**  
Port 3002 may be in use. Use another port: set `CHATBOT_PORT=5000` (e.g. `$env:CHATBOT_PORT="5000"` in PowerShell) when starting the backend, and in `frontend/.env` set `VITE_API_URL=http://localhost:5000`.

---

**Repository:** [github.com/orior11/chatbot](https://github.com/orior11/chatbot)
