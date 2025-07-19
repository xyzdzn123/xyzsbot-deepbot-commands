import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio
import json
import os
from typing import Optional, Dict, List
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamNotificationBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        # Configuration from environment variables
        self.twitch_client_id = os.getenv('TWITCH_CLIENT_ID')
        self.twitch_client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.streamer_twitch = os.getenv('STREAMER_TWITCH_USERNAME', 'xyzdzn123')
        self.streamer_youtube_channel_id = os.getenv('STREAMER_YOUTUBE_CHANNEL_ID')
        self.twitch_stream_url = os.getenv('TWITCH_STREAM_URL', f'https://twitch.tv/{self.streamer_twitch}')
        self.youtube_stream_url = os.getenv('YOUTUBE_STREAM_URL', 'https://youtube.com/@xyzdzn123/live')
        self.check_interval = int(os.getenv('STREAM_CHECK_INTERVAL', '60'))
        self.default_channel_name = os.getenv('DEFAULT_NOTIFICATION_CHANNEL_NAME', 'general')
        
        # Stream status tracking
        self.twitch_live = False
        self.youtube_live = False
        self.twitch_access_token = None
        
        # Configuration storage per guild
        self.guild_configs = {}
        
        # Session for HTTP requests
        self.session = None

    async def setup_hook(self):
        """Initialize the bot after login"""
        self.session = aiohttp.ClientSession()
        await self.get_twitch_access_token()
        
        # Start stream monitoring
        if not self.stream_monitor.is_running():
            self.stream_monitor.start()
        
        logger.info(f"Bot {self.user} is ready!")

    async def close(self):
        """Clean up when bot is shutting down"""
        if self.session:
            await self.session.close()
        await super().close()

    async def get_twitch_access_token(self) -> bool:
        """Get Twitch API access token"""
        if not self.twitch_client_id or not self.twitch_client_secret:
            logger.warning("Twitch credentials not configured")
            return False
            
        try:
            url = "https://id.twitch.tv/oauth2/token"
            data = {
                'client_id': self.twitch_client_id,
                'client_secret': self.twitch_client_secret,
                'grant_type': 'client_credentials'
            }
            
            async with self.session.post(url, data=data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    self.twitch_access_token = token_data.get('access_token')
                    logger.info("Twitch access token obtained successfully")
                    return True
                else:
                    logger.error(f"Failed to get Twitch access token: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Error getting Twitch access token: {e}")
            return False

    async def check_twitch_stream(self) -> bool:
        """Check if streamer is live on Twitch"""
        if not self.twitch_access_token:
            return False
            
        try:
            url = f"https://api.twitch.tv/helix/streams?user_login={self.streamer_twitch}"
            headers = {
                'Client-ID': self.twitch_client_id,
                'Authorization': f'Bearer {self.twitch_access_token}'
            }
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return len(data.get('data', [])) > 0
                elif response.status == 401:
                    # Token expired, try to refresh
                    await self.get_twitch_access_token()
                    return False
                else:
                    logger.error(f"Twitch API error: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Error checking Twitch stream: {e}")
            return False

    async def check_youtube_stream(self) -> bool:
        """Check if streamer is live on YouTube"""
        if not self.youtube_api_key or not self.streamer_youtube_channel_id:
            return False
            
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'channelId': self.streamer_youtube_channel_id,
                'eventType': 'live',
                'type': 'video',
                'key': self.youtube_api_key
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return len(data.get('items', [])) > 0
                else:
                    logger.error(f"YouTube API error: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Error checking YouTube stream: {e}")
            return False

    async def find_notification_channel(self, guild: discord.Guild) -> Optional[discord.TextChannel]:
        """Find a suitable channel for notifications in a guild"""
        guild_config = self.guild_configs.get(guild.id, {})
        
        # Check if there's a configured notification channel
        configured_channel_id = guild_config.get('notification_channel_id')
        if configured_channel_id:
            channel = guild.get_channel(configured_channel_id)
            if channel and isinstance(channel, discord.TextChannel):
                # Check if bot has permission to send messages
                if channel.permissions_for(guild.me).send_messages:
                    return channel
        
        # Look for channels by priority
        channel_priorities = [
            guild_config.get('notification_channel_name', self.default_channel_name),
            'general',
            'chat',
            'announcements',
            'bot-commands',
            'notifications'
        ]
        
        for channel_name in channel_priorities:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel and channel.permissions_for(guild.me).send_messages:
                return channel
        
        # Fall back to any channel where bot can send messages
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel
        
        return None

    async def send_stream_notification(self, platform: str, stream_url: str):
        """Send stream notification to all guilds"""
        embed = discord.Embed(
            title="🔴 xyzdzn123 is now LIVE!",
            description=f"Come watch the stream on {platform}!",
            color=0x9146FF if platform.lower() == 'twitch' else 0xFF0000,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="Stream Link",
            value=f"[Click here to watch!]({stream_url})",
            inline=False
        )
        
        embed.set_footer(text=f"Live on {platform}")
        
        sent_count = 0
        failed_count = 0
        
        for guild in self.guilds:
            try:
                channel = await self.find_notification_channel(guild)
                if channel:
                    await channel.send(embed=embed)
                    sent_count += 1
                    logger.info(f"Sent notification to {guild.name} (#{channel.name})")
                else:
                    failed_count += 1
                    logger.warning(f"No suitable channel found in {guild.name}")
            except discord.Forbidden:
                failed_count += 1
                logger.error(f"No permission to send messages in {guild.name}")
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to send notification to {guild.name}: {e}")
        
        logger.info(f"Stream notification sent to {sent_count} guilds, failed in {failed_count} guilds")

    @tasks.loop(seconds=60)  # Default interval, will be updated from config
    async def stream_monitor(self):
        """Monitor stream status and send notifications"""
        try:
            # Update loop interval from config (only if different)
            if self.stream_monitor.seconds != self.check_interval:
                self.stream_monitor.change_interval(seconds=self.check_interval)
            
            # Check Twitch
            twitch_is_live = await self.check_twitch_stream()
            if twitch_is_live and not self.twitch_live:
                # Stream just started
                await self.send_stream_notification("Twitch", self.twitch_stream_url)
                self.twitch_live = True
            elif not twitch_is_live and self.twitch_live:
                # Stream ended
                self.twitch_live = False
                logger.info("Twitch stream ended")
            
            # Check YouTube
            youtube_is_live = await self.check_youtube_stream()
            if youtube_is_live and not self.youtube_live:
                # Stream just started
                await self.send_stream_notification("YouTube", self.youtube_stream_url)
                self.youtube_live = True
            elif not youtube_is_live and self.youtube_live:
                # Stream ended
                self.youtube_live = False
                logger.info("YouTube stream ended")
                
        except Exception as e:
            logger.error(f"Error in stream monitor: {e}")

    @stream_monitor.before_loop
    async def before_stream_monitor(self):
        """Wait until bot is ready before starting stream monitor"""
        await self.wait_until_ready()

    # Admin commands for configuration
    @commands.command(name='set_notification_channel')
    @commands.has_permissions(administrator=True)
    async def set_notification_channel(self, ctx, channel: discord.TextChannel = None):
        """Set the notification channel for this server"""
        if channel is None:
            channel = ctx.channel
        
        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("❌ I don't have permission to send messages in that channel!")
            return
        
        if ctx.guild.id not in self.guild_configs:
            self.guild_configs[ctx.guild.id] = {}
        
        self.guild_configs[ctx.guild.id]['notification_channel_id'] = channel.id
        
        embed = discord.Embed(
            title="✅ Notification Channel Set",
            description=f"Stream notifications will be sent to {channel.mention}",
            color=0x00FF00
        )
        await ctx.send(embed=embed)

    @commands.command(name='stream_status')
    async def stream_status(self, ctx):
        """Check current stream status"""
        embed = discord.Embed(
            title="📺 Stream Status",
            color=0x9146FF
        )
        
        twitch_status = "🔴 LIVE" if self.twitch_live else "⚫ Offline"
        youtube_status = "🔴 LIVE" if self.youtube_live else "⚫ Offline"
        
        embed.add_field(name="Twitch", value=twitch_status, inline=True)
        embed.add_field(name="YouTube", value=youtube_status, inline=True)
        
        if self.twitch_live:
            embed.add_field(name="Twitch Link", value=f"[Watch on Twitch]({self.twitch_stream_url})", inline=False)
        if self.youtube_live:
            embed.add_field(name="YouTube Link", value=f"[Watch on YouTube]({self.youtube_stream_url})", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='notification_config')
    @commands.has_permissions(administrator=True)
    async def notification_config(self, ctx):
        """Show current notification configuration for this server"""
        guild_config = self.guild_configs.get(ctx.guild.id, {})
        
        embed = discord.Embed(
            title="🔧 Notification Configuration",
            color=0x0099FF
        )
        
        # Current notification channel
        channel_id = guild_config.get('notification_channel_id')
        if channel_id:
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                embed.add_field(
                    name="Notification Channel",
                    value=channel.mention,
                    inline=False
                )
            else:
                embed.add_field(
                    name="Notification Channel",
                    value="⚠️ Configured channel not found",
                    inline=False
                )
        else:
            embed.add_field(
                name="Notification Channel",
                value="Not configured (will use default)",
                inline=False
            )
        
        # Show what channel would be used
        current_channel = await self.find_notification_channel(ctx.guild)
        if current_channel:
            embed.add_field(
                name="Current Target Channel",
                value=current_channel.mention,
                inline=False
            )
        else:
            embed.add_field(
                name="Current Target Channel",
                value="❌ No suitable channel found",
                inline=False
            )
        
        embed.add_field(
            name="Check Interval",
            value=f"{self.check_interval} seconds",
            inline=True
        )
        
        embed.add_field(
            name="Monitored Streamer",
            value=self.streamer_twitch,
            inline=True
        )
        
        await ctx.send(embed=embed)

    @set_notification_channel.error
    @notification_config.error
    async def admin_command_error(self, ctx, error):
        """Handle admin command errors"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need administrator permissions to use this command!")
        else:
            logger.error(f"Command error: {error}")
            await ctx.send("❌ An error occurred while executing the command.")

    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'Connected to {len(self.guilds)} guilds')
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{self.streamer_twitch} for streams"
        )
        await self.change_presence(activity=activity)

    async def on_guild_join(self, guild):
        """Called when bot joins a new guild"""
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
        # Try to send a welcome message
        channel = await self.find_notification_channel(guild)
        if channel:
            embed = discord.Embed(
                title="👋 Hello!",
                description=f"Thanks for adding me to {guild.name}!",
                color=0x00FF00
            )
            embed.add_field(
                name="Stream Notifications",
                value=f"I'll automatically notify you when {self.streamer_twitch} goes live on Twitch or YouTube!",
                inline=False
            )
            embed.add_field(
                name="Configuration",
                value="Administrators can use `!set_notification_channel` to choose where notifications are sent.",
                inline=False
            )
            embed.add_field(
                name="Commands",
                value="`!stream_status` - Check current stream status\n`!notification_config` - View configuration",
                inline=False
            )
            
            try:
                await channel.send(embed=embed)
            except Exception as e:
                logger.error(f"Failed to send welcome message to {guild.name}: {e}")

def main():
    """Main function to run the bot"""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        logger.error("Please create a .env file based on .env.example")
        return
    
    bot = StreamNotificationBot()
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        logger.error("Invalid Discord token!")
    except Exception as e:
        logger.error(f"Failed to run bot: {e}")

if __name__ == "__main__":
    main()