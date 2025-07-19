# xyzBOT Discord Stream Notification Bot

A Discord bot that automatically sends notifications when xyzdzn123 goes live on Twitch or YouTube.

## Features

- **Automatic Stream Detection**: Monitors Twitch and YouTube for live streams
- **Multi-Server Support**: Works across all Discord servers where the bot is installed
- **Smart Channel Detection**: Automatically finds suitable channels with write permissions
- **Admin Configuration**: Server administrators can configure notification settings
- **Resource Efficient**: Configurable check intervals to minimize API usage
- **Customizable Links**: Stream URLs can be customized via environment variables

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/xyzdzn123/xyzsbot-deepbot-commands.git
   cd xyzsbot-deepbot-commands
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your API credentials:
   - Discord Bot Token
   - Twitch Client ID and Secret
   - YouTube API Key
   - Streamer configuration

4. **Run the bot**:
   ```bash
   python bot.py
   ```

## Configuration

### Required API Credentials

#### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Copy the bot token to `DISCORD_TOKEN` in `.env`

#### Twitch API
1. Go to [Twitch Developer Console](https://dev.twitch.tv/console)
2. Create a new application
3. Copy Client ID and Client Secret to `.env`

#### YouTube API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Create credentials (API Key)
4. Copy API key to `.env`

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Discord bot token | Required |
| `TWITCH_CLIENT_ID` | Twitch API client ID | Required |
| `TWITCH_CLIENT_SECRET` | Twitch API client secret | Required |
| `YOUTUBE_API_KEY` | YouTube Data API key | Optional |
| `STREAMER_TWITCH_USERNAME` | Twitch username to monitor | xyzdzn123 |
| `STREAMER_YOUTUBE_CHANNEL_ID` | YouTube channel ID to monitor | Optional |
| `TWITCH_STREAM_URL` | Custom Twitch stream URL | https://twitch.tv/xyzdzn123 |
| `YOUTUBE_STREAM_URL` | Custom YouTube stream URL | https://youtube.com/@xyzdzn123/live |
| `STREAM_CHECK_INTERVAL` | Check interval in seconds | 60 |
| `DEFAULT_NOTIFICATION_CHANNEL_NAME` | Default channel name to use | general |

## Bot Commands

### User Commands
- `!stream_status` - Check current stream status for Twitch and YouTube

### Admin Commands (Administrator permission required)
- `!set_notification_channel [#channel]` - Set notification channel for the server
- `!notification_config` - View current notification configuration

## How It Works

1. **Stream Monitoring**: The bot checks Twitch and YouTube APIs at regular intervals
2. **Live Detection**: When a stream starts, the bot detects the status change
3. **Channel Selection**: For each Discord server, the bot finds a suitable channel:
   - Configured notification channel (if set by admin)
   - Default channels like #general, #chat, #announcements
   - Any channel where the bot has send message permissions
4. **Notification**: Sends an embed message with stream link and platform info

## Channel Priority

The bot looks for notification channels in this order:
1. Admin-configured notification channel
2. Channel named after `DEFAULT_NOTIFICATION_CHANNEL_NAME`
3. #general
4. #chat
5. #announcements
6. #bot-commands
7. #notifications
8. Any channel with send message permissions

## Permissions Required

The bot needs these Discord permissions:
- **Send Messages**: To post notifications
- **Embed Links**: To send rich embed notifications
- **View Channels**: To find suitable channels
- **Read Message History**: To function properly

## Resource Efficiency

- **Configurable Check Intervals**: Adjust `STREAM_CHECK_INTERVAL` to balance responsiveness vs API usage
- **Token Caching**: Twitch access tokens are cached and refreshed as needed
- **Error Handling**: Graceful handling of API rate limits and errors
- **Minimal Memory Usage**: Lightweight design with efficient data structures

## Troubleshooting

### Bot Not Sending Notifications
1. Check bot permissions in Discord servers
2. Verify API credentials in `.env` file
3. Check if bot can find suitable channels (`!notification_config`)
4. Review bot logs for error messages

### API Rate Limits
- Increase `STREAM_CHECK_INTERVAL` if hitting rate limits
- Consider using webhooks for real-time notifications (advanced)

### Missing Notifications
- Verify streamer usernames/channel IDs are correct
- Check if APIs are returning expected data
- Ensure bot is online and monitoring

## Development

The bot is built with:
- **discord.py**: Discord API wrapper
- **aiohttp**: Async HTTP client for API requests
- **asyncio**: Asynchronous programming support
- **python-dotenv**: Environment variable management

### Adding New Platforms

To add support for new streaming platforms:
1. Implement a new check method (e.g., `check_platform_stream()`)
2. Add platform configuration to environment variables
3. Update the stream monitoring loop
4. Add platform-specific embed styling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the xyzBOT ecosystem. See the main repository for license information.

## Support

For support or questions:
- Check the troubleshooting section above
- Review bot logs for error messages
- Contact the streamer or bot maintainer

---

*Generated for xyzBOT Discord Stream Notification System*