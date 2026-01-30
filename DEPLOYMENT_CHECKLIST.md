# 🚀 EC2 Deployment Checklist

## Pre-Deployment Checklist

### Local Preparation
- [ ] Test application locally with `python main.py`
- [ ] Verify all users in `users.json` are correct
- [ ] Ensure `requirements.txt` is up to date
- [ ] Review security settings
- [ ] Create backup of `users.json`

### AWS Account
- [ ] AWS account created and verified
- [ ] Payment method added
- [ ] Access to EC2 console
- [ ] Understand pricing (see cost calculator)

---

## Deployment Checklist

### Phase 1: EC2 Instance Setup (10 min)
- [ ] Launch EC2 instance (Ubuntu 22.04 LTS)
- [ ] Instance type selected (`t2.small` recommended)
- [ ] Security group configured:
  - [ ] SSH (port 22) - My IP only
  - [ ] HTTP (port 80) - 0.0.0.0/0
  - [ ] Custom TCP (port 8000) - 0.0.0.0/0
  - [ ] HTTPS (port 443) - 0.0.0.0/0 (optional)
- [ ] Key pair created and downloaded (`quiz-automation-key.pem`)
- [ ] Key pair saved securely (can't redownload!)
- [ ] Storage set to 20 GB
- [ ] Instance launched successfully
- [ ] Public IP address noted: _________________

### Phase 2: Connect to EC2 (2 min)
- [ ] Key permissions set (`chmod 400` on Mac/Linux)
- [ ] Successfully connected via SSH
- [ ] Verified Ubuntu version: `lsb_release -a`

### Phase 3: Install Dependencies (5 min)
- [ ] System updated: `sudo apt update && sudo apt upgrade -y`
- [ ] Python installed: `python3 --version`
- [ ] Pip installed: `pip3 --version`
- [ ] Google Chrome installed: `google-chrome --version`
- [ ] ChromeDriver installed: `chromedriver --version`
- [ ] System libraries installed (xvfb, libnss3, etc.)
- [ ] Nginx installed: `nginx -v`

### Phase 4: Upload Project Files (3 min)
- [ ] Project uploaded to `~/quiz-automation/`
- [ ] All files present:
  - [ ] `main.py`
  - [ ] `automate.py`
  - [ ] `requirements.txt`
  - [ ] `users.json`
  - [ ] `quiz-automation.service`
  - [ ] `nginx-config.conf`
  - [ ] `deploy.sh`
  - [ ] Documentation files

### Phase 5: Setup Python Environment (5 min)
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] No installation errors
- [ ] Packages verified: `pip list`

### Phase 6: Configure Application (2 min)
- [ ] `automate.py` set to headless mode:
  ```python
  driver = setup_driver(headless=True)
  ```
- [ ] Logs directory created: `mkdir -p logs`
- [ ] File permissions set correctly
- [ ] `users.json` has correct credentials

### Phase 7: Setup Systemd Service (3 min)
- [ ] Service file copied: `sudo cp quiz-automation.service /etc/systemd/system/`
- [ ] Systemd reloaded: `sudo systemctl daemon-reload`
- [ ] Service enabled: `sudo systemctl enable quiz-automation`
- [ ] Service started: `sudo systemctl start quiz-automation`
- [ ] Service status checked: `sudo systemctl status quiz-automation`
- [ ] No errors in status output
- [ ] Service shows "active (running)"

### Phase 8: Test API (5 min)
- [ ] Health endpoint tested: `curl http://localhost:8000/health`
- [ ] Health check returns: `{"status":"healthy"}`
- [ ] Root endpoint tested: `curl http://localhost:8000/`
- [ ] API accessible from local machine
- [ ] Test QR processing:
  ```powershell
  Invoke-RestMethod -Uri "http://YOUR-EC2-IP:8000/process-qr" `
    -Method POST `
    -Body '{"qr_url":"https://jeeto16cr.com/q/R6RcHQ"}' `
    -ContentType "application/json"
  ```
- [ ] API returns valid response
- [ ] All users processed successfully

### Phase 9: Setup Nginx (Optional - 5 min)
- [ ] Nginx config copied to sites-available
- [ ] Config edited with correct domain/IP
- [ ] Symbolic link created to sites-enabled
- [ ] Nginx config tested: `sudo nginx -t`
- [ ] Nginx restarted: `sudo systemctl restart nginx`
- [ ] API accessible via Nginx (port 80)

### Phase 10: Setup SSL (Optional - 10 min)
- [ ] Domain name pointing to EC2 IP
- [ ] DNS propagated (check with `nslookup`)
- [ ] Certbot installed
- [ ] SSL certificate obtained
- [ ] HTTPS working: `https://yourdomain.com`
- [ ] HTTP redirects to HTTPS

---

## Post-Deployment Checklist

### Monitoring & Logs
- [ ] Logs accessible: `sudo journalctl -u quiz-automation -f`
- [ ] No errors in logs
- [ ] CloudWatch alarms setup (optional)
- [ ] Log rotation configured

### Security
- [ ] SSH security group restricted to My IP
- [ ] Users.json has strong passwords
- [ ] System updates scheduled
- [ ] Backup strategy in place
- [ ] `.env` file used for sensitive data (if applicable)

### Performance
- [ ] Load test performed (if expecting high traffic)
- [ ] Response times acceptable
- [ ] Memory usage monitored: `htop`
- [ ] Disk space checked: `df -h`

### Documentation
- [ ] API documentation accessible
- [ ] Deployment notes saved
- [ ] Server credentials documented securely
- [ ] Contact information updated

### Backup & Recovery
- [ ] Backup of `users.json` created
- [ ] Backup strategy documented
- [ ] Recovery procedure tested
- [ ] AMI snapshot created (optional)

---

## Operational Checklist

### Daily Operations
- [ ] Check service status: `sudo systemctl status quiz-automation`
- [ ] Monitor logs for errors
- [ ] Check disk space
- [ ] Verify API responsiveness

### Weekly Maintenance
- [ ] Review error logs
- [ ] Update system packages: `sudo apt update && sudo apt upgrade`
- [ ] Check for application updates
- [ ] Verify backups

### Monthly Tasks
- [ ] Review AWS billing
- [ ] Update dependencies if needed
- [ ] Performance review
- [ ] Security audit
- [ ] Backup rotation

---

## Troubleshooting Checklist

### Service Won't Start
- [ ] Check logs: `sudo journalctl -u quiz-automation -xe`
- [ ] Verify Python path in service file
- [ ] Check file permissions
- [ ] Test manual start: `cd ~/quiz-automation && source venv/bin/activate && python main.py`
- [ ] Check port 8000 not in use: `sudo netstat -tulpn | grep 8000`

### API Not Accessible
- [ ] Service running: `sudo systemctl status quiz-automation`
- [ ] Port 8000 open in security group
- [ ] Firewall not blocking: `sudo ufw status`
- [ ] Nginx configured correctly (if using)
- [ ] Test locally on EC2: `curl http://localhost:8000/health`

### Selenium/Chrome Issues
- [ ] Chrome installed: `google-chrome --version`
- [ ] ChromeDriver installed: `chromedriver --version`
- [ ] Version compatibility checked
- [ ] Headless mode enabled
- [ ] Display server available (xvfb)

### Performance Issues
- [ ] Memory usage: `free -h`
- [ ] CPU usage: `top`
- [ ] Disk space: `df -h`
- [ ] Consider upgrading instance type
- [ ] Add swap space if out of memory

---

## Rollback Plan

### If Deployment Fails
1. [ ] Stop new service: `sudo systemctl stop quiz-automation`
2. [ ] Restore from backup:
   ```bash
   cd ~/quiz-automation
   tar -xzf backups/backup-YYYYMMDD-HHMMSS.tar.gz
   ```
3. [ ] Restart service: `sudo systemctl start quiz-automation`
4. [ ] Verify old version working
5. [ ] Investigate failure cause

---

## Success Criteria

### Deployment Successful When:
- ✅ Service starts without errors
- ✅ API responds to health checks
- ✅ QR processing completes successfully
- ✅ All users can login and logout
- ✅ Logs show no critical errors
- ✅ API accessible from internet
- ✅ Response times acceptable (<30s per user)

---

## Contact & Support

### Server Details
- **Server IP**: _________________
- **Domain** (if applicable): _________________
- **Instance ID**: _________________
- **Key Pair Name**: quiz-automation-key
- **Region**: _________________

### Important Commands
```bash
# Check status
sudo systemctl status quiz-automation

# View logs
sudo journalctl -u quiz-automation -f

# Restart
sudo systemctl restart quiz-automation

# Stop
sudo systemctl stop quiz-automation

# Update
cd ~/quiz-automation && ./deploy.sh
```

---

**Deployment Date**: _________________  
**Deployed By**: _________________  
**Version**: 1.0.0  
**Status**: ⬜ Development | ⬜ Staging | ⬜ Production
