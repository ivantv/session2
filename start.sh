#!/bin/bash

# Organic Chemistry 3D Flask App Starter Script
# This script properly manages the Flask application and port cleanup

PORT=6061
APP_NAME="Organic Chemistry 3D"

echo "🧪 $APP_NAME - Starting Application"
echo "=================================="

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

# Activate virtual environment if it exists
if [ -d "../.venv" ]; then
    echo "🔄 Activating virtual environment..."
    source ../.venv/bin/activate
fi

# Start the Flask application
echo "🚀 Starting Flask server on port $PORT..."
echo "🌐 Access your app at: http://localhost:$PORT"
echo "🧪 Quiz available at: http://localhost:$PORT/quiz"
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo "=================================="

# Run the application
python3 app.py
