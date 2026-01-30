#!/bin/bash

#####################################
# Deploy/Update Script
# Use this to update your application
#####################################

echo "================================================"
echo "Quiz Automation - Deployment Script"
echo "================================================"
echo ""

# Set variables
APP_DIR="/home/ubuntu/quiz-automation"
SERVICE_NAME="quiz-automation"

# Navigate to app directory
cd $APP_DIR || exit 1

echo "Step 1: Stopping service..."
sudo systemctl stop $SERVICE_NAME

echo "Step 2: Backing up current version..."
mkdir -p backups
tar -czf "backups/backup-$(date +%Y%m%d-%H%M%S).tar.gz" \
    --exclude='venv' \
    --exclude='backups' \
    --exclude='logs' \
    --exclude='__pycache__' \
    .

echo "Step 3: Pulling latest changes..."
# If using git
if [ -d ".git" ]; then
    git pull origin main
    echo "✓ Git pull complete"
else
    echo "⚠ Not a git repository. Please upload files manually."
fi

echo "Step 4: Activating virtual environment..."
source venv/bin/activate

echo "Step 5: Installing/updating dependencies..."
pip install -r requirements.txt --upgrade

echo "Step 6: Setting headless mode..."
sed -i 's/headless=False/headless=True/g' automate.py

echo "Step 7: Creating logs directory..."
mkdir -p logs

echo "Step 8: Setting permissions..."
chmod +x *.sh
chmod 644 users.json

echo "Step 9: Starting service..."
sudo systemctl start $SERVICE_NAME

echo "Step 10: Checking service status..."
sleep 2
sudo systemctl status $SERVICE_NAME --no-pager

echo ""
echo "================================================"
echo "✓ Deployment complete!"
echo "================================================"
echo ""
echo "View logs: sudo journalctl -u $SERVICE_NAME -f"
echo "Check status: sudo systemctl status $SERVICE_NAME"
echo ""
