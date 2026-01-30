# Quiz Automation - Element Locators Guide

## Overview
This document contains all the important HTML elements and selectors needed for automating the login/logout workflow on the Jeeto16Cr website.

---

## Page Structure Analysis

### Base Structure
- **App Root**: `<div id="root"></div>`
- **Dynamic Content**: React-based SPA (Single Page Application)
- **JavaScript Bundle**: `/assets/index-DJwYBETd.js`
- **Stylesheet**: `/assets/index-BhPXfkIh.css`

---

### OPTIONAL: Close Button (Popup/Modal)

**Element Details:**
```html
<button class="absolute top-4 right-4 w-8 h-8 hover:bg-white/20 rounded-full flex items-center justify-center transition-all duration-200 transform hover:scale-110 active:scale-95 z-10" 
        aria-label="Close">
  <svg class="w-5 h-5 text-white" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewBox="0 0 24 24" stroke="currentColor">
    <path d="M6 18L18 6M6 6l12 12"></path>
  </svg>
</button>
```

**When it appears:**
- May appear after QR redirect (popup/modal)
- May appear after login
- **Not always present** - automation should continue if not found

**Selector Options:**
- **By Aria Label**: `button[aria-label="Close"]` ⭐ BEST
- **By Position Class**: `button.absolute.top-4.right-4`
- **XPath**: `//button[@aria-label='Close']`

**Recommended Implementation:**
```python
def close_popup_if_present(driver):
    """Close popup if present, don't fail if not found"""
    try:
        wait = WebDriverWait(driver, 2)  # Short wait since optional
        close_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
        )
        close_btn.click()
        print("✓ Popup closed")
        return True
    except TimeoutException:
        print("No popup found (OK)")
        return False
```

**Visual Properties:**
- Position: Absolute, top-right corner (`top-4 right-4`)
- Shape: Rounded circle (`rounded-full`)
- Icon: X (close) icon
- Size: 8x8 units
- Color: White icon with hover effect

---

### 1. LOGIN BUTTON (Initial Page)

**Element Details:**
```html
<button type="button" class="font-extrabold text-[#B30C1D] hover:text-[#A10A19] transition-colors hover:underline">
  લૉગિન કરો
</button>
```

**Selector Options:**
- **By Text (Gujarati)**: `લૉગિન કરો`
- **By CSS Class**: `.font-extrabold.text-\[\#B30C1D\]`
- **By Button Type**: `button[type="button"]` (with text match)
- **XPath**: `//button[contains(text(), 'લૉગિન કરો')]`

**Recommended Selector for Selenium:**
```python
# Using XPath with text
login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'લૉગિન કરો')]")

# Alternative - Using CSS Selector with partial class
login_button = driver.find_element(By.CSS_SELECTOR, "button.font-extrabold")
```

**Visual Properties:**
- Text Color: `#B30C1D` (Red)
- Hover Color: `#A10A19` (Darker Red)
- Font Weight: Extra Bold
- Has underline on hover
- Transition effects on color change

---

### 2. LOGIN FORM FIELDS

#### Mobile Number Input Field

**Actual Element Structure:**
```html
<input class="w-full pl-3 pr-4 py-3 bg-gradient-to-r from-[#F5C10E]/10 to-[#F7D64E]/10 rounded-lg text-gray-900 placeholder-gray-600 focus:ring-1 focus:ring-black focus:border-[#F5C10E] transition-all duration-200 outline-none font-medium" 
       placeholder="મોબાઇલ નંબર" 
       maxlength="10" 
       type="text" 
       value="" 
       name="username">
```

**Important**: The field name is `username`, NOT `mobile`!

**Selector Options:**
- **By Name**: `input[name="username"]` ⭐ BEST
- **By Placeholder**: `input[placeholder="મોબાઇલ નંબર"]`
- **By Type + Maxlength**: `input[type="text"][maxlength="10"]`
- **XPath**: `//input[@name='username']`

**Recommended Selector:**
```python
mobile_input = driver.find_element(By.NAME, "username")
# OR
mobile_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
```

**Field Requirements:**
- Type: Text input (not tel!)
- Name: username
- Max Length: 10 digits
- Expected Format: Indian mobile number (10 digits)

---

#### Password Input Field

**Actual Element Structure:**
```html
<input class="w-full pl-3 pr-12 py-3 bg-gradient-to-r from-[#F5C10E]/10 to-[#F7D64E]/10 rounded-lg text-gray-900 placeholder-gray-600 focus:ring-1 focus:ring-black focus:border-[#F5C10E] transition-all duration-200 outline-none font-medium" 
       placeholder="પાસવર્ડ" 
       type="password" 
       value="" 
       name="password">
```

**Selector Options:**
- **By Name**: `input[name="password"]` ⭐ BEST
- **By Type**: `input[type="password"]`
- **By Placeholder**: `input[placeholder="પાસવર્ડ"]`
- **XPath**: `//input[@name='password']`

**Recommended Selector:**
```python
password_input = driver.find_element(By.NAME, "password")
# OR
password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
```

---

#### Login Submit Button

**Actual Element Structure:**
```html
<button type="submit" 
        class="w-full bg-[#efa029] text-white py-3 rounded-lg font-extrabold text-lg transition-all duration-300 transform hover:scale-[1.02] shadow-lg hover:shadow-xl flex items-center justify-center gap-2 group disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none cursor-pointer">
  <span>લૉગિન કરો</span>
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right group-hover:translate-x-1 transition-transform" aria-hidden="true">
    <path d="M5 12h14"></path>
    <path d="m12 5 7 7-7 7"></path>
  </svg>
</button>
```

**Visual Properties:**
- Background Color: `#efa029` (Orange)
- Full width button
- Contains text: "લૉગિન કરો"
- Has arrow icon on the right

**Selector Options:**
- **By Type**: `button[type="submit"]` ⭐ BEST
- **By Background Color**: `button.bg-[#efa029]`
- **By Text Content**: `//button[contains(., 'લૉગિન કરો')]`
- **XPath**: `//button[@type='submit']`

**Recommended Selector:**
```python
submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
# OR
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
```

---

### 3. LOGOUT BUTTON (Side Menu)

**Expected Location**: User Profile Menu (Material-UI Menu)

#### Step 1: Click Avatar to Open Menu

**Actual Element Structure:**
```html
<div class="MuiAvatar-root MuiAvatar-circular MuiAvatar-colorDefault css-1ahp8i2">
  R
</div>
```

**Description:**
- Material-UI Avatar component (circular profile icon)
- Contains user's initial (e.g., "R")
- Usually located in top-right corner of page

**Selector Options:**
- **By MUI Classes**: `div.MuiAvatar-root.MuiAvatar-circular` ⭐ BEST
- **By Single Class**: `.MuiAvatar-root`
- **XPath**: `//div[contains(@class, 'MuiAvatar-root')]`

**Recommended Selector:**
```python
# Click avatar to open menu
avatar = driver.find_element(By.CSS_SELECTOR, "div.MuiAvatar-root.MuiAvatar-circular")
avatar.click()
```

---

#### Step 2: Click Logout Menu Item

**Actual Element Structure:**
```html
<li class="MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-utm0jj" 
    tabindex="-1" 
    role="menuitem">
  <svg class="MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-y2kftd" focusable="false" aria-hidden="true" viewBox="0 0 24 24">
    <path d="m17 7-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4z"></path>
  </svg>
  લૉગઆઉટ
  <span class="MuiTouchRipple-root css-4mb1j7"></span>
</li>
```

**Description:**
- Material-UI MenuItem component
- Contains logout icon (arrow + door SVG)
- Contains Gujarati text "લૉગઆઉટ"
- Has role="menuitem"

**Selector Options:**
- **By Role + Text**: `//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]` ⭐ BEST
- **By MUI Classes + Text**: `//li[contains(@class, 'MuiMenuItem-root') and contains(., 'લૉગઆઉટ')]`
- **By Text Only**: `//li[contains(text(), 'લૉગઆઉટ')]`
- **XPath Generic**: `//*[contains(text(), 'લૉગઆઉટ')]`

**Recommended Selector:**
```python
# Click logout menu item
logout_item = driver.find_element(By.XPATH, "//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]")
logout_item.click()
```

**Complete Logout Flow:**
```python
# Step 1: Click avatar to open menu
avatar = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiAvatar-root.MuiAvatar-circular"))
)
avatar.click()
time.sleep(1)  # Wait for menu to appear

# Step 2: Click logout menu item
logout_item = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]"))
)
logout_item.click()
```

**Additional Notes:**
- Menu appears as dropdown when avatar is clicked
- Material-UI uses CSS animations for menu appearance
- Wait 1-1.5 seconds after clicking avatar for menu to fully appear
- Logout icon is an exit/door icon with arrow

---

## Side Menu / Navigation Drawer

### ⚠️ Update: No Side Menu - Uses Profile Avatar Menu Instead

---

## Complete Automation Flow

### Understanding QR URL Redirects

**Important**: The QR URL (`https://jeeto16cr.com/q/R6RcHQ`) automatically redirects to the auth/register page with QR parameters preserved:

```
Original: https://jeeto16cr.com/q/R6RcHQ
Redirects to: https://jeeto16cr.com/auth/register?qr=1768044780551_2&language=g&mode=online&groupType=db
```

**Key Parameters Preserved**:
- `qr` - The QR identifier (e.g., `1768044780551_2`)
- `language` - Language preference (e.g., `g` for Gujarati)
- `mode` - Quiz mode (e.g., `online`)
- `groupType` - Group type (e.g., `db`)

**Automation Strategy**:
1. Navigate directly to the QR URL
2. Let it redirect to auth page with parameters
3. **IMPORTANT**: Click "લૉગિન કરો" button to show login form (even on auth page)
4. Enter credentials and login
5. After login, the QR parameters are automatically processed

### Step-by-Step Selenium Code Structure

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # QR URL - will redirect to auth page with parameters
    qr_url = "https://jeeto16cr.com/q/R6RcHQ"
    
    # Navigate directly to QR URL
    print("Navigating to QR URL (will redirect to auth page)...")
    driver.get(qr_url)
    time.sleep(3)  # Wait for redirect
    
    print(f"Redirected to: {driver.current_url}")
    
    # STEP 1: Click "લૉગિન કરો" button (required even on auth page)
    print("Step 1: Clicking 'લૉગિન કરો' button to show login form...")
    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'લૉગિન કરો')]"))
    )
    login_btn.click()
    time.sleep(2)  # Wait for login form to appear
    
    # STEP 2: Enter Mobile Number (name="username" NOT "mobile"!)
    print("Step 2: Entering mobile number...")
    mobile_input = wait.until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    mobile_input.clear()
    mobile_input.send_keys("9876543210")  # Replace with actual mobile
    
    # STEP 3: Enter Password
    print("Step 3: Entering password...")
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("your_password")  # Replace with actual password
    
    # STEP 4: Click Submit/Login
    print("Step 4: Submitting login form...")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    time.sleep(3)  # Wait for login to complete
    
    # After login, QR parameters are automatically processed
    print(f"Post-login URL: {driver.current_url}")
    time.sleep(2)
    
    # STEP 5: Click avatar to open profile menu
    print("Step 5: Opening profile menu...")
    avatar = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiAvatar-root.MuiAvatar-circular"))
    )
    avatar.click()
    time.sleep(1)  # Wait for menu to appear
    
    # STEP 6: Click Logout menu item
    print("Step 6: Clicking logout...")
    logout_item = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]"))
    )
    logout_item.click()
    
    print("Automation completed successfully!")
    
except Exception as e:
    print(f"Error occurred: {e}")
    
finally:
    time.sleep(2)
    driver.quit()
```

---

## Important Wait Strategies

### Explicit Waits (Recommended)
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)

# Wait for element to be clickable
element = wait.until(EC.element_to_be_clickable((By.XPATH, "xpath")))

# Wait for element to be visible
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "selector")))

# Wait for element to be present in DOM
element = wait.until(EC.presence_of_element_located((By.NAME, "name")))
```

### Implicit Wait
```python
driver.implicitly_wait(10)  # Set once at the beginning
```

---

## Troubleshooting Tips

### Issue: Element Not Found
**Solutions:**
1. Add explicit waits before interacting with elements
2. Check if page is fully loaded (`WebDriverWait`)
3. Verify selector using browser DevTools
4. Check if element is inside iframe
5. Wait for React app to render (`time.sleep(2)` after page load)

### Issue: Element Not Clickable
**Solutions:**
1. Use `EC.element_to_be_clickable()` wait condition
2. Scroll element into view: `driver.execute_script("arguments[0].scrollIntoView();", element)`
3. Wait for overlay/modal to close
4. Use JavaScript click: `driver.execute_script("arguments[0].click();", element)`

### Issue: StaleElementReferenceException
**Solutions:**
1. Re-locate element after DOM updates
2. Use fresh selectors instead of storing elements
3. Add waits between actions

---

## Testing Checklist

- [ ] Login button is clickable
- [ ] Mobile input accepts 10 digits
- [ ] Password input masks characters
- [ ] Submit button triggers login
- [ ] Wait for successful login (check URL or element)
- [ ] Menu toggle opens side menu
- [ ] Logout button is visible in menu
- [ ] Logout button triggers logout
- [ ] Redirect to home/login page after logout

---

## Notes

1. **Language**: Website uses Gujarati text - ensure proper Unicode support
2. **Dynamic Content**: React SPA - elements load asynchronously
3. **Wait Times**: Add appropriate waits for animations and API calls
4. **Error Handling**: Implement try-catch blocks for robustness
5. **Screenshots**: Capture screenshots on failure for debugging

---

## Additional Selectors to Investigate (If Above Don't Work)

### Alternative Login Button Selectors
```python
# Try multiple strategies
selectors = [
    (By.XPATH, "//button[contains(text(), 'લૉગિન કરો')]"),
    (By.CSS_SELECTOR, "button.font-extrabold"),
    (By.XPATH, "//button[contains(@class, 'text-[#B30C1D]')]"),
    (By.XPATH, "//button[contains(@class, 'hover:underline')]")
]
```

### Alternative Logout Button Selectors
```python
selectors = [
    (By.XPATH, "//button[contains(text(), 'લૉગઆઉટ')]"),
    (By.XPATH, "//a[contains(text(), 'લૉગઆઉટ')]"),
    (By.CSS_SELECTOR, "nav button:last-child"),
    (By.XPATH, "//div[@role='menu']//button[contains(text(), 'લૉગઆઉટ')]")
]
```

---

## API Response Format

### Expected Response Structure

When processing multiple users through the API, the response should include results for all users:

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
      "error": "Timeout waiting for .success"
    }
  ]
}
```

### Response Fields

#### Root Level
- **qr_url** (string): The QR URL that was processed
- **results** (array): Array of result objects for each user

#### Result Object
- **mobile** (string): User's mobile number
- **status** (string): Either "success" or "error"
- **error** (string, optional): Error message if status is "error"

### Sample Implementation

```python
def run_for_user(user, qr_url):
    """
    Process automation for a single user
    Returns: dict with mobile, status, and optional error
    """
    mobile = user.get("mobile")
    password = user.get("password")
    
    try:
        # Your automation code here
        driver = webdriver.Chrome()
        driver.get(qr_url)
        
        # Login process
        # ... (your automation steps)
        
        # If successful
        return {
            "mobile": mobile,
            "status": "success"
        }
        
    except TimeoutException as e:
        return {
            "mobile": mobile,
            "status": "error",
            "error": f"Timeout waiting for {str(e)}"
        }
        
    except Exception as e:
        return {
            "mobile": mobile,
            "status": "error",
            "error": str(e)
        }
        
    finally:
        driver.quit()
```

### API Endpoint Example

```python
@app.post("/process-qr")
def process_qr(payload: dict):
    qr_url = payload.get("qr_url")
    
    if not qr_url:
        return {"error": "qr_url missing"}
    
    with open("users.json") as f:
        users = json.load(f)
    
    results = []
    
    for user in users:
        result = run_for_user(user, qr_url)
        results.append(result)
    
    return {
        "qr_url": qr_url,
        "results": results
    }
```

### Error Handling Best Practices

1. **Always return mobile number** - For tracking which user had issues
2. **Specific error messages** - Include element selectors or timeout info
3. **Continue on error** - Don't stop processing other users if one fails
4. **Log errors** - Keep detailed logs for debugging

### Common Error Messages

- `"Timeout waiting for .success"` - Element not found within timeout period
- `"Login failed"` - Invalid credentials or login button not found
- `"Side menu not opened"` - Menu toggle didn't work
- `"Logout button not found"` - Logout element not located in menu
- `"Network error"` - Connection issues or page didn't load

---

**Document Created**: January 22, 2026  
**Document Updated**: January 23, 2026  
**Version**: 1.1  
**Project**: Quiz Automation - Jeeto16Cr
