# Correct Automation Flow - Visual Guide

## Complete Step-by-Step Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Navigate to QR URL                                      │
│ URL: https://jeeto16cr.com/q/R6RcHQ                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Automatic Redirect                                              │
│ TO: https://jeeto16cr.com/auth/register?qr=...&language=g...    │
│ ✓ QR parameters preserved                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 1.5: Close Popup/Modal (OPTIONAL)                         │
│ <button aria-label="Close">X</button>                          │
│ ⚠️  May or may not appear - don't fail if not found            │
│ ✓ Will skip if popup not present                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Click "લૉગિન કરો" Button                               │
│ <button class="font-extrabold text-[#B30C1D]...">              │
│   લૉગિન કરો                                                     │
│ </button>                                                       │
│ ⚠️  REQUIRED even on auth page!                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Login Form Appears                                              │
│ ┌─────────────────────────────┐                                 │
│ │ Mobile: [input type="tel"]  │                                 │
│ │ Password: [input type="pwd"]│                                 │
│ │ [Submit Button]             │                                 │
│ └─────────────────────────────┘                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Enter Mobile Number                                    │
│ Input: 9876543210                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Enter Password                                          │
│ Input: ********                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Click Submit/Login Button                              │
│ <button type="submit">લૉગિન</button>                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Login Processing                                                │
│ ✓ Authentication                                                │
│ ✓ QR parameters automatically processed                         │
│ ✓ Redirect to dashboard/quiz page                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5.5: Close Post-Login Popup (OPTIONAL)                    │
│ Check for any popup after login and close if present           │
│ ✓ Will skip if no popup                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Click User Avatar (Profile Icon)                       │
│ <div class="MuiAvatar-root MuiAvatar-circular">R</div>         │
│ Material-UI circular avatar - Opens profile menu               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Profile Menu Appears                                            │
│ Material-UI Menu dropdown with options                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Click Logout Menu Item                                 │
│ <li role="menuitem">                                            │
│   <svg><!-- Exit icon --></svg>                                 │
│   લૉગઆઉટ                                                        │
│ </li>                                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ ✓✓✓ AUTOMATION COMPLETE ✓✓✓                                    │
│ User logged out successfully                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Points

### 0. Optional Close Button (Popup/Modal)
A close button may appear at any point (after redirect or after login):

**Button HTML:**
```html
<button class="absolute top-4 right-4 w-8 h-8..." aria-label="Close">
  <svg class="w-5 h-5 text-white"><!-- X icon --></svg>
</button>
```

**Handling Strategy:**
- Use short timeout (2 seconds) to check for it
- If found, click it
- If not found, continue without error
- Check after QR redirect AND after login

**Code:**
```python
try:
    close_btn = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
    )
    close_btn.click()
except TimeoutException:
    pass  # No popup, continue
```

### 1. QR URL Redirect
- **Input**: `https://jeeto16cr.com/q/R6RcHQ`
- **Output**: `https://jeeto16cr.com/auth/register?qr=1768044780551_2&language=g&mode=online&groupType=db`
- **Parameters**: All QR params are preserved in the URL

### 2. Login Button (CRITICAL!)
Even though you're on the auth/register page, **you MUST click the "લૉગિન કરો" button** to show the login form.

**Button HTML:**
```html
<button type="button" 
        class="font-extrabold text-[#B30C1D] hover:text-[#A10A19] transition-colors hover:underline">
  લૉગિન કરો
</button>
```

**Why?** 
- The auth page shows both register and login options
- Clicking "લૉગિન કરો" switches to login form view
- Without clicking, login inputs won't be visible

### 3. Login Form
After clicking "લૉગિન કરો", the form appears:
- Mobile input: `<input type="tel">`
- Password input: `<input type="password">`
- Submit button: `<button type="submit">`

### 4. Post-Login
After successful login:
- QR parameters are automatically processed by the website
- User is redirected to the appropriate quiz/dashboard page
- No need to manually navigate to QR URL again

### 5. Logout (Material-UI Components)
- Click user avatar/profile icon (MUI circular avatar)
- Wait for profile menu dropdown to appear
- Click logout menu item with text "લૉગઆઉટ"

**Avatar HTML:**
```html
<div class="MuiAvatar-root MuiAvatar-circular MuiAvatar-colorDefault">
  R <!-- User's initial -->
</div>
```

**Logout Menu Item HTML:**
```html
<li class="MuiMenuItem-root" role="menuitem">
  <svg><!-- Exit icon --></svg>
  લૉગઆઉટ
</li>
```

**Implementation:**
```python
# Click avatar to open menu
avatar = driver.find_element(By.CSS_SELECTOR, "div.MuiAvatar-root.MuiAvatar-circular")
avatar.click()
time.sleep(1)  # Wait for menu animation

# Click logout menu item
logout_item = driver.find_element(By.XPATH, "//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]")
logout_item.click()
```

## Common Mistakes to Avoid

❌ **Don't skip clicking "લૉગિન કરો"**
```python
# WRONG - trying to enter credentials without clicking login button
mobile_input = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
# This will fail because form is not visible yet!
```

✅ **Always click "લૉગિન કરો" first**
```python
# CORRECT
login_btn.click()  # Show login form
time.sleep(2)      # Wait for form to appear
mobile_input = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
```

❌ **Don't go to homepage first**
```python
# WRONG - loses QR parameters
driver.get("https://jeeto16cr.com")  # Homepage
driver.get(qr_url)                    # QR URL
```

✅ **Go directly to QR URL**
```python
# CORRECT - preserves QR parameters
driver.get(qr_url)  # Direct to QR URL
```

## Testing Checklist

- [ ] Navigate to QR URL
- [ ] Wait for redirect to auth page
- [ ] Verify URL contains QR parameters
- [ ] Check for optional close button (popup)
- [ ] Click close button if present, or skip
- [ ] Click "લૉગિન કરો" button
- [ ] Wait for login form to appear
- [ ] Verify mobile and password inputs are visible
- [ ] Enter mobile number
- [ ] Enter password
- [ ] Click submit button
- [ ] Wait for login to complete
- [ ] Verify post-login URL
- [ ] Check for optional post-login popup
- [ ] Close popup if present, or skip
- [ ] Open side menu
- [ ] Find logout button
- [ ] Click logout
- [ ] Verify logout complete

---

**Created**: January 25, 2026  
**Purpose**: Visual guide for correct automation flow  
**Status**: Updated with login button requirement
