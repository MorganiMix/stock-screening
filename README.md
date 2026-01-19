# Stock Screening Bot

A Python application that performs automated daily stock screening and sends results via Telegram. The bot analyzes Hong Kong stocks, calculates returns over different periods, generates performance charts, and delivers comprehensive reports.

## Features

- 📊 **Automated Stock Analysis**: Downloads and analyzes stock data from Yahoo Finance
- 📈 **Performance Metrics**: Calculates 1-day, 5-day, and 20-day returns
- 📱 **Telegram Integration**: Sends Excel reports and charts directly to Telegram
- ⏰ **Daily Scheduling**: Runs automatically at scheduled times
- 🐳 **Docker Support**: Containerized deployment with Docker Compose
- 📝 **Comprehensive Logging**: Detailed logs for monitoring and debugging
- 🔒 **Secure Configuration**: Environment-based credential management

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Telegram bot token and chat ID

### 1. Clone and Setup
```bash
git clone https://github.com/MorganiMix/stock-screening
cd stock-screening
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 3. Run with Docker Compose
```bash
# Build and start the container
docker compose up -d

# View logs
docker compose logs -f

# Stop the container
docker compose down
```

## Manual Installation

### Prerequisites
- Python 3.10+
- pip package manager

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Telegram credentials
```

### 3. Run the Application
```bash
# Start daily scheduler
python stock_screening_students_v8.py

# Run once for testing
python stock_screening_students_v8.py --run-once
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TELEGRAM_TOKEN` | Your Telegram bot token | - | ✅ |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | - | ✅ |
| `DATA_PATH` | Path to data directory | `./` | ❌ |
| `EXCEL_FILENAME` | Stock data Excel filename | `AASTOCKS_Export_2025-7-13.xlsx` | ❌ |
| `START_DATE` | Chart start date | `2024-01-01` | ❌ |

### Getting Telegram Credentials

1. **Create a Bot**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Save the bot token

2. **Get Chat ID**:
   - Start a chat with your bot
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

### Schedule Configuration

By default, the bot runs daily at 9:00 AM. To change this:

```python
# In stock_screening_students_v8.py, modify:
schedule.every().day.at("09:00").do(run_stock_screening)

# Examples:
schedule.every().day.at("08:30").do(run_stock_screening)  # 8:30 AM
schedule.every().monday.at("09:00").do(run_stock_screening)  # Mondays only
schedule.every(2).hours.do(run_stock_screening)  # Every 2 hours
```

## Docker Deployment

### Docker Compose (Recommended)

The `docker-compose.yml` provides:
- Automatic container restart
- Volume mounting for persistent data
- Environment variable management
- Logging configuration

```bash
# Start in background
docker-compose up -d

# View real-time logs
docker-compose logs -f stock-screening

# Restart service
docker-compose restart

# Update and rebuild
docker-compose down
docker-compose up --build -d
```

### Manual Docker Commands

```bash
# Build image
docker build -t stock-screening-bot .

# Run container
docker run -d \
  --name stock-screening \
  --env-file .env \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  stock-screening-bot
```

## File Structure

```
stock-screening-bot/
├── stock_screening_students_v8.py  # Main application
├── requirements.txt                # Python dependencies
├── Dockerfile                     # Docker image definition
├── docker-compose.yml            # Docker Compose configuration
├── .env.example                  # Environment template
├── .env                         # Your environment variables (gitignored)
├── .gitignore                   # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── README.md                   # This documentation
├── AASTOCKS_Export_2025-7-13.xlsx  # Stock data file
├── output/                     # Generated files (Docker volume)
│   ├── df_result_DDMMYYYY.xlsx # Daily results
│   └── chart1.png             # Performance chart
└── logs/                      # Application logs (Docker volume)
    └── stock_screening.log    # Main log file
```

## Output Files

### Excel Report (`df_result_DDMMYYYY.xlsx`)
Contains stock analysis with columns:
- **Stock Code**: Hong Kong stock symbol
- **Stock Name**: Company name in Chinese
- **Return(1day)**: 1-day percentage return
- **Return(5days)**: 5-day percentage return  
- **Return(20days)**: 20-day percentage return

Sorted by performance (best performers first).

### Performance Chart (`chart1.png`)
Line chart showing:
- Top 5 performing stocks
- Hang Seng Index (^HSI) for comparison
- Normalized performance since start date
- Time series from configured start date

## Monitoring and Troubleshooting

### Viewing Logs

**Docker Compose:**
```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service logs
docker-compose logs stock-screening
```

**Manual Installation:**
```bash
# View log file
tail -f logs/stock_screening.log

# Check recent entries
tail -n 50 logs/stock_screening.log
```

### Common Issues

1. **Missing Telegram Credentials**
   ```
   ERROR - Missing Telegram credentials in environment variables
   ```
   - Ensure `.env` file exists with valid `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`

2. **Excel File Not Found**
   ```
   ERROR - Error loading stock data from Excel: [Errno 2] No such file or directory
   ```
   - Verify `EXCEL_FILENAME` path in `.env`
   - Ensure Excel file exists in the specified location

3. **Network Issues**
   ```
   ERROR - Error downloading data for XXXX.HK
   ```
   - Check internet connection
   - Yahoo Finance may be temporarily unavailable

4. **Telegram Send Failure**
   ```
   ERROR - Error sending to Telegram
   ```
   - Verify bot token and chat ID
   - Ensure bot has permission to send messages

### Health Checks

**Docker:**
```bash
# Check container health
docker-compose ps

# Container resource usage
docker stats stock-screening-bot
```

**Manual:**
```bash
# Test run
python stock_screening_students_v8.py --run-once

# Check process
ps aux | grep stock_screening
```

## Development

### Adding New Features

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes and test**
4. **Update documentation**
5. **Submit pull request**

### Testing

```bash
# Test single run
python stock_screening_students_v8.py --run-once

# Test with Docker
docker-compose run --rm stock-screening python stock_screening_students_v8.py --run-once
```

### Updating Stock List

1. Export new stock list from AASTOCKS
2. Replace `AASTOCKS_Export_2025-7-13.xlsx`
3. Update `EXCEL_FILENAME` in `.env` if filename changed
4. Restart the application

## Security Considerations

- ✅ Environment variables for sensitive data
- ✅ Non-root user in Docker container
- ✅ Read-only Excel file mounting
- ✅ Gitignored credential files
- ✅ Minimal Docker image (Python slim)

## Performance

- **Memory Usage**: ~200-300MB during execution
- **CPU Usage**: Low, spikes during data download/processing
- **Network**: Downloads ~86 stock datasets daily
- **Storage**: Logs and output files grow over time

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review application logs
3. Create an issue in the repository
4. Provide logs and configuration details (without credentials)

## Changelog

### v8.0 (Current)
- Added Docker support with Docker Compose
- Implemented comprehensive logging
- Added daily scheduling
- Environment-based configuration
- Error handling and recovery
- Modular code structure
- Security improvements
