#!/bin/bash

# 🎬 CINEFLIX BOT - Start Script
# এই script bot সহজে চালু করতে সাহায্য করবে

echo "🎬 CINEFLIX BOT - Starting..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "📝 Please create .env file first:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    echo ""
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo ""
    echo "📥 Install Python 3:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   MacOS: brew install python3"
    echo ""
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed!"
    echo ""
    echo "📥 Install pip3:"
    echo "   Ubuntu/Debian: sudo apt install python3-pip"
    echo ""
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Load environment variables
export $(cat .env | xargs)

# Start the bot
echo "🚀 Starting CINEFLIX Bot..."
echo ""
echo "Press Ctrl+C to stop the bot"
echo ""

python3 bot.py
