import discord, datetime, time
from discord.ext import commands, tasks
from itertools import cycle

start_time = time.time()

class Events(commands.Cog):
  def __init__(self, client):
        self.client = client
        self.status = cycle(['Bind', 'Haven', 'Ascent','Split','Fracture'])
        

  @tasks.loop(seconds=10.0)
  async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))
        
  @commands.Cog.listener()
  async def on_ready(self):
        await self.client.wait_until_ready()
        self.change_status.start()
        print("Event Commands Are Ready!")

  @commands.command(pass_context=True)
  async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
      



def setup(bot):
  bot.add_cog(Events(bot))
