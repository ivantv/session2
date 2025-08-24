#!/bin/bash

# Production startup script for EC2
# Organic Chemistry 3D Flask App

PORT=6061
APP_NAME="Organic Chemistry 3D"

echo "🧪 $APP_NAME - Production Server"
echo "=================================="

# Get the public IP of the EC2 instance
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)
PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4 2>/dev/null)

if [ ! -z "$PUBLIC_IP" ]; then
    echo "🌐 Public IP: $PUBLIC_IP"
    echo "🔗 External URL: http://$PUBLIC_IP:$PORT"
fi

if [ ! -z "$PRIVATE_IP" ]; then
    echo "🏠 Private IP: $PRIVATE_IP"
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down $APP_NAME..."
    
    # Kill any processes using our port
    PIDS=$(lsof -ti :$PORT 2>/dev/null)
    if [ ! -z "$PIDS" ]; then
        echo "🔄 Cleaning up processes on port $PORT..."
        echo $PIDS | xargs kill -9 2>/dev/null
        echo "✅ Port $PORT cleaned up"
    fi
    
    echo "✅ $APP_NAME shutdown complete"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Check if port is in use and clean it up
EXISTING_PIDS=$(lsof -ti :$PORT 2>/dev/null)
if [ ! -z "$EXISTING_PIDS" ]; then
    echo "⚠️  Port $PORT is in use. Cleaning up..."
    echo $EXISTING_PIDS | xargs kill -9 2>/dev/null
    sleep 1
    echo "✅ Port $PORT freed"
fi

# Check if running as root (not recommended for production)
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  WARNING: Running as root is not recommended for production"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
elif [ -d "../.venv" ]; then
    echo "🔄 Activating virtual environment..."
    source ../.venv/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing/updating dependencies..."
    pip install -r requirements.txt --quiet
fi

# Start the Flask application
echo "🚀 Starting Flask server on port $PORT..."
echo "🌐 Server will be accessible at:"
echo "   - Local: http://localhost:$PORT"
if [ ! -z "$PUBLIC_IP" ]; then
    echo "   - External: http://$PUBLIC_IP:$PORT"
    echo "   - Quiz: http://$PUBLIC_IP:$PORT/quiz"
fi
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo "=================================="

# Set environment variables for production
export FLASK_ENV=production
export PYTHONUNBUFFERED=1

# Run the application
python3 app.py
