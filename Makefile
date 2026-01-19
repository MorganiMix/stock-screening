# Stock Screening Bot Makefile

.PHONY: help build up down logs restart test clean setup

# Default target
help:
	@echo "Stock Screening Bot - Available commands:"
	@echo ""
	@echo "  setup     - Initial setup (copy .env.example to .env)"
	@echo "  build     - Build Docker image"
	@echo "  up        - Start services with Docker Compose"
	@echo "  down      - Stop services"
	@echo "  logs      - View real-time logs"
	@echo "  restart   - Restart services"
	@echo "  test      - Run single test execution"
	@echo "  clean     - Clean up containers and images"
	@echo "  install   - Install Python dependencies locally"
	@echo ""

# Initial setup
setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it with your credentials."; \
	else \
		echo ".env file already exists."; \
	fi
	@mkdir -p output logs

# Build Docker image
build:
	docker-compose build

# Start services
up:
	docker-compose up -d
	@echo "Stock screening bot started. Use 'make logs' to view output."

# Stop services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Restart services
restart:
	docker-compose restart
	@echo "Services restarted."

# Run single test
test:
	docker-compose run --rm stock-screening python stock_screening_students_v8.py --run-once

# Clean up
clean:
	docker-compose down -v
	docker system prune -f
	@echo "Cleaned up containers and images."

# Install dependencies locally
install:
	pip install -r requirements.txt

# Update and rebuild
update:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "Updated and restarted services."