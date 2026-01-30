# EC2 Deployment - Quick Start Guide

## 🚀 Fast Track Deployment (15 minutes)

### Step 1: Launch EC2 Instance (5 min)
1. Go to [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click "Launch Instance"
3. **Quick Settings**:
   - Name: `Quiz-Automation-Server`
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: `t2.small` (or `t2.micro` for free tier)
   - Key pair: Create new → Name: `quiz-automation-key` → Download `.pem`
   - Security Group: Allow SSH (22), Custom TCP (8000), HTTPS (443)
   - Storage: 20 GB
4. Click "Launch Instance"
5. Note your **Public IP address**

---

### Step 2: Connect to EC2 (2 min)

**Windows (PowerShell):**
```powershell
ssh -i quiz-automation-key.pem ubuntu@YOUR-EC2-IP
```

**Mac/Linux:**
```bash
chmod 400 quiz-automation-key.pem
ssh -i quiz-automation-key.pem ubuntu@YOUR-EC2-IP
```

---

### Step 3: Run Setup Script (5 min)

Copy and paste this **one command** on EC2:

```bash
wget -O - https://raw.githubusercontent.com/your-repo/main/ec2-setup.sh | bash
```

**OR manually upload and run:**

```bash
# After uploading ec2-setup.sh via SCP
chmod +x ec2-setup.sh
./ec2-setup.sh
```

---

### Step 4: Upload Project Files (2 min)

**From your Windows machine:**

```powershell
# Navigate to your project folder
cd "c:\Hetarth\Quiz automation"

# Upload files (replace YOUR-EC2-IP)
scp -i quiz-automation-key.pem -r * ubuntu@YOUR-EC2-IP:~/quiz-automation/
```

---

### Step 5: Setup Python Environment (2 min)

**On EC2:**

```bash
cd ~/quiz-automation

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Set headless mode
sed -i 's/headless=False/headless=True/g' automate.py

# Create logs directory
mkdir -p logs
```

---

### Step 6: Setup Systemd Service (1 min)

```bash
# Copy service file
sudo cp quiz-automation.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable quiz-automation
sudo systemctl start quiz-automation

# Check status
sudo systemctl status quiz-automation
```

---

### Step 7: Test Your API ✅

**From your local machine:**

```powershell
# Test the API (replace YOUR-EC2-IP)
Invoke-RestMethod -Uri "http://YOUR-EC2-IP:8000/process-qr" `
  -Method POST `
  -Body '{"qr_url":"https://jeeto16cr.com/q/R6RcHQ"}' `
  -ContentType "application/json"
```

**Expected Response:**
```json
{
  "qr_url": "https://jeeto16cr.com/q/R6RcHQ",
  "results": [
    { "mobile": "9999999999", "status": "success" },
    { "mobile": "8888888888", "status": "success" }
  ]
}
```

---

## 🎉 You're Live!

Your API is now running at: `http://YOUR-EC2-IP:8000`

---

## Essential Commands

### View Logs
```bash
# Real-time logs
sudo journalctl -u quiz-automation -f

# Last 100 lines
sudo journalctl -u quiz-automation -n 100
```

### Restart Service
```bash
sudo systemctl restart quiz-automation
```

### Stop Service
```bash
sudo systemctl stop quiz-automation
```

### Check Status
```bash
sudo systemctl status quiz-automation
```

### Update Application
```bash
cd ~/quiz-automation
./deploy.sh
```

---

## Optional: Setup Nginx (5 min)

```bash
# Copy nginx config
sudo cp nginx-config.conf /etc/nginx/sites-available/quiz-automation

# Create symbolic link
sudo ln -s /etc/nginx/sites-available/quiz-automation /etc/nginx/sites-enabled/

# Edit to add your domain/IP
sudo nano /etc/nginx/sites-available/quiz-automation

# Test config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

Now access via: `http://YOUR-EC2-IP/process-qr`

---

## Optional: Setup SSL with Let's Encrypt (5 min)

**Prerequisites**: You need a domain name pointing to your EC2 IP

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow prompts
# Certbot will automatically configure Nginx for HTTPS
```

Now access via: `https://yourdomain.com/process-qr`

---

## Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u quiz-automation -xe

# Check Python
which python3
/home/ubuntu/quiz-automation/venv/bin/python --version

# Test manually
cd ~/quiz-automation
source venv/bin/activate
python main.py
```

### Can't connect to port 8000
```bash
# Check security group in AWS Console
# Ensure port 8000 is open

# Check if service is running
sudo systemctl status quiz-automation

# Check if port is listening
sudo netstat -tulpn | grep 8000
```

### Chrome/Selenium issues
```bash
# Reinstall Chrome
sudo apt remove google-chrome-stable -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Verify
google-chrome --version
chromedriver --version
```

---

## File Upload via FileZilla (Alternative)

1. **Download FileZilla** from [filezilla-project.org](https://filezilla-project.org/)

2. **Convert PEM to PPK** (Windows only):
   - Open PuTTYgen
   - Load your `.pem` file
   - Save private key as `.ppk`

3. **Connect with FileZilla**:
   - Host: `sftp://YOUR-EC2-IP`
   - Username: `ubuntu`
   - Port: `22`
   - Edit → Settings → SFTP → Add key file (your `.ppk`)
   - Click "Connect"

4. **Upload Files**:
   - Navigate to `/home/ubuntu/quiz-automation`
   - Drag and drop your project files

---

## Estimated Costs

### Free Tier (12 months)
- **t2.micro**: FREE for 750 hours/month
- **Storage**: 30 GB FREE
- **Data Transfer**: 15 GB FREE

### After Free Tier
- **t2.micro**: ~$8.50/month
- **t2.small**: ~$17/month (Recommended)
- **t2.medium**: ~$34/month

### Tips to Save Money
- Stop instance when not in use
- Use reserved instances (up to 75% discount)
- Set up billing alerts

---

## Security Checklist

- [ ] Change SSH security group to "My IP" only
- [ ] Create backup of users.json
- [ ] Setup SSL certificate (for production)
- [ ] Enable CloudWatch monitoring
- [ ] Setup automated backups
- [ ] Use strong passwords in users.json
- [ ] Consider using AWS Secrets Manager for sensitive data

---

## Support & Resources

- Full Guide: See `DEPLOYMENT_GUIDE.md`
- AWS EC2 Docs: [aws.amazon.com/ec2](https://aws.amazon.com/ec2/)
- FastAPI Docs: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- Selenium Docs: [selenium.dev](https://www.selenium.dev/)

---

**Last Updated**: January 26, 2026  
**Deployment Time**: ~15 minutes  
**Difficulty**: Beginner-Friendly
