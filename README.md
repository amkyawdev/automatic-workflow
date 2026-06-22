# Automatic Workflow

Modern workflow automation platform built with FastAPI + Vanilla JS.

## 🚀 Quick Start

### Frontend (Static - GitHub Pages)
```bash
cd frontend/src
# Open pages/index.html in browser
```

### Backend (Vercel)
```bash
cd backend
cp .env.example .env
# Edit .env with your values
vercel --prod
```

## 📁 Project Structure

```
├── frontend/          # Static site (HTML/CSS/JS)
│   └── src/
│       ├── pages/     # HTML pages
│       ├── styles/    # CSS files
│       └── scripts/   # JavaScript modules
│
├── backend/           # FastAPI backend
│   ├── api/          # Vercel entry point
│   ├── src/
│   │   ├── core/     # Domain logic
│   │   ├── infrastructure/  # External services
│   │   └── presentation/   # API routes
│   └── vercel.json   # Vercel config
│
├── .github/workflows/ # CI/CD
└── README.md
```

## 🌐 Deployment

### Frontend → GitHub Pages
1. Go to repo Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/frontend/src`

### Backend → Vercel
1. Create Vercel project
2. Link to `backend/` directory
3. Add environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `OPENAI_API_KEY`
4. Deploy

## 🔑 Environment Variables

See `.env.example` for required variables.

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/workflows` | List workflows |
| POST | `/api/v1/workflows` | Create workflow |
| POST | `/api/v1/workflows/{id}/execute` | Execute workflow |
| POST | `/api/v1/integrations/connect` | Connect integration |
| POST | `/api/v1/chat` | Chat with AI assistant |

## 🛠️ Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn src.presentation.app:app --reload

# Frontend
# Just open frontend/src/pages/index.html
```

## 📄 License

MIT
