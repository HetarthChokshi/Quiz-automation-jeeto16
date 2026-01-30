# 🚀 Quick Start Guide

## Step-by-Step Setup

### 1️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- `fastapi` - Web API framework
- `uvicorn` - ASGI server
- `selenium` - Browser automation
- `webdriver-manager` - Automatic ChromeDriver management
- `pydantic` - Data validation

### 2️⃣ Configure Users

Edit `users.json` with your credentials:

```json
[
  {
    "mobile": "9999999999",
    "password": "your_password_here"
  }
]
```

Add as many users as needed!

### 3️⃣ Test Your Setup

```powershell
python test_setup.py
```

This will verify:
- ✅ All packages are installed
- ✅ Chrome browser is working
- ✅ users.json is valid
- ✅ All files are present

### 4️⃣ Start the API Server

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5️⃣ Test the API

Open browser and go to: **http://localhost:8000/docs**

Or test with PowerShell:

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get

# Process QR URL
$body = @{
    qr_url = "https://jeeto16cr.com/q/R6RcHQ"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/process-qr" -Method Post -Body $body -ContentType "application/json"
```

## 📋 Common Commands

### Start Server
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Test Single User
```powershell
python automate.py
```

### View Logs (Verbose)
```powershell
uvicorn main:app --reload --log-level debug
```

### Run in Background (Windows)
```powershell
Start-Process powershell -ArgumentList "uvicorn main:app --host 0.0.0.0 --port 8000" -WindowStyle Hidden
```

## 🔧 Configuration Options

### Change Port
```powershell
uvicorn main:app --reload --port 9000
```

### Run Headless (No Browser Window)

Edit `automate.py`, line ~350:
```python
driver = setup_driver(headless=True)  # Change to True
```

### Update Website URL

Edit `automate.py`, line ~357:
```python
driver.get("https://your-website-url.com")  # Change URL here
```

## 🐛 Troubleshooting

### "Module not found" Error
```powershell
pip install -r requirements.txt --upgrade
```

### Chrome/ChromeDriver Issues
```powershell
pip install webdriver-manager --upgrade
```

### Port Already in Use
```powershell
# Use different port
uvicorn main:app --reload --port 8001
```

### users.json Not Found
```powershell
# Run test setup to create it
python test_setup.py
```

## 📖 Documentation

- **README.md** - Full documentation
- **AUTOMATION_ELEMENTS_GUIDE.md** - Element selectors and technical details
- **http://localhost:8000/docs** - Interactive API documentation (when server is running)

## 🎯 Next Steps

1. ✅ Update `users.json` with real credentials
2. ✅ Update website URL in `automate.py` if needed
3. ✅ Test with a single user first
4. ✅ Run batch processing for all users

## 💡 Tips

- Keep browser window visible first time to see what's happening
- Check console logs for detailed error messages
- Use `/users` endpoint to verify users are loaded correctly
- Test with one user before running for all users

---

**Need Help?** Check `AUTOMATION_ELEMENTS_GUIDE.md` for detailed technical documentation.
