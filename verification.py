"""
Discord Verification System
--------------------------
A modern verification system with button interaction and role assignment.
"""
# imports
import discord
from discord.ext import commands
from discord.ui import View, Button
from typing import Dict

# Code
BANNER_URL = "YOUR_BANNER_URL"

verification_settings: Dict[int, dict] = {}

class VerificationButton(View):
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(
        label="Verify",
        style=discord.ButtonStyle.secondary,
        custom_id="verify_button"
    )
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        guild_settings = verification_settings.get(interaction.guild.id)
        if not guild_settings:
            await interaction.response.send_message("Verification system is not set up properly.", ephemeral=True)
            return

        role = interaction.guild.get_role(guild_settings['role_id'])
        if not role:
            await interaction.response.send_message("Verification role not found. Please contact an administrator.", ephemeral=True)
            return

        # Check
        if role in interaction.user.roles:
            await interaction.response.send_message("You are already verified!", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(role, reason="User verification")
            
            # Create embed
            embed = discord.Embed(
                description=(
                    f"## ```            Verification Successful        ```\n"
                    f"__**Welcome {interaction.user.name}!**__\n"
                    f"> * You now have access to the server\n"
                    f"> * Role Added: {role.mention}\n"
                    f"> * Enjoy your stay!"
                ),
                color=discord.Color(0x2c303d)  
            )
            
            embed.set_image(url=BANNER_URL)
            
            # success message
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # logs 
    
            if 'log_channel_id' in guild_settings:
                log_channel = interaction.guild.get_channel(guild_settings['log_channel_id'])
                if log_channel:
                    log_embed = discord.Embed(
                        description=(
                            f"## ```          New Verification        ```\n"
                            f"__**User Information**__\n"
                            f"> * **User**: {interaction.user.mention}\n"
                            f"> * **ID**: `{interaction.user.id}`\n"
                            f"> * **Account Created**: <t:{int(interaction.user.created_at.timestamp())}:R>"
                        ),
                        color=discord.Color(0x2c303d)
                    )
                    # Set user's avatar as thumbnail instead of banner
                    log_embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    log_embed.set_footer(text=f"Verification Log | {interaction.guild.name}")
                    await log_channel.send(embed=log_embed)

        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to give you the verified role. Please contact an administrator.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred during verification. Please try again later.",
                ephemeral=True
            )

@bot.command()
@commands.has_permissions(administrator=True)
async def setupverify(ctx, role: discord.Role, log_channel: discord.TextChannel = None):
    """
    Set up the verification system
    
    Parameters:
        ctx (Context): The command context
        role (Role): The role to give to verified users
        log_channel (TextChannel, optional): Channel to log verifications
    
    Usage:
        !setupverify @Verified #verification-logs
        !setupverify @Verified
    """
    # store settings
    verification_settings[ctx.guild.id] = {
        'role_id': role.id,
        'log_channel_id': log_channel.id if log_channel else None
    }
    
    # create embed
    embed = discord.Embed(
        description=(
            f"## ```            Server Verification        ```\n"
            f"__**Welcome to {ctx.guild.name}!**__\n"
            f"> * Click the button below to verify\n"
            f"> * You will receive the {role.mention} role\n"
            f"> * This will give you access to the server\n\n"
            f"__**Rules Reminder**__\n"
            f"> * By verifying, you agree to follow our rules\n"
            f"> * Be respectful to all members\n"
            f"> * Have fun and enjoy your stay!"
        ),
        color=discord.Color(0x2c303d)
    )
    
    embed.set_image(url=BANNER_URL)
    
    # Create view with verification button
    view = VerificationButton()
    
    # Send public verification message with buttons
    verification_message = await ctx.send(embed=embed, view=view)

@bot.event
async def on_ready():
    bot.add_view(VerificationButton())
