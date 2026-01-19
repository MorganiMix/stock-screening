# Stock Screening Bot

A Python script that performs daily stock screening and sends results via Telegram.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your environment variables in the `.env` file:
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID
   - `DATA_PATH`: Path to your data directory (default: C:/temp/)
   - `EXCEL_FILENAME`: Name of your stock data Excel file
   - `START_DATE`: Start date for chart generation (default: 2024-01-01)

## Usage

### Run Daily Scheduler
```bash
python stock_screening_students_v8.py
```
This will start the scheduler to run the stock screening daily at 9:00 AM.

### Run Once (for testing)
```bash
python stock_screening_students_v8.py --run-once
```
This will run the stock screening immediately once.

## Features

- Downloads stock data from Yahoo Finance
- Calculates 1-day, 5-day, and 20-day returns
- Generates performance charts
- Sends results via Telegram (Excel file + chart)
- Daily scheduling with logging
- Error handling and recovery

## Files Generated

- `df_result_DDMMYYYY.xlsx`: Stock screening results
- `chart1.png`: Performance chart
- `stock_screening.log`: Application logs