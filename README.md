# 🚀 Full-Stack Todo Application

A modern, feature-rich todo application built with **Next.js 16** (frontend) and **FastAPI** (backend).

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Node](https://img.shields.io/badge/node-18.18+-green.svg)

---

## ✨ Features

- ✅ **User Authentication** - Secure JWT-based authentication
- ✅ **Task Management** - Create, read, update, delete tasks
- ✅ **Categories** - Organize tasks by category (Work, Personal, Shopping, Health, Other)
- ✅ **Priority Levels** - Set task priorities (High, Medium, Low)
- ✅ **Due Dates** - Track task deadlines
- ✅ **Search** - Quickly find tasks
- ✅ **Dark/Light Theme** - Toggle between themes
- ✅ **Responsive Design** - Works on mobile and desktop
- ✅ **Real-time Stats** - View task statistics

---

## 🚀 Quick Start

### **Option 1: One-Click Start (Recommended)**

Simply double-click the `start-app.bat` file in the project root.

### **Option 2: Manual Start**

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open Browser:**
```
http://localhost:3000
```

---

## 🛑 Stop Servers

### **Option 1: Stop Script**
Double-click `stop-app.bat`

### **Option 2: Manual**
Press `Ctrl+C` in both terminal windows

---

## 🏗️ Tech Stack

### **Frontend**
- **Framework:** Next.js 16.1.5 (App Router)
- **UI Library:** React 19.2.3
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Notifications:** React Hot Toast
- **Language:** TypeScript

### **Backend**
- **Framework:** FastAPI 0.128.0
- **Database:** PostgreSQL (Neon Cloud)
- **ORM:** SQLModel 0.0.24
- **Authentication:** JWT with bcrypt
- **Server:** Uvicorn (ASGI)
- **Language:** Python 3.14

---

## 📂 Project Structure

```
Hackthon_Full-Stack_App/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py        # Authentication routes
│   │   │   └── tasks.py       # Task CRUD routes
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── database.py        # Database connection
│   │   ├── auth.py            # JWT utilities
│   │   ├── config.py          # Configuration
│   │   └── dependencies.py    # FastAPI dependencies
│   ├── main.py                # Application entry point
│   ├── .env                   # Environment variables
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Next.js Frontend
│   ├── app/
│   │   ├── page.tsx           # Landing page
│   │   ├── layout.tsx         # Root layout
│   │   └── dashboard/
│   │       └── page.tsx       # Dashboard page
│   ├── components/            # React components
│   │   ├── AuthForm.tsx       # Login/Register form
│   │   ├── TaskList.tsx       # Task list component
│   │   ├── TaskItem.tsx       # Individual task
│   │   └── TaskForm.tsx       # Create/Edit task form
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   ├── types.ts           # TypeScript types
│   │   └── constants.ts       # App constants
│   ├── .env.local             # Environment variables
│   └── package.json           # Node dependencies
│
├── start-app.bat              # Quick start script
├── stop-app.bat               # Stop servers script
├── README.md                  # This file
└── README-URDU.md             # Urdu/Hindi guide
```

---

## 🌐 API Endpoints

### **Authentication**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### **Tasks**
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task by ID
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle completion

### **Health**
- `GET /` - API info
- `GET /health` - Health check

**API Documentation:** http://localhost:8001/docs

---

## 🔧 Configuration

### **Backend Environment Variables** (`backend/.env`)
```bash
# Database
DATABASE_URL=postgresql+psycopg://user:pass@host/db

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8001
```

### **Frontend Environment Variables** (`frontend/.env.local`)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## 📦 Installation

### **Prerequisites**
- Python 3.14+
- Node.js 18.18+
- Internet connection (for cloud database)

### **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

### **Frontend Setup**
```bash
cd frontend
npm install
```

---

## 🧪 Testing

### **Test Backend Health**
```bash
curl http://localhost:8001/health
```

### **Test Frontend**
```bash
curl http://localhost:3000
```

### **Test API Documentation**
Open: http://localhost:8001/docs

---

## 🐛 Troubleshooting

### **Port Already in Use**
```bash
# Run stop script
stop-app.bat

# Or manually kill processes
netstat -ano | findstr :8001
taskkill /F /PID <PID>
```

### **Database Connection Error**
- Check internet connection
- Verify `DATABASE_URL` in `backend/.env`
- Ensure Neon database is accessible

### **Frontend Not Loading**
```bash
cd frontend
npm install
npm run dev
```

### **Backend Import Errors**
```bash
cd backend
pip install -r requirements.txt
```

---

## 📊 Database Schema

### **Users Table**
- `id` (UUID) - Primary key
- `email` (String) - Unique, indexed
- `name` (String)
- `hashed_password` (String)
- `created_at` (DateTime)

### **Tasks Table**
- `id` (Integer) - Primary key
- `user_id` (UUID) - Foreign key to users
- `title` (String)
- `description` (String, optional)
- `completed` (Boolean)
- `category` (String, optional)
- `priority` (String)
- `due_date` (DateTime, optional)
- `order` (Integer)
- `created_at` (DateTime)
- `updated_at` (DateTime)

---

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Bcrypt password hashing
- ✅ CORS protection
- ✅ SQL injection prevention (SQLModel ORM)
- ✅ Input validation (Pydantic)
- ✅ Secure environment variables

---

## 🚀 Deployment

### **Backend (Render.com)**
- See `backend/RENDER_DEPLOYMENT_GUIDE.md`

### **Frontend (Vercel)**
- See `FRONTEND_DEPLOYMENT_COMPLETE.md`

---

## 📝 Development

### **Backend Development**
```bash
cd backend
python -m uvicorn main:app --reload --port 8001
```

### **Frontend Development**
```bash
cd frontend
npm run dev
```

### **Code Style**
- Backend: Follow PEP 8
- Frontend: ESLint + Prettier

---

## 🎯 Future Enhancements

- [ ] Task sharing between users
- [ ] Email notifications
- [ ] Task attachments
- [ ] Recurring tasks
- [ ] Task comments
- [ ] Mobile app (React Native)
- [ ] AI-powered task suggestions

---

## 📄 License

This project is for educational purposes.

---

## 👨‍💻 Author

Built with ❤️ for the Hackathon

---

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- Next.js team for the excellent frontend framework
- Neon for cloud PostgreSQL hosting
- Vercel for frontend hosting

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the Urdu/Hindi guide: `README-URDU.md`
3. Check terminal error messages
4. Verify environment variables

---

**Happy Coding! 🚀**
