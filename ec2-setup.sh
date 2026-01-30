#!/bin/bash

#####################################
# EC2 Setup Script for Quiz Automation
# Run this script after connecting to EC2
#####################################

echo "================================================"
echo "Quiz Automation Server - EC2 Setup Script"
echo "================================================"
echo ""

# Exit on error
set -e

# Update system
echo "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "Step 2: Installing Python and pip..."
sudo apt install python3 python3-pip python3-venv -y

# Install Chrome
echo "Step 3: Installing Google Chrome..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
echo "Step 4: Installing ChromeDriver..."
sudo apt install chromium-chromedriver -y

# Install required system libraries
echo "Step 5: Installing system libraries..."
sudo apt install -y \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libgbm1 \
    libasound2 \
    unzip \
    wget

# Install Nginx
echo "Step 6: Installing Nginx..."
sudo apt install nginx -y

# Install git (optional)
echo "Step 7: Installing Git..."
sudo apt install git -y

# Verify installations
echo ""
echo "================================================"
echo "Verifying installations..."
echo "================================================"
python3 --version
pip3 --version
google-chrome --version
chromedriver --version
nginx -v
git --version

echo ""
echo "================================================"
echo "✓ System setup complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Upload your project files to ~/quiz-automation"
echo "2. cd ~/quiz-automation"
echo "3. Run: python3 -m venv venv"
echo "4. Run: source venv/bin/activate"
echo "5. Run: pip install -r requirements.txt"
echo "6. Edit automate.py to set headless=True"
echo "7. Test: python main.py"
echo ""
