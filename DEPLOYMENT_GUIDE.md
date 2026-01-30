# AWS EC2 Deployment Guide

## 🚀 Complete Guide to Deploy Quiz Automation on EC2

---

## Prerequisites

### 1. AWS Account Requirements
- Active AWS account
- Access to EC2 service
- Basic understanding of SSH

### 2. Local Requirements
- SSH client (PuTTY for Windows or terminal for Mac/Linux)
- Your project files ready
- AWS CLI (optional but recommended)

---

## Step 1: Launch EC2 Instance

### 1.1 Choose AMI (Amazon Machine Image)
- Go to AWS Console → EC2 → Launch Instance
- **Recommended**: Ubuntu Server 22.04 LTS (Free tier eligible)
- Alternative: Amazon Linux 2023

### 1.2 Choose Instance Type
- **For testing**: `t2.micro` (Free tier - 1 vCPU, 1 GB RAM)
- **For production**: `t2.small` or `t2.medium` (Better performance)
- Click "Next: Configure Instance Details"

### 1.3 Configure Instance
- Keep default settings
- Enable "Auto-assign Public IP"
- Click "Next: Add Storage"

### 1.4 Add Storage
- Default: 8 GB (minimum)
- **Recommended**: 20 GB for Chrome and dependencies
- Click "Next: Add Tags"

### 1.5 Add Tags (Optional)
- Key: `Name`, Value: `Quiz-Automation-Server`
- Click "Next: Configure Security Group"

### 1.6 Configure Security Group
Create a new security group with these rules:

| Type | Protocol | Port | Source | Description |
|------|----------|------|--------|-------------|
| SSH | TCP | 22 | My IP | SSH access |
| Custom TCP | TCP | 8000 | 0.0.0.0/0 | FastAPI server |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Future SSL (optional) |

**Important**: For SSH, use "My IP" for security, or "0.0.0.0/0" if you need access from multiple locations.

### 1.7 Review and Launch
- Review your settings
- Click "Launch"
- **Create a new key pair**:
  - Name: `quiz-automation-key`
  - Download the `.pem` file
  - **SAVE IT SAFELY** - you can't download it again!
- Click "Launch Instances"

---

## Step 2: Connect to EC2 Instance

### Option A: Windows (Using PuTTY)

1. Convert `.pem` to `.ppk`:
   - Download PuTTYgen
   - Load your `.pem` file
   - Click "Save private key" as `.ppk`

2. Connect with PuTTY:
   - Host: `ubuntu@<your-ec2-public-ip>`
   - Port: 22
   - Connection → SSH → Auth → Browse to your `.ppk` file
   - Click "Open"

### Option B: Mac/Linux/Windows PowerShell

```bash
# Set permissions (first time only)
chmod 400 quiz-automation-key.pem

# Connect
ssh -i quiz-automation-key.pem ubuntu@<your-ec2-public-ip>
```

Replace `<your-ec2-public-ip>` with your instance's public IP from AWS console.

---

## Step 3: Install Dependencies on EC2

Once connected, run these commands:

### 3.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Install Python and Pip
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 3.3 Install Chrome and ChromeDriver
```bash
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Install ChromeDriver
sudo apt install chromium-chromedriver -y

# Verify installations
google-chrome --version
chromedriver --version
```

### 3.4 Install Required System Libraries
```bash
# For Selenium and Chrome
sudo apt install -y \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libgbm1 \
    libasound2
```

---

## Step 4: Upload Project Files

### Option A: Using SCP (From your local machine)

```bash
# From your local machine (not on EC2)
scp -i quiz-automation-key.pem -r "c:\Hetarth\Quiz automation" ubuntu@<your-ec2-ip>:~/quiz-automation
```

### Option B: Using Git (Recommended)

```bash
# On EC2
cd ~
git clone <your-repository-url> quiz-automation
# OR if not using git, manually upload files using SCP or FileZilla
```

### Option C: Manual Upload Using FileZilla (Windows Users)

1. Download FileZilla
2. Edit → Settings → SFTP → Add key file (your .ppk file)
3. Connect:
   - Host: `sftp://<your-ec2-ip>`
   - Username: `ubuntu`
   - Port: 22
4. Drag and drop your project folder

---

## Step 5: Setup Project on EC2

```bash
# Navigate to project directory
cd ~/quiz-automation

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Verify installation
pip list
```

---

## Step 6: Configure for Headless Mode

The server doesn't have a display, so Chrome must run in headless mode.

Edit `automate.py` to ensure headless is enabled:

```bash
nano automate.py
```

Find this line in `run_for_user()` function:
```python
driver = setup_driver(headless=False)
```

Change to:
```python
driver = setup_driver(headless=True)  # Must be True for EC2
```

Save: `Ctrl+O`, Enter, `Ctrl+X`

---

## Step 7: Test the Application

```bash
# Make sure you're in the project directory and venv is activated
cd ~/quiz-automation
source venv/bin/activate

# Test the server
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test from your local machine:**
```powershell
# Replace <your-ec2-ip> with your instance's public IP
Invoke-RestMethod -Uri "http://<your-ec2-ip>:8000/process-qr" -Method POST -Body '{"qr_url":"https://jeeto16cr.com/q/R6RcHQ"}' -ContentType "application/json"
```

Press `Ctrl+C` to stop the server.

---

## Step 8: Run Server in Background (Production)

### Option A: Using nohup (Simple)

```bash
# Run server in background
nohup python main.py > server.log 2>&1 &

# Check if running
ps aux | grep python

# View logs
tail -f server.log

# Stop server
pkill -f "python main.py"
```

### Option B: Using systemd (Recommended - Auto-restart)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/quiz-automation.service
```

Add this content:
```ini
[Unit]
Description=Quiz Automation FastAPI Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/quiz-automation
Environment="PATH=/home/ubuntu/quiz-automation/venv/bin"
ExecStart=/home/ubuntu/quiz-automation/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and enable:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable quiz-automation

# Start service
sudo systemctl start quiz-automation

# Check status
sudo systemctl status quiz-automation

# View logs
sudo journalctl -u quiz-automation -f

# Restart service
sudo systemctl restart quiz-automation

# Stop service
sudo systemctl stop quiz-automation
```

---

## Step 9: Setup Nginx Reverse Proxy (Optional but Recommended)

### Why Use Nginx?
- Better security
- SSL/HTTPS support
- Domain name support
- Load balancing

### Install Nginx
```bash
sudo apt install nginx -y
```

### Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/quiz-automation
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name <your-domain-or-ip>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and start:
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/quiz-automation /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable on boot
sudo systemctl enable nginx
```

Now access your API at: `http://<your-ec2-ip>/process-qr`

---

## Step 10: Monitor and Maintain

### View Application Logs
```bash
# If using systemd
sudo journalctl -u quiz-automation -f

# If using nohup
tail -f ~/quiz-automation/server.log
```

### Check Server Resources
```bash
# CPU and Memory usage
htop
# OR
top

# Disk usage
df -h

# Check running processes
ps aux | grep python
```

### Update Application
```bash
cd ~/quiz-automation

# Stop service
sudo systemctl stop quiz-automation

# Pull latest changes (if using git)
git pull

# OR upload new files via SCP/FileZilla

# Restart service
sudo systemctl start quiz-automation
```

---

## Security Best Practices

### 1. Use Environment Variables
Never hardcode sensitive data. Use `.env` file:

```bash
nano .env
```

Add:
```env
ALLOWED_ORIGINS=your-frontend-domain.com
SECRET_KEY=your-secret-key-here
```

### 2. Restrict Security Group
- Change SSH source from `0.0.0.0/0` to your IP
- Use Nginx and close port 8000 to public

### 3. Setup SSL (HTTPS)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (requires domain name)
sudo certbot --nginx -d yourdomain.com
```

### 4. Regular Updates
```bash
# Weekly security updates
sudo apt update && sudo apt upgrade -y
```

### 5. Backup users.json
```bash
# Create backup
cp users.json users.json.backup

# Restore if needed
cp users.json.backup users.json
```

---

## Troubleshooting

### Issue: Chrome/ChromeDriver not working
```bash
# Reinstall Chrome
sudo apt remove google-chrome-stable -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Check version compatibility
google-chrome --version
chromedriver --version
```

### Issue: Port 8000 not accessible
```bash
# Check if server is running
sudo netstat -tulpn | grep 8000

# Check security group in AWS Console
# Make sure port 8000 is open for 0.0.0.0/0
```

### Issue: Out of memory
```bash
# Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Issue: Permission denied for users.json
```bash
cd ~/quiz-automation
chmod 644 users.json
chown ubuntu:ubuntu users.json
```

---

## Cost Estimation

### EC2 Instance Costs (Monthly)
- **t2.micro** (Free tier): $0 for first 12 months, then ~$8.50/month
- **t2.small**: ~$17/month
- **t2.medium**: ~$34/month

### Data Transfer
- First 1 GB out: Free
- Next 9.999 TB: $0.09/GB

### Tips to Reduce Costs
- Stop instance when not in use (only pay for storage)
- Use reserved instances for long-term (up to 75% discount)
- Monitor usage with AWS CloudWatch

---

## Quick Reference Commands

```bash
# Connect to EC2
ssh -i quiz-automation-key.pem ubuntu@<ec2-ip>

# Activate virtual environment
cd ~/quiz-automation && source venv/bin/activate

# Check service status
sudo systemctl status quiz-automation

# View logs
sudo journalctl -u quiz-automation -f

# Restart service
sudo systemctl restart quiz-automation

# Stop service
sudo systemctl stop quiz-automation

# Update code
cd ~/quiz-automation && git pull && sudo systemctl restart quiz-automation
```

---

## Next Steps

1. ✅ **Domain Name**: Point a domain to your EC2 IP
2. ✅ **SSL Certificate**: Enable HTTPS with Let's Encrypt
3. ✅ **Monitoring**: Setup CloudWatch alarms
4. ✅ **Backup**: Configure automated backups
5. ✅ **CI/CD**: Setup automated deployments with GitHub Actions

---

**Deployment Date**: January 26, 2026  
**Status**: Production Ready  
**Server Type**: AWS EC2 Ubuntu 22.04 LTS
