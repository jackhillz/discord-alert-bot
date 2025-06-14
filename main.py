import os
import logging
import discord
from discord.ext import commands

# Only load dotenv locally
if os.getenv("RENDER") is None:
    from dotenv import load_dotenv
    load_dotenv()

# Load the token
token = os.getenv("DISCORD_TOKEN")
print(f"✅ Token retrieved: {'Yes' if token else 'No'}")

# Setup logging to a file
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Setup bot
bot = commands.Bot(command_prefix='!', intents=intents)
secret_role = "Gamer"

# Events
@bot.event
async def on_ready():
    print(f"✅ Bot is ready! Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"👋 Welcome to the server, {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - don't use that word!")
    await bot.process_commands(message)

# Commands
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} role removed")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said: {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("🤫 Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("🚫 You do not have permission to do that!")

# Finally run the bot
print("🚀 Launching bot...")
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
