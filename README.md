# Quiz Automation System

Automated login/logout system for Jeeto16Cr quiz platform with multi-user support.

## 🚀 Features

- ✅ Automated login with mobile number and password
- ✅ QR URL processing for multiple users
- ✅ Automated logout from side menu
- ✅ Multi-user batch processing
- ✅ Detailed error handling and logging
- ✅ RESTful API with FastAPI
- ✅ Individual result tracking for each user

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

## 🔧 Installation

1. **Clone or download the project**

2. **Install Python dependencies**

```powershell
pip install -r requirements.txt
```

3. **Configure users**

Edit `users.json` with your user credentials:

```json
[
  {
    "mobile": "9999999999",
    "password": "your_password"
  },
  {
    "mobile": "8888888888",
    "password": "another_password"
  }
]
```

## 🎮 Usage

### Method 1: Run API Server

Start the FastAPI server:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

### Method 2: Direct Python Execution

Test automation for a single user:

```powershell
python automate.py
```

## 📡 API Endpoints

### 1. Health Check

```http
GET /
```

**Response:**
```json
{
  "status": "running",
  "message": "Quiz Automation API is running"
}
```

### 2. Get Users List

```http
GET /users
```

**Response:**
```json
{
  "total_users": 2,
  "users": [
    { "mobile": "9999999999" },
    { "mobile": "8888888888" }
  ]
}
```

### 3. Process QR URL

```http
POST /process-qr
Content-Type: application/json

{
  "qr_url": "https://jeeto16cr.com/q/R6RcHQ"
}
```

**Response:**
```json
{
  "qr_url": "https://jeeto16cr.com/q/R6RcHQ",
  "results": [
    {
      "mobile": "9999999999",
      "status": "success"
    },
    {
      "mobile": "8888888888",
      "status": "error",
      "error": "Timeout waiting for login button"
    }
  ],
  "total_users": 2,
  "successful": 1,
  "failed": 1
}
```

## 🧪 Testing with cURL

### Windows PowerShell:

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get

# Get users
Invoke-RestMethod -Uri "http://localhost:8000/users" -Method Get

# Process QR
$body = @{
    qr_url = "https://jeeto16cr.com/q/R6RcHQ"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/process-qr" -Method Post -Body $body -ContentType "application/json"
```

### Using cURL:

```bash
# Health check
curl http://localhost:8000/

# Get users
curl http://localhost:8000/users

# Process QR
curl -X POST "http://localhost:8000/process-qr" \
  -H "Content-Type: application/json" \
  -d '{"qr_url": "https://jeeto16cr.com/q/R6RcHQ"}'
```

## 📁 Project Structure

```
Quiz automation/
├── main.py                      # FastAPI server
├── automate.py                  # Selenium automation logic
├── users.json                   # User credentials
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── AUTOMATION_ELEMENTS_GUIDE.md # Detailed element locators guide
├── save_html.py                 # HTML page saver utility
└── website-page-*.html          # Saved HTML pages
```

## 🔍 How It Works

### Automation Flow

1. **Click Login Button** - Locates and clicks the login button on homepage
2. **Enter Mobile Number** - Inputs user's mobile number (10 digits)
3. **Enter Password** - Inputs user's password
4. **Submit Login** - Clicks submit button to log in
5. **Verify Login** - Checks if login was successful
6. **Process QR URL** - Navigates to the provided QR URL
7. **Open Side Menu** - Clicks menu toggle to open navigation drawer
8. **Click Logout** - Finds and clicks logout button in side menu

### Element Selectors

The automation uses multiple fallback selectors for reliability:

- **Login Button:** `//button[contains(text(), 'લૉગિન કરો')]`
- **Mobile Input:** `input[type='tel']` or `input[name='mobile']`
- **Password Input:** `input[type='password']` or `input[name='password']`
- **Submit Button:** `button[type='submit']`
- **Menu Toggle:** `button[aria-label='menu']`
- **Logout Button:** `//button[contains(text(), 'લૉગઆઉટ')]`

See `AUTOMATION_ELEMENTS_GUIDE.md` for complete selector documentation.

## ⚙️ Configuration

### Headless Mode

To run browser in headless mode (no GUI), edit `automate.py`:

```python
driver = setup_driver(headless=True)  # Change False to True
```

### Timeout Settings

Default timeout is 15 seconds. To adjust, modify in `automate.py`:

```python
wait = WebDriverWait(driver, 15)  # Change 15 to desired seconds
```

### Website URL

Update the base URL in `automate.py`:

```python
driver.get("https://jeeto16cr.com")  # Change to actual URL
```

## 🐛 Troubleshooting

### Chrome Driver Issues

If Chrome driver fails, install manually:

```powershell
pip install webdriver-manager
```

### Element Not Found Errors

1. Check if website structure has changed
2. Use browser DevTools to inspect elements
3. Update selectors in `automate.py`
4. Increase timeout values

### Login Failures

1. Verify credentials in `users.json`
2. Check if CAPTCHA is required
3. Ensure stable internet connection
4. Review logs for specific error messages

### Module Import Errors

Reinstall dependencies:

```powershell
pip install -r requirements.txt --upgrade
```

## 📊 Logging

Logs are printed to console with timestamps:

```
2026-01-23 10:30:45 - INFO - Starting automation for user: 9999999999
2026-01-23 10:30:47 - INFO - ✓ Login button clicked successfully
2026-01-23 10:30:49 - INFO - ✓ Mobile number entered
2026-01-23 10:30:50 - INFO - ✓ Password entered
2026-01-23 10:30:51 - INFO - ✓ Login form submitted
2026-01-23 10:30:54 - INFO - ✓ Login successful
2026-01-23 10:30:57 - INFO - ✓ Side menu opened
2026-01-23 10:30:59 - INFO - ✓ Logout button clicked
2026-01-23 10:31:01 - INFO - ✓✓✓ Automation completed successfully for 9999999999
```

## 🔒 Security Notes

- **Never commit `users.json` with real credentials to version control**
- Add `users.json` to `.gitignore`
- Use environment variables for production
- Keep API server on private network

## 📝 License

This project is for educational and automation purposes only.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

For detailed element locators and technical documentation, see:
- `AUTOMATION_ELEMENTS_GUIDE.md` - Complete element selector guide

---

**Last Updated:** January 23, 2026  
**Version:** 1.0.0
