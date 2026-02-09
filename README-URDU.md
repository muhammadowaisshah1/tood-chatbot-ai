# 🚀 Todo App - Local Setup Guide (اردو/हिंदी)

## 📋 Application Ko Kaise Chalayein

### ✅ **Sabse Aasan Tareeqa (Recommended)**

1. **`start-app.bat`** file par **double-click** karein
2. Automatically 2 terminal windows khulenge (Backend aur Frontend)
3. Browser automatically khul jayega
4. **Done!** Application chal rahi hai

---

## 🛑 **Application Ko Kaise Band Karein**

### **Option 1: Stop Script Use Karein**
- **`stop-app.bat`** file par double-click karein
- Dono servers automatically band ho jayenge

### **Option 2: Manual**
- Dono terminal windows mein `Ctrl+C` press karein
- Ya phir terminal windows ko close kar dein

---

## 🔧 **Manual Start Karne Ka Tareeqa**

Agar aap manually start karna chahte hain:

### **Step 1: Backend Start Karein**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### **Step 2: Frontend Start Karein** (Dusre terminal mein)
```bash
cd frontend
npm run dev
```

### **Step 3: Browser Mein Open Karein**
```
http://localhost:3000
```

---

## 🌐 **Important URLs**

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main Application |
| **Backend API** | http://localhost:8001 | API Server |
| **API Docs** | http://localhost:8001/docs | Swagger Documentation |
| **Health Check** | http://localhost:8001/health | Server Status |

---

## 📱 **Application Features**

✅ User Registration aur Login
✅ Tasks Create, Edit, Delete
✅ Task Categories (Work, Personal, Shopping, etc.)
✅ Priority Levels (High, Medium, Low)
✅ Due Dates
✅ Search Functionality
✅ Dark/Light Theme
✅ Mobile Responsive

---

## ⚙️ **System Requirements**

- **Python:** 3.14+ (Installed ✅)
- **Node.js:** 18.18+ (Installed ✅)
- **Database:** Neon PostgreSQL (Cloud - Already Connected ✅)
- **Internet:** Required (for database connection)

---

## 🐛 **Agar Koi Problem Aaye**

### **Problem 1: Port Already in Use**
**Error:** `Address already in use`

**Solution:**
```bash
# Stop script run karein
stop-app.bat
```

### **Problem 2: Backend Connect Nahi Ho Raha**
**Solution:**
1. Check karein ke backend terminal mein error to nahi
2. `.env` file check karein backend folder mein
3. Internet connection check karein (database cloud par hai)

### **Problem 3: Frontend Load Nahi Ho Raha**
**Solution:**
```bash
cd frontend
npm install
npm run dev
```

### **Problem 4: Database Connection Error**
**Solution:**
- Internet connection check karein
- `backend/.env` file mein `DATABASE_URL` check karein

---

## 📂 **Project Structure**

```
Hackthon_Full-Stack_App/
├── backend/              # FastAPI Backend
│   ├── app/             # Application code
│   ├── main.py          # Entry point
│   ├── .env             # Environment variables
│   └── requirements.txt # Python dependencies
│
├── frontend/            # Next.js Frontend
│   ├── app/            # Pages
│   ├── components/     # React components
│   ├── lib/            # Utilities
│   ├── .env.local      # Environment variables
│   └── package.json    # Node dependencies
│
├── start-app.bat       # ✨ Quick start script
├── stop-app.bat        # ✨ Stop servers script
└── README-URDU.md      # Ye file
```

---

## 💡 **Tips**

1. **Hamesha dono servers chalane hain** (Backend + Frontend)
2. **Backend pehle start karein**, phir Frontend
3. **Internet connection zaroori hai** (database ke liye)
4. **Ctrl+C se servers band kar sakte hain**
5. **Browser cache clear karein** agar changes nahi dikh rahe

---

## 🎯 **Quick Commands**

| Action | Command |
|--------|---------|
| Start Everything | Double-click `start-app.bat` |
| Stop Everything | Double-click `stop-app.bat` |
| Backend Only | `cd backend && python -m uvicorn main:app --reload` |
| Frontend Only | `cd frontend && npm run dev` |
| Install Backend Deps | `cd backend && pip install -r requirements.txt` |
| Install Frontend Deps | `cd frontend && npm install` |

---

## 📞 **Support**

Agar koi problem aaye to:
1. Terminal mein error message dekhen
2. Browser console check karein (F12 press karein)
3. Dono servers restart karein

---

## ✅ **Checklist - Pehli Baar Setup**

- [x] Python installed hai
- [x] Node.js installed hai
- [x] Backend dependencies installed hain
- [x] Frontend dependencies installed hain
- [x] Database connected hai
- [x] `.env` files configured hain
- [x] Application successfully chal rahi hai

---

## 🎉 **Congratulations!**

Aapka Full-Stack Todo Application successfully setup ho gaya hai!

**Enjoy coding! 🚀**
