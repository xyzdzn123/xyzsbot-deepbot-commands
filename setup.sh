#!/bin/bash

# xyzBOT Discord Stream Notification Bot Setup Script
# This script helps set up the bot with proper configuration

echo "🚀 xyzBOT Discord Stream Notification Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

echo "✅ pip found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API credentials:"
    echo "   - Discord Bot Token"
    echo "   - Twitch Client ID and Secret"
    echo "   - YouTube API Key (optional)"
    echo "   - Streamer configuration"
    echo ""
    echo "   You can edit .env with: nano .env"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🔧 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Run the bot: python3 bot.py"
echo "3. Invite the bot to your Discord server with appropriate permissions"
echo ""
echo "For detailed setup instructions, see README.md"
echo ""
echo "Bot Commands:"
echo "  !stream_status - Check current stream status"
echo "  !set_notification_channel - Set notification channel (admin only)"
echo "  !notification_config - View configuration (admin only)"