import discord
import random
import json
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from discord.ui import Button, View


# Intents and bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.members = True
# Welcome 
        # Event that triggers when a new member joins the server
@bot.event
async def on_member_join(member):
            # List of channel IDs where you want to send the welcome message
            channel_ids = [1281396798711402611, 1294968351541432380]  # Replace with your channel IDs

            # The welcome message that will be sent
            welcome_message = f"Welcome {member.mention} to the server! 🎉We are Glad to have you here."

            # Send the message in all specified channels
            for channel_id in channel_ids:
                channel = bot.get_channel(channel_id)
                if channel is not None:
                    await channel.send(welcome_message)
# Self Roles 

# JSON file path to store user data
USER_DATA_FILE = "user_data.json"
# Emojis 
# Cooldown duration (10 minutes)
cooldown_duration = timedelta(minutes=10)
# Helper function to load user data from JSON file
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return empty dict if file does not exist
# POTD ROLE GIVER
# Helper function to save user data to JSON file
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load existing data from file
user_data = load_user_data()

# Helper function to get current user data
def get_user_data(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {'balance': 0, 'last_earn': "1970-01-01 00:00:00"}
        save_user_data(user_data)
    return user_data[str(user_id)]

# Command to earn shards (with embed)
@bot.tree.command(name="earn", description="Earn Shards")
async def earn(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user = get_user_data(user_id)

    # Convert string date to datetime
    last_earn_time = datetime.strptime(user['last_earn'], "%Y-%m-%d %H:%M:%S")

    # Check cooldown
    now = datetime.now()
    if now - last_earn_time < cooldown_duration:
        remaining_time = cooldown_duration - (now - last_earn_time)
        minutes, seconds = divmod(remaining_time.total_seconds(), 60)

        # Embed for cooldown message
        embed = discord.Embed(
            title="Cooldown Alert",
            description=f"Please wait {int(minutes)} minutes and {int(seconds)} seconds before Using Comand again.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return

    # Give random shards (10-100)
    shards = random.randint(10, 100)
    user['balance'] += shards
    user['last_earn'] = now.strftime("%Y-%m-%d %H:%M:%S")  # Save datetime as string

    # Save updated data to file
    save_user_data(user_data)

    # Embed for successful earn
    embed = discord.Embed(
        title="Shards Earned!",
        description=f"<:shard:1294882576963604600> `-` {shards}",
        
        color=discord.Color.blue()
    )
    embed.set_footer(text="Shards will be used to rent Roles, Colors, and even Permissions soon!")
    await interaction.response.send_message(embed=embed)

# Command to check balance (with embed)
@bot.tree.command(name="balance", description="Check your balance")
async def balance(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user = get_user_data(user_id)

    # Give 1 shard if balance is 0
    if user['balance'] == 0:
        user['balance'] = 1
        description = "You had 0 shard, so we've given you 1 shard."
    else:
        description = f"<:shard:1294882576963604600> `-` {user['balance']}."

    # Save updated data to file
    save_user_data(user_data)

    # Embed for balance
    embed = discord.Embed(
        title=f"{interaction.user.display_name}'s Balance",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_footer(text="Shards will be used to rent Roles, Colors, and even Permissions soon!")
    await interaction.response.send_message(embed=embed)

# On ready event to sync commands with Discord
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync commands with Discord API
    
    print(f'Logged in as {bot.user}!')

# Run the bot with your token
bot.run("MTI5NDY1MDMxODQzNjQzODAyNg.G9IiWw.sSj5rdhy9Wzn43WNYbzBiZ0Luf9aIgx_gnFLtk")
