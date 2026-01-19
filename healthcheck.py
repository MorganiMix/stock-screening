#!/usr/bin/env python3
"""
Health check script for the stock screening bot
"""

import os
import sys
import logging
from datetime import datetime, timedelta

def check_log_file():
    """Check if log file exists and has recent entries"""
    log_file = "logs/stock_screening.log"
    
    if not os.path.exists(log_file):
        print("❌ Log file not found")
        return False
    
    # Check if log file has been updated in the last 24 hours
    stat = os.stat(log_file)
    last_modified = datetime.fromtimestamp(stat.st_mtime)
    if datetime.now() - last_modified > timedelta(hours=24):
        print("⚠️  Log file is older than 24 hours")
        return False
    
    print("✅ Log file exists and is recent")
    return True

def check_output_directory():
    """Check if output directory exists"""
    if not os.path.exists("output"):
        print("❌ Output directory not found")
        return False
    
    print("✅ Output directory exists")
    return True

def check_excel_file():
    """Check if Excel file exists"""
    excel_file = os.getenv('EXCEL_FILENAME', 'AASTOCKS_Export_2025-7-13.xlsx')
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        return False
    
    print(f"✅ Excel file exists: {excel_file}")
    return True

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Required environment variables are set")
    return True

def main():
    """Run all health checks"""
    print("🔍 Running health checks...")
    print("-" * 40)
    
    checks = [
        check_environment,
        check_excel_file,
        check_output_directory,
        check_log_file,
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Error in {check.__name__}: {e}")
            results.append(False)
    
    print("-" * 40)
    
    if all(results):
        print("🎉 All health checks passed!")
        sys.exit(0)
    else:
        print("💥 Some health checks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()