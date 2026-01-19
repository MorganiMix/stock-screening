# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 21:12:07 2022

@author: Victor Lee
"""

import pandas as pd
import numpy as np
import yfinance as yf
import time
import telegram
import matplotlib.pyplot as plt
from datetime import date
import asyncio
import warnings
import os
import schedule
from dotenv import load_dotenv
import logging

warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
TOKEN = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
path = os.getenv('DATA_PATH', './')
filename = os.getenv('EXCEL_FILENAME', 'AASTOCKS_Export_2025-7-13.xlsx')
date1 = os.getenv('START_DATE', '2024-01-01')

# Ensure output and logs directories exist
os.makedirs('output', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Setup logging with fallback
log_handlers = [logging.StreamHandler()]

try:
    # Try to create file handler
    log_handlers.append(logging.FileHandler('logs/stock_screening.log'))
except PermissionError:
    # Fallback to current directory if logs/ is not writable
    try:
        log_handlers.append(logging.FileHandler('stock_screening.log'))
        print("Warning: Using current directory for log file due to permission issues")
    except PermissionError:
        print("Warning: Cannot create log file, using console logging only")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=log_handlers
)
def run_stock_screening():
    """Main function to run the stock screening process"""
    try:
        logging.info("Starting stock screening process...")
        
        today = date.today().strftime("%d%m%Y")
        
        # Validate environment variables
        if not TOKEN or not chat_id:
            logging.error("Missing Telegram credentials in environment variables")
            return
        
        # Import excel with stock codes and create a list L_stock which stores the 
        # stock codes
        try:
            L_stocks = pd.read_excel(path + filename)["代號"].tolist()
            L_stocks = [i[1:] for i in L_stocks]
            L_stocks.append("^HSI")
            L_stocks_names = pd.read_excel(path + filename)["名稱"].tolist()
            L_stocks_names.append("恆生指數")
            logging.info(f"Loaded {len(L_stocks)} stocks for screening")
        except Exception as e:
            logging.error(f"Error loading stock data from Excel: {e}")
            return
        
        # Download stock data
        D_stocks = getdata(L_stocks)
        
        # Generate results table
        df_result = table_gen1(D_stocks, L_stocks, L_stocks_names)
        
        # Save results to Excel
        result_filename = f"output/df_result_{today}.xlsx"
        df_result.to_excel(result_filename, index=False)
        logging.info(f"Results saved to {result_filename}")
        
        # Generate chart
        generate_chart(D_stocks, df_result, today)
        
        # Send results via Telegram
        asyncio.run(send_telegram_results(today))
        
        logging.info("Stock screening process completed successfully")
        
    except Exception as e:
        logging.error(f"Error in stock screening process: {e}")

def generate_chart(D_stocks, df_result, today):
    """Generate and save the performance chart"""
    try:
        L_coins_sorted = df_result["Stock Code"].iloc[:5].tolist()
        L_coins_sorted.append("^HSI")
        
        f1, ax = plt.subplots(figsize=(15, 10))
        for i in L_coins_sorted:
            ax.plot(D_stocks[i].loc[date1:].index,
                   D_stocks[i].loc[date1:]["Close"] / D_stocks[i].loc[date1:]["Close"].iloc[0],
                   label=i, linewidth=1)
        ax.legend()
        ax.grid(True)
        plt.title(f"Stock Performance Chart - {today}")
        plt.savefig("output/chart1.png")
        plt.close()
        logging.info("Chart generated successfully")
    except Exception as e:
        logging.error(f"Error generating chart: {e}")

async def send_telegram_results(today):
    """Send results to Telegram"""
    try:
        bot = telegram.Bot(token=TOKEN)
        
        # Send Excel file
        with open(f"output/df_result_{today}.xlsx", 'rb') as file:
            await bot.send_document(chat_id=chat_id, document=file)
        
        # Send chart
        with open('output/chart1.png', 'rb') as photo:
            await bot.send_photo(chat_id=chat_id, photo=photo)
        
        logging.info("Results sent to Telegram successfully")
    except Exception as e:
        logging.error(f"Error sending to Telegram: {e}")

# To download the stock data one by one and save it as a dictionary
def getdata(L):
    D1 = {}
    for i in L:
        try:
            df = yf.download(i, "2021-01-01", progress=False)
            df.columns = df.columns.droplevel('Ticker')
            message = "Now downloading data:" + i
            print(message)
            logging.info(message)
            D1[i] = df
        except Exception as e:
            logging.error(f"Error downloading data for {i}: {e}")
    return D1

# Based on the dictionary above generates the result with the return of previous 5 days and 
# previous 20 days
def table_gen1(D, L_stocks, L_stocks_names):
    L_return_1day = []
    L_return_5days = []
    L_return_20days = []
    
    for i in L_stocks:
        try:
            return1day = round(100 * (D[i]["Close"].iloc[-1] - D[i]["Close"].iloc[-2]) / D[i]["Close"].iloc[-2], 1)
            return5days = round(100 * (D[i]["Close"].iloc[-1] - D[i]["Close"].iloc[-5]) / D[i]["Close"].iloc[-5], 1)
            return20days = round(100 * (D[i]["Close"].iloc[-1] - D[i]["Close"].iloc[-20]) / D[i]["Close"].iloc[-20], 1)
            
            L_return_1day.append(return1day)
            L_return_5days.append(return5days)
            L_return_20days.append(return20days)
        except Exception as e:
            logging.error(f"Error calculating returns for {i}: {e}")
            L_return_1day.append(0)
            L_return_5days.append(0)
            L_return_20days.append(0)
    
    df_result = pd.DataFrame({
        "Stock Code": L_stocks,
        "Stock Name": L_stocks_names,
        "Return(1day)": L_return_1day,
        "Return(5days)": L_return_5days,
        "Return(20days)": L_return_20days
    })
    df_result.sort_values(["Return(1day)", "Return(5days)", "Return(20days)"], ascending=False, inplace=True)
    return df_result

def schedule_daily_task():
    """Schedule the stock screening to run daily"""
    # Schedule the task to run every day at 9:00 AM
    schedule.every().day.at("09:00").do(run_stock_screening)
    
    logging.info("Daily stock screening scheduled for 9:00 AM")
    print("Stock screening scheduled to run daily at 9:00 AM")
    print("Press Ctrl+C to stop the scheduler")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user")
            print("\nScheduler stopped.")
            break
        except Exception as e:
            logging.error(f"Error in scheduler: {e}")
            time.sleep(60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--run-once":
        # Run once for testing
        print("Running stock screening once...")
        run_stock_screening()
    else:
        # Start the daily scheduler
        print("Starting daily stock screening scheduler...")
        schedule_daily_task()

