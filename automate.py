"""
Quiz Automation - Main Automation Script
Handles login, QR processing, and logout for multiple users
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_driver(headless=False):
    """
    Setup and configure Chrome WebDriver
    
    Args:
        headless (bool): Run browser in headless mode
        
    Returns:
        webdriver.Chrome: Configured Chrome driver
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
    
    # Additional options for stability
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Initialize driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    return driver


def close_popup_if_present(driver):
    """
    Close popup/modal if it appears (optional - won't fail if not present)
    
    Args:
        driver: WebDriver instance
        
    Returns:
        bool: True if popup was closed, False if no popup found
    """
    try:
        # Try to find the close button with various selectors
        close_button_selectors = [
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.XPATH, "//button[@aria-label='Close']"),
            (By.CSS_SELECTOR, "button.absolute.top-4.right-4"),
            (By.XPATH, "//button[contains(@class, 'absolute') and contains(@class, 'top-4') and contains(@class, 'right-4')]"),
        ]
        
        for by, selector in close_button_selectors:
            try:
                # Use a short wait (2 seconds) since this is optional
                wait = WebDriverWait(driver, 2)
                close_btn = wait.until(EC.element_to_be_clickable((by, selector)))
                close_btn.click()
                logger.info("✓ Optional popup/modal closed")
                time.sleep(0.5)
                return True
            except TimeoutException:
                continue
        
        logger.info("No popup/modal found (this is fine)")
        return False
        
    except Exception as e:
        logger.debug(f"No popup to close: {e}")
        return False


def click_login_button(driver, wait):
    """
    Step 1: Click the "લૉગિન કરો" button to show login form
    This button appears on both homepage and auth/register page after QR redirect
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        
    Raises:
        TimeoutException: If login button not found
    """
    logger.info("Step 1: Looking for 'લૉગિન કરો' button...")
    
    current_url = driver.current_url
    logger.info(f"Current URL: {current_url}")
    
    # Try multiple selectors for login button
    selectors = [
        (By.XPATH, "//button[contains(text(), 'લૉગિન કરો')]"),
        (By.CSS_SELECTOR, "button.font-extrabold.text-\\[\\#B30C1D\\]"),
        (By.XPATH, "//button[@type='button' and contains(@class, 'font-extrabold') and contains(@class, 'text-[#B30C1D]')]"),
        (By.CSS_SELECTOR, "button.font-extrabold"),
    ]
    
    for by, selector in selectors:
        try:
            login_btn = wait.until(EC.element_to_be_clickable((by, selector)))
            logger.info(f"✓ Found login button with selector: {selector}")
            login_btn.click()
            logger.info("✓ Login button clicked - waiting for login form...")
            time.sleep(2)  # Wait for login form to appear
            return
        except TimeoutException:
            logger.debug(f"Login button not found with selector: {selector}")
            continue
    
    raise TimeoutException("Login button 'લૉગિન કરો' not found with any selector")


def enter_credentials(driver, wait, mobile, password):
    """
    Step 2 & 3: Enter mobile number and password in the login form
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        mobile (str): Mobile number
        password (str): Password
        
    Raises:
        TimeoutException: If input fields not found
    """
    logger.info(f"Step 2 & 3: Entering credentials for mobile: {mobile}")
    
    # Enter mobile number - using name="username" (not "mobile"!)
    mobile_selectors = [
        (By.NAME, "username"),  # Primary selector - based on actual HTML
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[placeholder='મોબાઇલ નંબર']"),
        (By.CSS_SELECTOR, "input[type='text'][maxlength='10']"),
    ]
    
    mobile_entered = False
    for by, selector in mobile_selectors:
        try:
            mobile_input = wait.until(EC.presence_of_element_located((by, selector)))
            mobile_input.clear()
            mobile_input.send_keys(mobile)
            logger.info(f"✓ Mobile number entered using selector: {selector}")
            mobile_entered = True
            break
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"Mobile input not found with selector: {selector}")
            continue
    
    if not mobile_entered:
        raise TimeoutException("Mobile input field 'username' not found with any selector")
    
    time.sleep(0.5)
    
    # Enter password - using name="password"
    password_selectors = [
        (By.NAME, "password"),  # Primary selector
        (By.CSS_SELECTOR, "input[name='password']"),
        (By.CSS_SELECTOR, "input[placeholder='પાસવર્ડ']"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]
    
    password_entered = False
    for by, selector in password_selectors:
        try:
            password_input = wait.until(EC.presence_of_element_located((by, selector)))
            password_input.clear()
            password_input.send_keys(password)
            logger.info(f"✓ Password entered using selector: {selector}")
            password_entered = True
            break
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"Password input not found with selector: {selector}")
            continue
    
    if not password_entered:
        raise TimeoutException("Password input field not found with any selector")
    
    time.sleep(0.5)


def submit_login(driver, wait):
    """
    Step 4: Submit the login form by clicking the orange login button
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        
    Raises:
        TimeoutException: If submit button not found
    """
    logger.info("Step 4: Submitting login form...")
    
    # Try multiple selectors for the orange login submit button
    selectors = [
        (By.CSS_SELECTOR, "button[type='submit'].bg-\\[\\#efa029\\]"),  # Orange button with specific bg color
        (By.CSS_SELECTOR, "button[type='submit']"),  # Generic submit button
        (By.XPATH, "//button[@type='submit' and contains(@class, 'bg-[#efa029]')]"),
        (By.XPATH, "//button[@type='submit' and contains(., 'લૉગિન કરો')]"),  # Button with login text
        (By.XPATH, "//button[@type='submit']//span[contains(text(), 'લૉગિન કરો')]"),
    ]
    
    for by, selector in selectors:
        try:
            submit_btn = wait.until(EC.element_to_be_clickable((by, selector)))
            logger.info(f"✓ Found submit button with selector: {selector}")
            submit_btn.click()
            logger.info("✓ Login form submitted successfully")
            time.sleep(3)  # Wait for login to complete
            return
        except TimeoutException:
            continue
    
    raise TimeoutException("Submit button not found")


def verify_login_success(driver, wait):
    """
    Verify that login was successful
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        
    Raises:
        Exception: If login failed
    """
    logger.info("Verifying login success...")
    
    # Check for success indicators
    try:
        # Wait for success element or dashboard
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".success, .dashboard, [role='main']"))
        )
        logger.info("✓ Login successful")
        return True
    except TimeoutException:
        # Check if still on login page (error)
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, ".error, .alert-error")
            error_text = error_element.text
            raise Exception(f"Login failed: {error_text}")
        except NoSuchElementException:
            # No error shown, assume success
            logger.info("✓ Login assumed successful (no error displayed)")
            return True


def process_qr_page(driver, qr_url):
    """
    Navigate to QR URL and process the page
    
    Args:
        driver: WebDriver instance
        qr_url (str): The QR URL to visit
    """
    logger.info(f"Processing QR URL: {qr_url}")
    driver.get(qr_url)
    time.sleep(3)  # Wait for page to load
    logger.info("✓ QR page loaded")


def open_side_menu(driver, wait):
    """
    Step 5: Open the user profile menu by clicking the avatar
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        
    Raises:
        TimeoutException: If avatar/menu button not found
    """
    logger.info("Step 5: Opening user menu...")
    
    # Try multiple selectors for the MUI Avatar (profile picture)
    selectors = [
        # MUI Avatar with specific classes
        (By.CSS_SELECTOR, "div.MuiAvatar-root.MuiAvatar-circular"),
        (By.CSS_SELECTOR, ".MuiAvatar-root"),
        (By.XPATH, "//div[contains(@class, 'MuiAvatar-root') and contains(@class, 'MuiAvatar-circular')]"),
        # Alternative: button with avatar
        (By.CSS_SELECTOR, "button .MuiAvatar-root"),
        # Fallback: any clickable avatar
        (By.XPATH, "//div[contains(@class, 'MuiAvatar')]"),
    ]
    
    for by, selector in selectors:
        try:
            avatar = wait.until(EC.element_to_be_clickable((by, selector)))
            logger.info(f"✓ Found avatar/menu with selector: {selector}")
            avatar.click()
            logger.info("✓ User menu opened")
            time.sleep(1.5)  # Wait for menu animation
            return
        except TimeoutException:
            logger.debug(f"Avatar not found with selector: {selector}")
            continue
    
    raise TimeoutException("User avatar/menu button not found")


def click_logout(driver, wait):
    """
    Step 6: Click logout menu item (MUI MenuItem)
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        
    Raises:
        TimeoutException: If logout button not found
    """
    logger.info("Step 6: Clicking logout menu item...")
    
    # Try multiple selectors for the MUI MenuItem logout
    selectors = [
        # MUI MenuItem with logout text
        (By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and contains(., 'લૉગઆઉટ')]"),
        (By.CSS_SELECTOR, "li.MuiMenuItem-root"),  # Generic MUI menu item (check text after)
        (By.XPATH, "//li[@role='menuitem' and contains(., 'લૉગઆઉટ')]"),
        # Alternative selectors
        (By.XPATH, "//li[contains(text(), 'લૉગઆઉટ')]"),
        (By.XPATH, "//*[contains(text(), 'લૉગઆઉટ')]"),
    ]
    
    for by, selector in selectors:
        try:
            logout_item = wait.until(EC.element_to_be_clickable((by, selector)))
            logger.info(f"✓ Found logout menu item with selector: {selector}")
            logout_item.click()
            logger.info("✓ Logout clicked")
            time.sleep(2)  # Wait for logout to complete
            return
        except TimeoutException:
            logger.debug(f"Logout item not found with selector: {selector}")
            continue
    
    raise TimeoutException("Logout button not found in menu")


def run_for_user(user, qr_url):
    """
    Main automation function for a single user
    
    Args:
        user (dict): User dictionary with 'mobile' and 'password'
        qr_url (str): The QR URL to process
        
    Returns:
        dict: Result dictionary with mobile, status, and optional error
    """
    mobile = user.get("mobile")
    password = user.get("password")
    
    if not mobile or not password:
        return {
            "mobile": mobile or "unknown",
            "status": "error",
            "error": "Missing mobile or password in user data"
        }
    
    driver = None
    
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting automation for user: {mobile}")
        logger.info(f"QR URL: {qr_url}")
        logger.info(f"{'='*60}")
        
        # Setup driver
        driver = setup_driver(headless=True)  # Set to True for headless mode
        wait = WebDriverWait(driver, 15)
        
        # Navigate directly to QR URL (it will redirect to auth page with QR params)
        logger.info(f"Navigating to QR URL: {qr_url}")
        driver.get(qr_url)
        time.sleep(3)  # Wait for redirect to complete
        
        # Log the final URL after redirect
        final_url = driver.current_url
        logger.info(f"Redirected to: {final_url}")
        
        # Check and close any popup/modal if present (optional)
        close_popup_if_present(driver)
        
        # Step 1: Click login button
        click_login_button(driver, wait)
        
        # Step 2 & 3: Enter credentials
        enter_credentials(driver, wait, mobile, password)
        
        # Step 4: Submit login
        submit_login(driver, wait)
        
        # Verify login success
        verify_login_success(driver, wait)
        
        # After login, the QR parameters should be processed automatically
        # Wait a bit for any post-login processing
        time.sleep(3)
        logger.info(f"Post-login URL: {driver.current_url}")
        
        # Check for popup after login as well (optional)
        close_popup_if_present(driver)
        
        # Step 5: Open side menu
        open_side_menu(driver, wait)
        
        # Step 6: Click logout
        click_logout(driver, wait)
        
        logger.info(f"✓✓✓ Automation completed successfully for {mobile}")
        
        return {
            "mobile": mobile,
            "status": "success"
        }
        
    except TimeoutException as e:
        error_msg = f"Timeout: {str(e)}"
        logger.error(f"✗ {error_msg} for {mobile}")
        return {
            "mobile": mobile,
            "status": "error",
            "error": error_msg
        }
        
    except NoSuchElementException as e:
        error_msg = f"Element not found: {str(e)}"
        logger.error(f"✗ {error_msg} for {mobile}")
        return {
            "mobile": mobile,
            "status": "error",
            "error": error_msg
        }
        
    except WebDriverException as e:
        error_msg = f"WebDriver error: {str(e)}"
        logger.error(f"✗ {error_msg} for {mobile}")
        return {
            "mobile": mobile,
            "status": "error",
            "error": error_msg
        }
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"✗ {error_msg} for {mobile}")
        return {
            "mobile": mobile,
            "status": "error",
            "error": error_msg
        }
        
    finally:
        # Always close the driver
        if driver:
            try:
                driver.quit()
                logger.info(f"Browser closed for {mobile}")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")


# Test function for standalone execution
if __name__ == "__main__":
    # Test with sample user
    test_user = {
        "mobile": "9999999999",
        "password": "test123"
    }
    test_qr_url = "https://jeeto16cr.com/q/R6RcHQ"
    
    result = run_for_user(test_user, test_qr_url)
    print(f"\nResult: {result}")
