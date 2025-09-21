# imports
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
from discord import SelectOption
from discord.ui import Select, View, Button
import random

# code
async def create_giveaway_embed(ctx, prize: str, duration: int, winners: int = 1):
    """
    Creates a professional giveaway embed
    
    Parameters:
        ctx (Context): Discord context object
        prize (str): The prize to be given away
        duration (int): Duration in minutes
        winners (int): Number of winners (default: 1)
    """
    end_time = datetime.now() + timedelta(minutes=duration)
    
    embed = discord.Embed(
        description=(
            f"## ```         Server - Giveaway Started        ```\n"
            f"__**Prize Information**__\n"
            f"> * **Prize**: `{prize}`\n"
            f"> * **Winners**: `{winners}`\n"
            f"> * **Duration**: `{duration} minutes`\n"
            f"> * **Ends**: <t:{int(end_time.timestamp())}:R>\n"
            f"__**How to Enter**__\n"
            f"> * React with 🎉 to enter!\n"
            f"> * Winner will be selected randomly"
        ),
        color=discord.Color(0x2c303d)
    )
    
    # Add banner
    embed.set_image(url="attachment://banner.png")
    
    # Send embed
    file = discord.File("banner.png", filename="banner.png")
    message = await ctx.send(file=file, embed=embed)
    
    # Add reaction
    await message.add_reaction("🎉")
    
    # Start timer
    await asyncio.sleep(duration * 60)
    
    # Get updated message
    message = await ctx.channel.fetch_message(message.id)
    
    # Get users who reacted
    reaction = discord.utils.get(message.reactions, emoji="🎉")
    users = [user async for user in reaction.users() if not user.bot]
    
    if not users:
        await ctx.send("No one entered the giveaway! 😢")
        return
    
    # Select winners
    winners_list = random.sample(users, min(winners, len(users)))
    winners_mentions = ", ".join(winner.mention for winner in winners_list)
    
    # Create embed
    winner_embed = discord.Embed(
        description=(
            f"## ```           Server - Giveaway Ended        ```\n"
            f"__**Winner Information**__\n"
            f"> * **Prize**: `{prize}`\n"
            f"> * **Winner(s)**: {winners_mentions}\n"
            f"\n🎉 Congratulations! Please contact the staff to claim your prize!"
        ),
        color=discord.Color(0x2c303d)
    )
    
    # Add banner 
    winner_embed.set_image(url="attachment://banner.png")
    
    # Send embed 
    file = discord.File("banner.png", filename="banner.png")
    await ctx.send(file=file, embed=winner_embed)

@bot.command()
async def giveaway(ctx, duration: int, winners: int, *, prize: str):
    """
    Starts a new giveaway
    
    Parameters:
        ctx (Context): Discord context object
        duration (int): Duration in minutes
        winners (int): Number of winners
        prize (str): The prize to be given away
    
    Usage:
        !giveaway <minutes> <winners> <prize>
        Example: !giveaway 60 1 Discord Nitro
    """
    await create_giveaway_embed(ctx, prize, duration, winners)
