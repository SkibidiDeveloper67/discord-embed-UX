# imports
import discord
from discord.ext import commands
from datetime import datetime

# code
# id of logs channel
invite_logs_channel_id = 1420139058029658113

bot = commands.Bot(command_prefix="!", intents=intents)

# store invites data (reset on bot restart)
# note: if you want to persist invite data across restarts, consider using a database
invite_counts = {}
total_invite_counts = {}
cached_invites = {}

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    # cache all guild invites on startup
    for guild in bot.guilds:
        cached_invites[guild.id] = await guild.invites()

async def create_invite_embed(guild, member, inviter=None, left=False):
    """
    creates professional invite tracking embed
    
    parameters:
        guild: discord guild object
        member: member who joined/left
        inviter: member who invited (none if left=True)
        left: whether member left the server
    """
    
    # prepare invite counts for display
    if inviter:
        current = invite_counts.get(inviter.id, 0)
    
    embed = discord.Embed(
        description=(
            f"## ```           {guild.name} - Invite System      ```\n" # remember to adjust the width of the padding to match your server name length
        ),
        color=discord.Color(0x2c303d)
    )

    if left:
        embed.description += f"> User **{member.name}** left the server"
    elif inviter:
        member_count = len(guild.members)
        embed.description += f"> User **{member.name}** joined from **{inviter.name}**'s invite, they're the `{member_count}`th member and **{inviter.name}** has `{current}` active invites"
    else:
        embed.description += f"> User **{member.name}** joined the server"

    # set banner
    embed.set_image(url="attachment://banner.png")

    return embed

@bot.event
async def on_member_join(member):
    """handle new member joins and track invites"""
    guild = member.guild
    
    # fetch new invite list
    new_invites = await guild.invites()
    
    # find used invite by comparing with cached invites
    used_invite = None
    inviter = None
    
    for invite in new_invites:
        # find matching cached invite
        cached_invite = next(
            (inv for inv in cached_invites[guild.id] if inv.code == invite.code),
            None
        )
        
        if cached_invite and invite.uses > cached_invite.uses:
            used_invite = invite
            inviter = invite.inviter
            break
    
    if inviter:
        # update invite counts
        invite_counts[inviter.id] = invite_counts.get(inviter.id, 0) + 1
        total_invite_counts[inviter.id] = total_invite_counts.get(inviter.id, 0) + 1
    
    # update cached invites
    cached_invites[guild.id] = new_invites
    
    # create and send embed
    embed = await create_invite_embed(guild, member, inviter)
    
    # get logs channel
    channel = guild.get_channel(invite_logs_channel_id)
    
    if channel and channel.permissions_for(guild.me).send_messages:
        file = discord.File("banner.png", filename="banner.png")
        await channel.send(file=file, embed=embed)

@bot.event
async def on_member_remove(member):
    """handle member leaves"""
    guild = member.guild
    
    # decrease current invite count for inviter if found
    for invite in cached_invites.get(guild.id, []):
        if invite.inviter and member in guild.members:
            invite_counts[invite.inviter.id] = max(0, invite_counts.get(invite.inviter.id, 0) - 1)
    
    # create and send embed
    embed = await create_invite_embed(guild, member, left=True)
    
    # get logs channel
    channel = guild.get_channel(invite_logs_channel_id)
    
    if channel and channel.permissions_for(guild.me).send_messages:
        file = discord.File("banner.png", filename="banner.png")
        await channel.send(file=file, embed=embed)

@bot.command()
async def invites(ctx, member: discord.Member = None):
    """show invite counts for a member"""
    member = member or ctx.author
    total = total_invite_counts.get(member.id, 0)
    current = invite_counts.get(member.id, 0)
    
    embed = discord.Embed(
        description=(
            f"## ```           {ctx.guild.name} - Invite System      ```\n" # remember to adjust the width of the padding to match your server name length
            f"> User **{member.name}** has `{current}` active invites and `{total}` total invites"
        ),
        color=discord.Color(0x2c303d)
    )
    # use banner link or file
    embed.set_image(url="YOUR_BANNER_URL")
    file = discord.File("banner.png", filename="banner.png") 
    await ctx.send(file=file, embed=embed)
