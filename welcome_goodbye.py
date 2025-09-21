# imports
import discord
from discord.ext import commands
from datetime import datetime
from typing import Dict

# code

welcome_channels: Dict[int, int] = {}

@bot.event
async def on_member_join(member):
    """Event triggered when a new member joins the server"""
    if member.guild.id not in welcome_channels:
        return
        
    channel = member.guild.get_channel(welcome_channels[member.guild.id])
    if not channel:
        return

    # embed
    embed = discord.Embed(
        description=(
            f"## ```            Welcome to the Server        ```\n"
            f"__**Welcome {member.name}!**__\n"
            f"> * Thanks for joining our community!\n"
            f"> * You are our `{member.guild.member_count}th` member\n"
            f"> * Account Created: <t:{int(member.created_at.timestamp())}:R>\n\n"
        ),
        color=discord.Color(0x2c303d)
    )

    embed.set_image(url="YOUR_BANNER_URL")
    
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    """Event triggered when a member leaves the server"""
    if member.guild.id not in welcome_channels:
        return
         
    channel = member.guild.get_channel(welcome_channels[member.guild.id])
    if not channel:
        return

    # Calculate
    if member.joined_at:
        joined_at = member.joined_at
        time_in_server = datetime.now(joined_at.tzinfo) - joined_at
        days = time_in_server.days
    else:
        joined_at = datetime.now()
        days = 0
    
    # goodbye embed
    embed = discord.Embed(
        description=(
            f"## ```                 Member Left        ```\n"
            f"__**Goodbye {member.name}**__\n"
            f"> * Member Count: `{member.guild.member_count}`\n"
            f"> * Joined: <t:{int(joined_at.timestamp())}:R>\n"
            f"> * Time in Server: `{days} days`"
        ),
        color=discord.Color(0x2c303d)
    )
    
    # banner
    embed.set_image(url="YOUR_BANNER_URL")
    
    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setjoinleave(ctx, channel: discord.TextChannel = None):
    """
    Set the channel for join/leave messages
    
    Parameters:
        ctx (Context): The command context
        channel (TextChannel): The channel to send messages to. If not provided, uses current channel.
    
    Usage:
        !setjoinleave #channel
        !setjoinleave  (uses current channel)
    """
    # If no channel provided, use current channel
    if channel is None:
        channel = ctx.channel
    
    # Store channel ID
    welcome_channels[ctx.guild.id] = channel.id
    
    await ctx.message.add_reaction('✅')
