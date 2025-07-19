# xyzBOT Commands for DeepBot

This repository contains command exports from xyzBOT that can be imported into DeepBot, plus the main Discord bot with livestream notifications.

## Files included:

- `deepbot_commands.json` - JSON format for API integration
- `deepbot_import.txt` - Text format for manual import
- `bot.py` - Discord bot with livestream notification functionality
- `README.md` - Full Discord bot documentation

## Import Instructions:

### Method 1: Direct Import
1. Download `deepbot_import.txt`
2. Open DeepBot
3. Go to **Commands** → **Import**
4. Select the downloaded file
5. Choose your import options
6. Apply settings

### Method 2: GitHub Integration
1. In DeepBot, go to **Settings** → **Integrations**
2. Connect your GitHub account
3. Add this repository URL: `https://github.com/yourusername/xyzbot-deepbot`
4. Set auto-sync to update commands automatically

### Method 3: Manual Copy
Copy individual commands from `deepbot_import.txt` into DeepBot manually.

## Commands Included:

### Currency System
- `!xyzs` - Check your currency balance
- `!send_xyzs` - Send currency to other users  
- `!give_xyzs` - Give currency (streamer only)
- `!top_xyzs` - Show currency leaderboard

### Queue System  
- `!queue` - Join the queue
- `!queue_list` - Show current queue
- `!next` - Call next person (mods only)
- `!clear_queue` - Clear queue (mods only)

### Fun Commands
- `!8ball` - Magic 8-ball responses
- `!roulette` - Russian roulette game
- `!slots` - Slot machine with betting
- `!joke` - Random jokes
- `!fact` - Random facts
- `!meme` - Random meme references

### Social Commands
- `!discord` - Show Discord link
- `!lurk` - Go into lurk mode
- `!unlurk` - Exit lurk mode  
- `!hug` - Give hugs to users
- `!shoutout` - Shoutout other streamers

### VIP System
- `!vips` - List all VIPs
- `!addvip` - Add VIP (mods only)
- `!removevip` - Remove VIP (mods only)

### Utility
- `!uptime` - Show stream uptime
- `!profile` - Show user stats

## Variable Setup:

DeepBot needs these user variables:
- `xyzs` (number) - User currency
- `xp` (number) - User experience points

Global variables:
- `active_users` (number) - Active user count
- `commands_used` (number) - Command usage counter

## Permissions:

- **Everyone**: Basic commands like !xyzs, !8ball, !lurk
- **Moderator**: Moderation commands like !addvip, !shoutout
- **Broadcaster**: Admin commands like !give_xyzs

## Cooldowns:

Commands have appropriate cooldowns to prevent spam:
- Basic commands: 5-10 seconds
- Social commands: 10-30 seconds  
- Games: 10-15 seconds

## Support:

For issues or questions, contact the streamer or check the original bot documentation.

---
*Generated from xyzBOT - Twitch Chat Bot*
