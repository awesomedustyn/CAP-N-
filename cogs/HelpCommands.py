import discord
from discord.ext import commands


class HelpCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(invoke_without_command = True)
  async def info(self, ctx):
      embed=discord.Embed(title="Aye Aye Cap'n!", description="Here are all my commands!")
      embed.add_field(name="Moderation Commands!", value="N/A", inline=True)
      embed.add_field(name="Fun Commands!", value="N/A", inline=True)
      embed.add_field(name="Valorant Commands!", value="N/A", inline=True)
      await ctx.send(embed=embed)


  @commands.Cog.listener()
  async def on_ready(self):
    print("Help Commands Are Ready!")




def setup(bot):
  bot.add_cog(HelpCommands(bot))
