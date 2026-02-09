# 🔧 Troubleshooting Guide - Todo App

## 🚨 Common Problems & Solutions

---

### ❌ Problem 1: "Port 8001 is already in use"

**Error Message:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8001)
```

**Solution:**
```bash
# Option 1: Use stop script
stop-app.bat

# Option 2: Manual kill
netstat -ano | findstr :8001
taskkill /F /PID <PID_NUMBER>
```

---

### ❌ Problem 2: "Port 3000 is already in use"

**Error Message:**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution:**
```bash
# Option 1: Use stop script
stop-app.bat

# Option 2: Manual kill
netstat -ano | findstr :3000
taskkill /F /PID <PID_NUMBER>
```

---

### ❌ Problem 3: "DATABASE_URL environment variable is not set"

**Error Message:**
```
ValueError: DATABASE_URL environment variable is not set
```

**Solution:**
1. Check `backend/.env` file exists
2. Verify it contains:
```bash
DATABASE_URL=postgresql+psycopg://neondb_owner:npg_...@ep-bold-surf...
```
3. Restart backend server

---

### ❌ Problem 4: "Could not connect to database"

**Error Message:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
1. ✅ Check internet connection
2. ✅ Verify DATABASE_URL is correct in `backend/.env`
3. ✅ Test database connection:
```bash
curl https://ep-bold-surf-ah3dx6q5-pooler.c-3.us-east-1.aws.neon.tech
```

---

### ❌ Problem 5: "Module not found" (Backend)

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

---

### ❌ Problem 6: "Module not found" (Frontend)

**Error Message:**
```
Error: Cannot find module 'next'
```

**Solution:**
```bash
cd frontend
npm install
```

---

### ❌ Problem 7: "Failed to fetch" in Browser

**Error in Browser Console:**
```
Failed to fetch
TypeError: NetworkError when attempting to fetch resource
```

**Solution:**
1. ✅ Check backend is running: http://localhost:8001/health
2. ✅ Verify `frontend/.env.local` has:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```
3. ✅ Restart frontend:
```bash
cd frontend
npm run dev
```

---

### ❌ Problem 8: "401 Unauthorized" Error

**Error Message:**
```
{"detail": "Could not validate credentials"}
```

**Solution:**
1. Clear browser localStorage:
   - Press F12 → Application → Local Storage → Clear
2. Login again
3. Check JWT token is being sent in requests

---

### ❌ Problem 9: "CORS Error" in Browser

**Error in Browser Console:**
```
Access to fetch at 'http://localhost:8001' has been blocked by CORS policy
```

**Solution:**
1. Check `backend/.env` has:
```bash
CORS_ORIGINS=http://localhost:3000
```
2. Restart backend server
3. Clear browser cache (Ctrl+Shift+Delete)

---

### ❌ Problem 10: Frontend Shows Blank Page

**Solution:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Clear browser cache:
```
Ctrl+Shift+Delete → Clear cached images and files
```
4. Hard refresh: `Ctrl+Shift+R`
5. Restart frontend server

---

### ❌ Problem 11: "Python not found"

**Error Message:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
```bash
# Try python3 instead
python3 -m uvicorn main:app --reload --port 8001

# Or use full path
C:\Python314\python.exe -m uvicorn main:app --reload --port 8001
```

---

### ❌ Problem 12: "npm not found"

**Error Message:**
```
'npm' is not recognized as an internal or external command
```

**Solution:**
1. Install Node.js from: https://nodejs.org/
2. Restart terminal
3. Verify installation:
```bash
node --version
npm --version
```

---

### ❌ Problem 13: Slow Database Queries

**Symptoms:**
- API responses taking 5+ seconds
- Tasks loading slowly

**Solution:**
1. Check internet speed
2. Database is on cloud (Neon) - requires good internet
3. Consider upgrading Neon plan for better performance

---

### ❌ Problem 14: "Invalid Token" After Some Time

**Error Message:**
```
{"detail": "Invalid token payload"}
```

**Solution:**
- JWT tokens expire after 7 days
- Simply login again
- Token will be refreshed automatically

---

### ❌ Problem 15: Changes Not Reflecting

**Solution:**

**Backend Changes:**
```bash
# Backend has auto-reload enabled
# Just save the file, it will reload automatically
```

**Frontend Changes:**
```bash
# Clear Next.js cache
cd frontend
rm -rf .next
npm run dev
```

**Browser:**
```
Hard refresh: Ctrl+Shift+R
Or clear cache: Ctrl+Shift+Delete
```

---

## 🔍 Debugging Tips

### **Check Backend Status**
```bash
curl http://localhost:8001/health
# Should return: {"status":"healthy"}
```

### **Check Frontend Status**
```bash
curl http://localhost:3000
# Should return: HTML content
```

### **View Backend Logs**
- Check the terminal where backend is running
- Look for error messages in red

### **View Frontend Logs**
- Check the terminal where frontend is running
- Open browser console (F12) for client-side errors

### **Check Database Connection**
```bash
cd backend
python -c "from app.database import engine; print('Database connected!')"
```

---

## 📊 Health Check Checklist

Run these commands to verify everything is working:

```bash
# 1. Backend health
curl http://localhost:8001/health

# 2. Frontend health
curl -I http://localhost:3000

# 3. API documentation
start http://localhost:8001/docs

# 4. Check ports
netstat -ano | findstr :8001
netstat -ano | findstr :3000
```

---

## 🆘 Emergency Reset

If nothing works, try complete reset:

```bash
# 1. Stop all servers
stop-app.bat

# 2. Clear caches
cd frontend
rm -rf .next node_modules
npm install

cd ../backend
rm -rf __pycache__ app/__pycache__

# 3. Restart
start-app.bat
```

---

## 📞 Getting Help

### **Step 1: Check Error Message**
- Read the complete error message
- Note the file and line number

### **Step 2: Check Logs**
- Backend terminal for API errors
- Frontend terminal for build errors
- Browser console (F12) for client errors

### **Step 3: Verify Configuration**
- `backend/.env` - All variables set?
- `frontend/.env.local` - API URL correct?

### **Step 4: Test Components**
- Backend: `curl http://localhost:8001/health`
- Frontend: `curl http://localhost:3000`
- Database: Check internet connection

---

## 🎯 Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Port in use | `stop-app.bat` |
| Module not found | `pip install -r requirements.txt` or `npm install` |
| Database error | Check internet + DATABASE_URL |
| CORS error | Check CORS_ORIGINS in backend/.env |
| 401 error | Clear localStorage + login again |
| Blank page | Clear cache + hard refresh |
| Slow loading | Check internet speed |
| Changes not showing | Hard refresh (Ctrl+Shift+R) |

---

## ✅ Prevention Tips

1. **Always use stop script** before closing terminals
2. **Don't modify .env files** unless necessary
3. **Keep internet connected** (database is cloud-based)
4. **Update dependencies regularly**
5. **Clear cache** if things look weird
6. **Use start script** for consistent startup

---

**Still having issues?** Check the main README.md or README-URDU.md for more details.
