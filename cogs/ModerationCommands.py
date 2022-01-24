from discord.ext import commands

class ModerationCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  

  @commands.Cog.listener()
  async def on_ready(self):
    print("Moderation Commands Are WIP!")




def setup(bot):
  bot.add_cog(ModerationCommands(bot))
