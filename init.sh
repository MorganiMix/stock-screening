#!/bin/bash
# Initialization script for the stock screening bot

echo "Initializing stock screening bot..."

# Create directories if they don't exist
mkdir -p /app/output /app/logs

# Set proper permissions
chmod 755 /app/output /app/logs

# Check if we can write to the directories
if [ -w /app/output ] && [ -w /app/logs ]; then
    echo "✅ Directories created and writable"
else
    echo "⚠️  Warning: Directory permissions may be incorrect"
fi

# Check if Excel file exists
if [ -f "/app/${EXCEL_FILENAME:-AASTOCKS_Export_2025-7-13.xlsx}" ]; then
    echo "✅ Excel file found"
else
    echo "❌ Excel file not found: ${EXCEL_FILENAME:-AASTOCKS_Export_2025-7-13.xlsx}"
fi

# Check environment variables
if [ -z "$TELEGRAM_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "❌ Missing required environment variables"
    echo "   Please set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID"
    exit 1
else
    echo "✅ Environment variables configured"
fi

echo "Initialization complete. Starting application..."
exec "$@"