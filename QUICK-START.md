# 🎯 Quick Reference Card

## 🚀 Start Application
```bash
# Double-click this file:
start-app.bat

# Or manually:
# Terminal 1: cd backend && python -m uvicorn main:app --reload --port 8001
# Terminal 2: cd frontend && npm run dev
```

## 🛑 Stop Application
```bash
# Double-click this file:
stop-app.bat

# Or press Ctrl+C in both terminals
```

## 🌐 URLs
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs
- **Health:** http://localhost:8001/health

## 🔑 Default Ports
- Frontend: `3000`
- Backend: `8001`

## 📁 Important Files
- `backend/.env` - Backend configuration
- `frontend/.env.local` - Frontend configuration
- `start-app.bat` - Start script
- `stop-app.bat` - Stop script

## 🐛 Quick Fixes

### Port in use?
```bash
stop-app.bat
```

### Backend not working?
```bash
cd backend
pip install -r requirements.txt
```

### Frontend not working?
```bash
cd frontend
npm install
```

### Database error?
- Check internet connection
- Verify DATABASE_URL in backend/.env

## 📊 Tech Stack
- **Frontend:** Next.js 16 + React 19 + TypeScript
- **Backend:** FastAPI + Python 3.14
- **Database:** PostgreSQL (Neon Cloud)
- **Auth:** JWT + bcrypt

## ✨ Features
✅ User Auth | ✅ CRUD Tasks | ✅ Categories | ✅ Priorities
✅ Due Dates | ✅ Search | ✅ Dark Mode | ✅ Responsive

---

**Need detailed help?** Read `README.md` or `README-URDU.md`
