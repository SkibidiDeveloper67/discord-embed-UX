# imports
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from discord.ui import View, Button
from typing import Set

# code

BANNER_URL = "YOUR_BANNER_URL"

class PollView(View):
    def __init__(self, duration: int):
        super().__init__(timeout=duration * 60)
        self.yes_votes: Set[int] = set()
        self.no_votes: Set[int] = set()
        self.message = None

    @discord.ui.button(label="   YES - 0% (0)   ", style=discord.ButtonStyle.secondary)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        await self.handle_vote(interaction, "yes")

    @discord.ui.button(label="   NO - 0% (0)   ", style=discord.ButtonStyle.secondary)
    async def no_button(self, interaction: discord.Interaction, button: Button):
        await self.handle_vote(interaction, "no")

    async def handle_vote(self, interaction: discord.Interaction, vote_type: str):
        user_id = interaction.user.id

        # Remove previous vote if exists
        self.yes_votes.discard(user_id)
        self.no_votes.discard(user_id)

        # vote
        if vote_type == "yes":
            self.yes_votes.add(user_id)
        else:
            self.no_votes.add(user_id)

        # Calculate 
        total_votes = len(self.yes_votes) + len(self.no_votes)
        yes_percentage = (len(self.yes_votes) / max(1, total_votes)) * 100
        no_percentage = (len(self.no_votes) / max(1, total_votes)) * 100

        # Update
        for child in self.children:
            if isinstance(child, Button):
                if child == self.yes_button:
                    child.label = f"   YES - {yes_percentage:.1f}% ({len(self.yes_votes)})   "
                elif child == self.no_button:
                    child.label = f"   NO - {no_percentage:.1f}% ({len(self.no_votes)})   "

        # Update 
        embed = self.message.embeds[0]

        # response 
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):

        for child in self.children:
            child.disabled = True

        total_votes = len(self.yes_votes) + len(self.no_votes)
        yes_percentage = (len(self.yes_votes) / max(1, total_votes)) * 100
        no_percentage = (len(self.no_votes) / max(1, total_votes)) * 100

        original_desc_lines = self.message.embeds[0].description.split('\n')
        original_question = next(line.split('`')[1] for line in original_desc_lines if '**Question**' in line)

        # Create result embed
        result_embed = discord.Embed(
            description=(
                f"## ```             Server - Poll Ended        ```\n"
                f"__**Poll Information**__\n"
                f"> * **Question**: `{original_question}`\n"
                f"> * **Total Votes**: `{total_votes}`\n\n"
                f"__**Final Results**__\n"
                f"> * **Yes Votes**: `{len(self.yes_votes)} ({yes_percentage:.1f}%)`\n"
                f"> * **No Votes**: `{len(self.no_votes)} ({no_percentage:.1f}%)`\n\n"
                f"__**Results**__\n"
                f"> * **{self.get_winner()}**"
            ),
            color=discord.Color(0x2c303d)
        )
        
        # Add banner
        result_embed.set_image(url=BANNER_URL)

        # Update
        await self.message.edit(embed=result_embed, view=self)
    
    def get_winner(self) -> str:
        """Determine the winner of the poll"""
        if len(self.yes_votes) > len(self.no_votes):
            return "`Yes` won! 🏆"
        elif len(self.no_votes) > len(self.yes_votes):
            return "`No` won! 🏆"
        else:
            return "It's a tie! 🤝"

@bot.event
async def on_ready():
    """Event triggered when bot is ready and connected to Discord"""
    print(f"Logged in as {bot.user}")
    print(f"Bot is ready to create polls!")

async def create_poll_embed(ctx, question: str, duration: int):
    """
    Creates a professional poll embed with buttons
    
    Parameters:
        ctx (Context): Discord context object
        question (str): The poll question
        duration (int): Duration in minutes
    """
    end_time = datetime.now() + timedelta(minutes=duration)
    
    embed = discord.Embed(
        description=(
            f"## ```            Server - Poll Started        ```\n"
            f"__**Poll Information**__\n"
            f"> * **Question**: `{question}`\n"
            f"> * **Duration**: `{duration} minutes`\n"
            f"> * **Ends**: <t:{int(end_time.timestamp())}:R>\n\n"
            f"__**How to Vote**__\n"
            f"> * Click the buttons below to vote!\n"
            f"> * You can change your vote at any time\n"
            f"> * Results update in real-time"
        ),
        color=discord.Color(0x2c303d)
    )
    
    # Add banner 
    embed.set_image(url=BANNER_URL)
    
    view = PollView(duration)
    
    # Send embed
    view.message = await ctx.send(embed=embed, view=view)

@bot.command()
async def poll(ctx, duration: int, *, question: str):
    """
    Creates a new Yes/No poll with buttons
    
    Parameters:
        ctx (Context): Discord context object
        duration (int): Duration in minutes
        question (str): The poll question
    
    Usage:
        !poll <minutes> <question>
        Example: !poll 60 Should we add more channels?
    """
    await create_poll_embed(ctx, question, duration)
