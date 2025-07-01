import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import unicodedata

load_dotenv()
API_KEY = os.getenv("API_KEY")

class Client(commands.Bot):
    async def on_ready(self):
        print(f"logged on as {self.user}")
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content != unicodedata.normalize('NFKC', message.content):
            await message.delete()
            await message.channel.send(f"**{message.author.display_name}** (<@{message.author.id}>) said\n{unicodedata.normalize('NFKC', message.content)}")

intents = discord.Intents.all()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

@client.tree.command(name="removefont", description="remove fonts a single users nickname")
async def removefontuser(interaction: discord.Interaction, user: discord.Member):
    try:
        await user.edit(nick=unicodedata.normalize('NFKC', user.display_name))
        await interaction.response.send_message(f"removed font from {user.display_name}'s (<@{user.id}>) nickname.")
    except discord.Forbidden:
        await interaction.response.send_message(f"couldnt change nickname because {user.display_name}'s role is higher than the bots role.")
    except Exception as e:
        await interaction.response.send_message(f"error: {e}\nplease send this to lovescults on discord.")

@client.tree.command(name="removefontall", description="remove fonts from every users nickname")
async def removefontall(interaction: discord.Interaction):
        guild = interaction.guild
        for member in guild.members:
            if member.display_name != unicodedata.normalize('NFKC', member.display_name):
                try:
                    await member.edit(nick=unicodedata.normalize('NFKC', member.display_name))
                except discord.Forbidden:
                    pass
        await interaction.response.send_message("done. if any users still have fonts in their name, it is likely that their role is higher than the bots role.")

client.run(API_KEY)