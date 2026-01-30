# Quick Selector Reference - Exact Elements

## ⚡ Quick Copy-Paste Selectors

### 0. Close Button (Optional - Popup/Modal)
```python
# Close popup if it appears (won't fail if not present)
try:
    close_btn = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
    )
    close_btn.click()
    print("✓ Popup closed")
except TimeoutException:
    print("No popup (OK)")
```

**HTML:**
```html
<button class="absolute top-4 right-4..." aria-label="Close">
  <svg class="w-5 h-5 text-white"><!-- X icon --></svg>
</button>
```

**When to use:** Call this after page loads or after login if popups appear.

---

### 1. Login Button (Red/Maroon - Opens Login Form)
```python
# Click to show login form
login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'લૉગિન કરો')]")
login_btn.click()
```

**HTML:**
```html
<button type="button" class="font-extrabold text-[#B30C1D] hover:text-[#A10A19]...">
  લૉગિન કરો
</button>
```

---

### 2. Mobile Number Input (⚠️ name="username" NOT "mobile"!)
```python
# Enter mobile number
mobile_input = driver.find_element(By.NAME, "username")
mobile_input.clear()
mobile_input.send_keys("9876543210")
```

**HTML:**
```html
<input name="username" 
       type="text" 
       placeholder="મોબાઇલ નંબર" 
       maxlength="10">
```

---

### 3. Password Input
```python
# Enter password
password_input = driver.find_element(By.NAME, "password")
password_input.clear()
password_input.send_keys("your_password")
```

**HTML:**
```html
<input name="password" 
       type="password" 
       placeholder="પાસવર્ડ">
```

---

### 4. Submit Login Button (Orange - Submits Form)
```python
# Click submit
submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_btn.click()
```

**HTML:**
```html
<button type="submit" class="bg-[#efa029]...">
  <span>લૉગિન કરો</span>
  <svg>...</svg>
</button>
```

---

### 5. User Avatar (Opens Profile Menu)
```python
# Click avatar to open menu
avatar = driver.find_element(By.CSS_SELECTOR, "div.MuiAvatar-root.MuiAvatar-circular")
avatar.click()
```

**HTML:**
```html
<div class="MuiAvatar-root MuiAvatar-circular MuiAvatar-colorDefault css-1ahp8i2">
  R
</div>
```

---

### 6. Logout Menu Item (Material-UI MenuItem)
```python
# Click logout from menu
logout_item = driver.find_element(By.XPATH, "//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]")
logout_item.click()
```

**HTML:**
```html
<li class="MuiMenuItem-root..." role="menuitem">
  <svg><!-- Exit icon --></svg>
  લૉગઆઉટ
</li>
```

---

## 🎯 Complete Working Code (Copy-Paste Ready)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
qr_url = "https://jeeto16cr.com/q/R6RcHQ"

try:
    # Step 1: Navigate to QR URL
    driver.get(qr_url)
    time.sleep(3)
    print(f"Redirected to: {driver.current_url}")
    
    # Step 1.5: Close popup if present (optional)
    try:
        close_btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
        )
        close_btn.click()
        time.sleep(0.5)
        print("✓ Popup closed")
    except TimeoutException:
        print("No popup (OK)")
    
    # Step 2: Click "લૉગિન કરો" button (red/maroon)
    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'લૉગિન કરો')]"))
    )
    login_btn.click()
    time.sleep(2)
    print("✓ Login button clicked")
    
    # Step 3: Enter mobile number (name="username")
    mobile_input = wait.until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    mobile_input.clear()
    mobile_input.send_keys("9876543210")
    print("✓ Mobile entered")
    
    # Step 4: Enter password
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("your_password")
    print("✓ Password entered")
    
    # Step 5: Click submit (orange button)
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    time.sleep(3)
    print("✓ Login submitted")
    
    # Step 5.5: Close popup after login if present (optional)
    try:
        close_btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
        )
        close_btn.click()
        time.sleep(0.5)
        print("✓ Post-login popup closed")
    except TimeoutException:
        print("No post-login popup (OK)")
    
    # Step 6: Click avatar to open profile menu
    avatar = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiAvatar-root.MuiAvatar-circular"))
    )
    avatar.click()
    time.sleep(1)
    print("✓ Menu opened")
    
    # Step 7: Click logout menu item
    logout_item = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]"))
    )
    logout_item.click()
    print("✓ Logged out")
    
    print("\n✓✓✓ AUTOMATION COMPLETE ✓✓✓")
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    time.sleep(2)
    driver.quit()
```

---

## 📋 Element Summary Table

| Element | Selector | Type | Key Attribute |
|---------|----------|------|---------------|
| **Close Button (Optional)** | `button[aria-label='Close']` | CSS | X icon, top-right |
| Login Button (Show Form) | `//button[contains(text(), 'લૉગિન કરો')]` | XPath | Red/Maroon button |
| Mobile Input | `input[name='username']` | CSS | ⚠️ name="username" |
| Password Input | `input[name='password']` | CSS | name="password" |
| Submit Button | `button[type='submit']` | CSS | Orange bg |
| **User Avatar** | `div.MuiAvatar-root.MuiAvatar-circular` | CSS | MUI circular avatar |
| **Logout Menu Item** | `//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]` | XPath | MUI MenuItem |

---

## ⚠️ Common Mistakes

### ❌ WRONG: Looking for name="mobile"
```python
mobile_input = driver.find_element(By.NAME, "mobile")  # Won't work!
```

### ✅ CORRECT: Use name="username"
```python
mobile_input = driver.find_element(By.NAME, "username")  # Works!
```

---

### ❌ WRONG: Using input[type='tel']
```python
mobile_input = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")  # Won't work!
```

### ✅ CORRECT: Use input[type='text']
```python
mobile_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'][maxlength='10']")  # Works!
```

---

## 🔄 Two "લૉગિન કરો" Buttons

**Button 1: Red/Maroon (type="button")** → Shows login form
```html
<button type="button" class="text-[#B30C1D]">લૉગિન કરો</button>
```

**Button 2: Orange (type="submit")** → Submits login
```html
<button type="submit" class="bg-[#efa029]">
  <span>લૉગિન કરો</span>
</button>
```

**How to distinguish:**
- Button 1: `type="button"`, red color `text-[#B30C1D]`
- Button 2: `type="submit"`, orange color `bg-[#efa029]`

---

**Created**: January 25, 2026  
**Purpose**: Quick reference for exact HTML selectors  
**Status**: Verified with actual page HTML
