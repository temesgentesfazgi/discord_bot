import os
import discord
from discord.ext import commands
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot
intents = discord.Intents.default()
intents.message_content = True  # Explicitly enable message content intent
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    print(f"Received message: {message.content}")
    await bot.process_commands(message)  # Pass the message to command processing

@bot.command(name="status")
async def status(ctx):
    response = f"Instance ID: {ec2_metadata.instance_id}\n"
    response += f"Public IP: {ec2_metadata.public_ipv4}\n"
    response += f"Region: {ec2_metadata.region}\n"
    await ctx.send(response)

@bot.command(name="details")
async def details(ctx):
    response = f"Instance Type: {ec2_metadata.instance_type}\n"
    response += f"AMI ID: {ec2_metadata.ami_id}\n"
    response += f"Availability Zone: {ec2_metadata.availability_zone}"
    await ctx.send(response)

@bot.command(name="debug_metadata")
async def debug_metadata(ctx):
    attributes = dir(ec2_metadata)
    await ctx.send(f"Available attributes: {attributes}")

bot.run(TOKEN)
