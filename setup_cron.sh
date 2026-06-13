#!/bin/bash
# Adds a cron job to run main.py every weekday at 9:30 AM (market open).
# Run this script once to install the cron job.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$SCRIPT_DIR/venv/bin/python3"
CRON_LINE="30 9 * * 1-5 cd $SCRIPT_DIR && $PYTHON main.py >> $SCRIPT_DIR/fetch.log 2>&1"

if crontab -l 2>/dev/null | grep -qF "main.py"; then
    echo "Cron job already installed:"
    crontab -l | grep "main.py"
    exit 0
fi

(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
echo "Cron job installed:"
echo "  $CRON_LINE"
