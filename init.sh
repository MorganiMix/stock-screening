#!/bin/bash
# Initialization script for the stock screening bot

echo "Initializing stock screening bot..."

# Create output directory if it doesn't exist
mkdir -p /output

# Set proper permissions
sudo chmod 755 /output

# Check if we can write to the directory
if [ -w /output ]; then
    echo "✅ Output directory created and writable"
else
    echo "⚠️  Warning: Output directory permissions may be incorrect"
fi

# Check if Excel file exists
if [ -f "/${EXCEL_FILENAME:-AASTOCKS_Export_2025-7-13.xlsx}" ]; then
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