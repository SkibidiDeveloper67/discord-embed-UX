# impots
import discord
from discord.ext import commands
from typing import Dict

# code
boost_channels: Dict[int, int] = {}

@bot.event
async def on_guild_update(before, after):
    """Event triggered when a guild is updated (including boosts)"""
    if before.premium_subscription_count < after.premium_subscription_count:
        if after.id not in boost_channels:
            return
            
        channel = after.get_channel(boost_channels[after.id])
        if not channel:
            return
            
        async for entry in after.audit_logs(action=discord.AuditLogAction.guild_update, limit=1):
            booster = entry.user
            if not booster:
                return
                
            await send_boost_embed(channel, booster, after)

async def send_boost_embed(channel, booster, guild):
    """Sends a boost notification embed"""
    
    # embed
    embed = discord.Embed(
        description=(
            f"## ```              Server Boosted!        ```\n"
            f"__**Thank you for boosting {guild.name}!**__\n"
            f"> * {booster.mention} just boosted the server! 🚀\n"
            f"> * We now have `{guild.premium_subscription_count}` boosts!\n"
            f"> * Current Server Level: `{guild.premium_tier}`\n"
        ),
        color=0xf47fff 
    )

    embed.set_image(url="YOUR_BANNER_URL")
    
    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setboost(ctx, channel: discord.TextChannel = None):
    """
    Set the channel for boost notifications
    
    Parameters:
        ctx (Context): The command context
        channel (TextChannel): The channel to send messages to. If not provided, uses current channel.
    
    Usage:
        !setboost #boost-logs
        !setboost  (uses current channel)
    """
    if channel is None:
        channel = ctx.channel
    
      boost_channels[ctx.guild.id] = channel.id
    
    await ctx.message.add_reaction('✅')

@bot.command()
@commands.has_permissions(administrator=True)
async def boost(ctx):
    """
    Test command to simulate a boost notification
    This command will be removed in production
    
    Usage:
        !boost
    """
    await send_boost_embed(ctx.channel, ctx.author, ctx.guild)
