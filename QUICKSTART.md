# Quick Start Guide - xyzBOT Discord Stream Notifications

This guide will get you up and running with the Discord stream notification bot in under 10 minutes.

## Prerequisites

- Python 3.8 or higher
- Discord account and server admin permissions
- Twitch Developer account
- YouTube Developer account (optional)

## Step 1: Get API Credentials

### Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Click "New Application" → Give it a name → Create
3. Go to "Bot" tab → Click "Add Bot"
4. Under "Token" click "Copy" (save this for later)
5. Enable "Message Content Intent" if needed

### Twitch API Credentials
1. Go to https://dev.twitch.tv/console
2. Click "Register Your Application"
3. Name: "xyzBOT Stream Notifications"
4. OAuth Redirect URLs: `http://localhost` 
5. Category: "Application Integration"
6. Click "Create"
7. Save the "Client ID" and "Client Secret"

### YouTube API Key (Optional)
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Save the API key

## Step 2: Download and Setup

```bash
# Clone the repository
git clone https://github.com/xyzdzn123/xyzsbot-deepbot-commands.git
cd xyzsbot-deepbot-commands

# Run the setup script
chmod +x setup.sh
./setup.sh
```

## Step 3: Configure Environment

Edit the `.env` file:
```bash
nano .env
```

Fill in your credentials:
```env
DISCORD_TOKEN=your_discord_bot_token_here
TWITCH_CLIENT_ID=your_twitch_client_id_here
TWITCH_CLIENT_SECRET=your_twitch_client_secret_here
YOUTUBE_API_KEY=your_youtube_api_key_here
STREAMER_TWITCH_USERNAME=xyzdzn123
```

## Step 4: Invite Bot to Discord

1. Go back to Discord Developer Portal → Your Application → OAuth2 → URL Generator
2. Select Scopes: `bot`
3. Select Bot Permissions:
   - Send Messages
   - Embed Links
   - View Channels
   - Read Message History
4. Copy the generated URL and open it in browser
5. Select your server and authorize

## Step 5: Run the Bot

```bash
python3 bot.py
```

You should see:
```
INFO:__main__:Logged in as YourBot#1234 (ID: 123456789)
INFO:__main__:Connected to 1 guilds
INFO:__main__:Bot YourBot#1234 is ready!
```

## Step 6: Test Commands

In your Discord server, try:
- `!stream_status` - Check if bot is working
- `!set_notification_channel #general` - Set notification channel (admin only)
- `!notification_config` - View current configuration

## Troubleshooting

**Bot not responding?**
- Check bot permissions in Discord server
- Verify token in .env file
- Make sure bot is online (no errors in console)

**No notifications?**
- Check if xyzdzn123 is actually streaming
- Verify Twitch username is correct
- Check bot logs for API errors

**Permission errors?**
- Make sure bot has "Send Messages" permission
- Try `!set_notification_channel` to set a specific channel

## Running 24/7

### Option 1: Screen (Linux/Mac)
```bash
screen -S xyzbot
python3 bot.py
# Press Ctrl+A then D to detach
```

### Option 2: Systemd Service (Linux)
Create `/etc/systemd/system/xyzbot.service`:
```ini
[Unit]
Description=xyzBOT Discord Stream Notifications
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/xyzsbot-deepbot-commands
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable xyzbot
sudo systemctl start xyzbot
```

### Option 3: Docker (Advanced)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "bot.py"]
```

```bash
docker build -t xyzbot .
docker run -d --env-file .env xyzbot
```

## Need Help?

- Check the full README.md for detailed documentation
- Review bot logs for error messages
- Ensure all API credentials are correct
- Test with `!stream_status` command first

---

*You're all set! The bot will now automatically notify your Discord servers when xyzdzn123 goes live.*