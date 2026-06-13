#!/bin/bash
# Adds a cron job to run fetch.py every weekday at 9:30 AM (market open)
# Run this script once to install the cron job.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$(which python3)"
CRON_LINE="30 9 * * 1-5 STOCKS_EMAIL_SENDER=your_gmail@gmail.com STOCKS_EMAIL_PASSWORD=your_app_password $PYTHON $SCRIPT_DIR/fetch.py >> $SCRIPT_DIR/fetch.log 2>&1"

# Check if already installed
if crontab -l 2>/dev/null | grep -qF "fetch.py"; then
    echo "Cron job already installed."
    crontab -l | grep "fetch.py"
    exit 0
fi

# Append to existing crontab
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
echo "Cron job installed:"
echo "  $CRON_LINE"
echo ""
echo "IMPORTANT: Edit the crontab to set your real Gmail credentials:"
echo "  crontab -e"
