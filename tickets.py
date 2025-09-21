# all imports required
import discord
from discord.ext import commands
from datetime import datetime
from discord import SelectOption
from discord.ui import Select, View

# code
async def create_ticket_embed(ctx, description: str, with_banner: bool = False):

    """
    Creates a professional ticket embed with user information and optional banner
    
    Parameters:
        ctx (Context): Discord context object containing message information
        description (str): Ticket description provided by the user
        with_banner (bool): Whether to include banner image in the embed
    
    Returns:
        None: Sends the embed directly to the channel
    """
    
    user = ctx.author
    member = ctx.guild.get_member(user.id)
    
    # Format dates
    time_format = "%d.%m.%Y %H:%M"
    joined_at = member.joined_at.strftime(time_format)
    created_at = user.created_at.strftime(time_format)
    current_time = datetime.now().strftime(time_format)
    
    # Set padding
    padding = "  " if with_banner else "      "
    
    # Create embed with ticket info
    embed = discord.Embed(
        description=(
            f"## ```{padding}Ticket - {user.name} | Category{padding}```\n"
            f"__**Information about user and ticket**__\n"
            f"> * **Username**: `{user.name}`\n"
            f"> * **User ID**: `{user.id}`\n"
            f"> * **Member Since**: `{joined_at}`\n"
            f"> * **Account Age**: `{created_at}`\n"
            f"__**Ticket description**__\n"
            f"> * **Description**: `{description}`"
        ),
        color=discord.Color(0x2c303d)
    )
    
    # Set bot avatar as thumbnail
    if bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)
    elif hasattr(bot.user, 'default_avatar'):
        embed.set_thumbnail(url=bot.user.default_avatar.url)
    
    # Get user's avatar for footer
    footer_icon = None
    if user.avatar:
        footer_icon = user.avatar.url
    elif hasattr(user, 'default_avatar'):
        footer_icon = user.default_avatar.url
    
    # Add footer 
    embed.set_footer(
        text=f"Ticket created by {user.name} | {current_time}",
        icon_url=footer_icon if footer_icon else None
    )
    
    # Add banner 
    if with_banner:
        embed.set_image(url="attachment://banner.png")
        file = discord.File("banner.png", filename="banner.png")
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send(embed=embed)

class CategorySelect(Select):
    def __init__(self):
        # ticket categories
        options = [
            SelectOption(
                label="Category 1",
                description="Description 1",
                value="cat1"
            ),
            SelectOption(
                label="Category 2",
                description="Description 2",
                value="cat2"
            ),
            SelectOption(
                label="Category 3",
                description="Description 3",
                value="cat3"
            ),
            SelectOption(
                label="Category 4",
                description="Description 4",
                value="cat4"
            )
        ]

        super().__init__(
            placeholder="Select ticket category...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """
        Handles the interaction when a category is selected
        Currently just shows a demo message (template showcase)
        
        Parameters:
            interaction (discord.Interaction): The interaction that triggered this callback
        """
        await interaction.response.send_message(
            f"This is a template showcase - Category selected: {self.values[0]}", 
            ephemeral=True
        )

class TicketView(View):
    """
    View containing the category selection dropdown
    Inherits from discord.ui.View
    """
    def __init__(self):
        super().__init__(timeout=None)  # View will not timeout
        self.add_item(CategorySelect())

# --- commands

@bot.command()
async def ticketpanel(ctx):
    """Create a ticket panel with category selection"""
    embed = discord.Embed(
        description=(
            f"## ```           Server - Ticket System        ```\n"
            f"> * If you have an issue related to **Category 1**, please open a ticket there. Our team will respond as soon as possible.\n\n"
            f"> * If your problem fits under **Category 2**, feel free to create a ticket in that section. We’ll be glad to help!\n\n"
            f"> * For anything that belongs to **Category 3**, please use the corresponding ticket option. Support will reach out to you shortly.\n\n"
            f"> * If your request matches **Category 4**, select that option to create a ticket and we’ll assist you soon.\n"
        ),
        color=discord.Color(0x2c303d)
    )
    
    # Add banner 
    embed.set_image(url="attachment://banner.png")
    
    file = discord.File("banner.png", filename="banner.png")
    await ctx.send(file=file, embed=embed, view=TicketView())

@bot.command()
async def embed(ctx, *, description: str = "No description"):
    """Create a ticket embed without banner"""
    await create_ticket_embed(ctx, description)

@bot.command()
async def embedbanner(ctx, *, description: str = "No description"):
    """Create a ticket embed with banner"""
    await create_ticket_embed(ctx, description, with_banner=True)
