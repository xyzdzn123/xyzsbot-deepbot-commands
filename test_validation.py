#!/usr/bin/env python3
"""
Test script to validate the Discord bot implementation
without requiring actual API credentials or Discord connection.
"""

import sys
import os
import ast

def validate_bot_structure():
    """Validate the bot.py file structure and key components"""
    print("🔍 Validating bot.py structure...")
    
    # Check if bot.py exists
    if not os.path.exists('bot.py'):
        print("❌ bot.py not found")
        return False
    
    try:
        with open('bot.py', 'r') as f:
            content = f.read()
        
        # Parse the file to check syntax
        tree = ast.parse(content)
        print("✅ Syntax validation passed")
        
        # Check for required components
        required_components = [
            'StreamNotificationBot',
            'check_twitch_stream',
            'check_youtube_stream',
            'find_notification_channel',
            'send_stream_notification',
            'stream_monitor',
            'set_notification_channel',
            'stream_status',
            'notification_config'
        ]
        
        for component in required_components:
            if component in content:
                print(f"✅ {component} found")
            else:
                print(f"❌ {component} missing")
                return False
        
        # Check for environment variable usage
        env_vars = [
            'DISCORD_TOKEN',
            'TWITCH_CLIENT_ID',
            'TWITCH_CLIENT_SECRET',
            'YOUTUBE_API_KEY',
            'STREAMER_TWITCH_USERNAME'
        ]
        
        for var in env_vars:
            if var in content:
                print(f"✅ {var} environment variable referenced")
            else:
                print(f"⚠️  {var} environment variable not found")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def validate_configuration_files():
    """Validate configuration files"""
    print("\n🔍 Validating configuration files...")
    
    # Check requirements.txt
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt found")
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
            if 'discord.py' in reqs:
                print("✅ discord.py requirement found")
            if 'aiohttp' in reqs:
                print("✅ aiohttp requirement found")
            if 'python-dotenv' in reqs:
                print("✅ python-dotenv requirement found")
    else:
        print("❌ requirements.txt not found")
        return False
    
    # Check .env.example
    if os.path.exists('.env.example'):
        print("✅ .env.example found")
        with open('.env.example', 'r') as f:
            env_content = f.read()
            required_vars = ['DISCORD_TOKEN', 'TWITCH_CLIENT_ID', 'YOUTUBE_API_KEY']
            for var in required_vars:
                if var in env_content:
                    print(f"✅ {var} in .env.example")
                else:
                    print(f"❌ {var} missing from .env.example")
    else:
        print("❌ .env.example not found")
        return False
    
    # Check .gitignore
    if os.path.exists('.gitignore'):
        print("✅ .gitignore found")
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                print("✅ .env excluded from git")
            else:
                print("⚠️  .env not excluded from git")
    else:
        print("⚠️  .gitignore not found")
    
    return True

def validate_documentation():
    """Validate documentation"""
    print("\n🔍 Validating documentation...")
    
    if os.path.exists('README.md'):
        print("✅ README.md found")
        with open('README.md', 'r') as f:
            readme_content = f.read()
            if 'Installation' in readme_content:
                print("✅ Installation instructions found")
            if 'Configuration' in readme_content:
                print("✅ Configuration section found")
            if 'Commands' in readme_content:
                print("✅ Commands documentation found")
    else:
        print("❌ README.md not found")
        return False
    
    return True

def main():
    """Run all validation tests"""
    print("🚀 Starting xyzBOT Discord Bot Validation\n")
    
    os.chdir('/home/runner/work/xyzsbot-deepbot-commands/xyzsbot-deepbot-commands')
    
    results = []
    results.append(validate_bot_structure())
    results.append(validate_configuration_files())
    results.append(validate_documentation())
    
    print(f"\n📊 Validation Results:")
    if all(results):
        print("🎉 All validations passed! Bot implementation looks good.")
        return 0
    else:
        print("❌ Some validations failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())