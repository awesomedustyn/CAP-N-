import discord
from discord.ext import commands


class FunCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command() 
  async def ping(self, ctx):
    await ctx.send("pong")


  @commands.Cog.listener()
  async def on_ready(self):
    print("Fun Commands Are Ready!")






def setup(bot):
  bot.add_cog(FunCommands(bot))
