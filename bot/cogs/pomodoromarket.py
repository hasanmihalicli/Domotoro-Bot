import discord
from discord.ext import commands
import random
from asset import liste
import random
from datetime import datetime, timedelta 
from pomodorostats import pomodorostat 
import json



class pomodoromarket(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    #MARKET
    @commands.command()
    async def market(self,ctx):
      myembed = discord.Embed(title = "Welcome to pomodoro Market", color=0xff0000)
      with open("stats/items.json","r") as f:
          items = json.load(f) # load items
      for i in items.keys():
        myembed.add_field(name = i,value=f"💸  {items[i]['money']}  `` !buy {i} ``") # items
      await ctx.send(embed=myembed)
     

    #BUY item 
    @commands.command()
    async def buy(self,ctx,item):
        with open("stats/items.json","r") as f:
          items = json.load(f) # load items
        for i in items.keys():
          if i != item:
            await ctx.send("There is no such item") # there is no such item MESSAGE
            return
          else:
            money = pomodorostat.get_key(ctx.author,'money') #get money
            if items[i]["money"] > money:
              myembed = discord.Embed(title = "you don't have enough money", color=0xff0000) # you don't have enough money MESSAGE
              await ctx.send(embed=myembed) 
              return
            else:
              print(f"Buy item   item Name : {i}  item Money : {items[i]['money']}") 
             
              
        # Add item
        with open("stats/pomodorouser.json","r") as f:
          users = json.load(f)

          await pomodorostat.update_data(users,ctx.author) # update data 
          await pomodorostat.add_item(users,ctx.author,1,item) # add item to envanter
          await pomodorostat.reduce_money(users,ctx.author,items[i]["money"]) # reduce money

        with open("stats/pomodorouser.json","w") as f:
          json.dump(users,f,indent=4) # save data
        # End


        myembed = discord.Embed(title = f"successfully purchased. for use. ``!use {item}``", color=0xff0000) # successfully purchased message
        await ctx.send(embed=myembed)




    #USE item
    @commands.command()
    async def use(self,ctx,item):
      with open("stats/items.json","r") as f:
          items = json.load(f) 
          for i in items.keys():
            if i != item:
              await ctx.send("There is no such item") #There is no such item MESSAGE
              return
      
      item_count = pomodorostat.get_item(ctx.author,item)
      if item_count <= 0:
        myembed = discord.Embed(title = "not enough items ``!market``", color=0xff0000) # not enough items MESSAGE
        await ctx.send(embed=myembed)
        return
      else:
        #start
        with open("stats/pomodorouser.json","r") as f:
          users = json.load(f)


        await pomodorostat.update_data(users,ctx.author) #update item
        await pomodorostat.reduce_item(users,ctx.author,1,item) # reduce item
          


        with open("stats/pomodorouser.json","w") as f:
          json.dump(users,f,indent=4) # save data
        # End


        #word item 
        if item == "word":
          myembed = discord.Embed(title = f"{random.choice(liste.DomotoroQuotes)}", color=0xff0000)
          await ctx.send(embed=myembed)
          return
        


def setup(bot):
	bot.add_cog(pomodoromarket(bot))