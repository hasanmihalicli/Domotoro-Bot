#imports
import os
import asyncio
import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta 
from asset import liste #Domotoro's Quotes
from pomodorostats import pomodorostat 
import json


#get conf.json file
with open('conf.json',"r") as conf:
  conf = json.load(conf)



#bot_varible
bot = commands.Bot(command_prefix=conf["PREFIX"],description="Pomodoro Bot",sort_commands=False)
bot.author_id = conf["AUTHOR"] 
stat_source = "stats/pomodorouser.json"
#---------------------------------------



#help command-----------------------------------
class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=0xff0000)
            await destination.send(embed=emby)
bot.help_command = NewHelpName()
#END---------------------------------------------





#on_ready EVENT
@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in") 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Studying")) # active bot presence
    print(bot.user)  # Prints the bot's username and identifier





#on_message EVENT
@bot.event
async def on_message(message):
  if message.author.bot:
    return
  if not message.guild:
    return
 
  with open(stat_source,"r") as f:
    users = json.load(f)

  await pomodorostat.update_data(users,message.author) # update data
  await pomodorostat.add_money(users,message.author,1) # add pomodoro point
 
  with open(stat_source,"w") as f:
    json.dump(users,f,indent=4)

  await bot.process_commands(message)





#Pomodoro count command
@bot.command(aliases=["ps","ds","envanter"])
async def pomodorostats(ctx):
  myembed = discord.Embed(title=f"You have worked a total of ``{pomodorostat.get_key(ctx.author,'Pomodoro_Count')}`` pomodoros with this bot.")
  money = pomodorostat.get_key(ctx.author,"money")
  myembed.add_field(name = "Money" , value = f"{money}",inline = False)
  myembed.add_field(name = "Word" , value = f"{pomodorostat.get_item(ctx.author,'word')}")
  await ctx.send(embed=myembed)



  
#Pomodoro commands
@bot.command(aliases=["p","domotoro",'dt'],pass_context=True)
async def pomodoro(ctx,Time:int):

        if Time > 60:
          await ctx.send("You're work very few hours 😑")
          return
        elif Time < 5:
          await ctx.send("You work too little 😑")
          return


        #VARIBLES--------------------------------
        start_time = datetime.now()  # start lesson time
        start_time_text = start_time.strftime("%H : %M") # start lesson time text
        end_time = datetime.now() + timedelta(minutes=Time)  # end lesson time
        end_time_text = end_time.strftime("%H : %M") # en lesson time text
        word_day = random.choice(liste.DomotoroQuotes) # randomly choosing a sentence
        break_time = 300  # Break Time with seconds
        lesseon_time = Time * 60  # lesson_time with seconds
        #-----------------------------------------


        myembed = discord.Embed(title="Click reaction to start pomodoro.",color=random.randint(0, 0xffffff)) # pomodoro start message
        myembed.add_field(name="Start Time", value=f"{start_time_text}") # start time
        myembed.add_field(name="End Time", value=f"{end_time_text}") # end time
        myembed.add_field(name="Domotoro's Quotes", value=f"{word_day}",inline=False) # word of the day
        myembed.add_field(name="Pomodoro started by", value=f"{ctx.author.mention}",inline=False) # pomodoro owner

        msg = await ctx.send(embed=myembed) # send pomodoro message



        await msg.add_reaction('✅') #add reaction
        
    
        #reaction check function
        def check_start(reaction, user):
          return user == ctx.author and str(reaction.emoji) == '✅'
        try:
          reaction, user = await bot.wait_for('reaction_add',timeout=20.0, check=check_start) #wait reaction add
        except:
          await msg.delete()
          #timeout error message
          await ctx.send(f"{ctx.author.mention} The pomodoro launch has been canceled because the pomodoro launch timer has expired") 
          return

        await msg.remove_reaction('✅', ctx.author) # remove reaction user
        await msg.remove_reaction('✅', bot.user) # remove reaction bot

        #check pomodoro count
        if pomodorostat.get_key(ctx.author,"pomodoro_message_id") != None:
          await msg.delete()
          await ctx.send("You already started 1 pomodoro.") 
          return


        # Add stat
        with open(stat_source,"r") as f:
          users = json.load(f)

        await pomodorostat.update_data(users,ctx.author) # update user data
        await pomodorostat.set_key(users,ctx.author,'pomodoro_message_id',msg.id)  # set message ID

        with open(stat_source,"w") as f:
          json.dump(users,f,indent=4)
        # End
        




        #start timer
        while lesseon_time != 0:

            minutes = (lesseon_time % 3600) // 60  #lesson min
            seconds = lesseon_time % 60 #lesson sec
          
 
            newmyembed = discord.Embed(title="Pomodoro Started!",description=f" Remaining Time = {minutes} : {seconds}",color=random.randint(0, 0xffffff)) #Pomodoro started message
            newmyembed.add_field(name="Domotoro's Quotes",value=f"{word_day}") # Domotoro's Quotes
            newmyembed.add_field(name="Pomodoro started by", value=f"{ctx.author.mention}",inline=False) # pomodoro owner
            await msg.edit(embed=newmyembed)  



            lesseon_time -= 1 
            await asyncio.sleep(1)  # Waiting time


        newmyembed = discord.Embed(title="Lesson time ended!", color=random.randint(0, 0xffffff))
        await msg.edit(embed=newmyembed)  # Lesson ended message
        await asyncio.sleep(2) # lesson sleep

        start_time_lesson = datetime.now()  # start lesson time
        start_time_lesson_text = start_time_lesson.strftime("%H : %M")
        end_time_break = datetime.now() + timedelta(minutes=break_time / 60) # End Break time 
        end_time_break_text = end_time_break.strftime("%H : %M")


        newmyembed = discord.Embed(title="Break Time started!",color=random.randint(0, 0xffffff)) #Break started message
        newmyembed.add_field(name="Start Time", value=f"{start_time_lesson_text}") # start break time
        newmyembed.add_field(name="End Time", value=f"{end_time_break_text}") # end break time
 
                                  
        await msg.edit(embed=newmyembed)
        await asyncio.sleep(3) #break sleep





        #Start brek timer
        while break_time != 0:


            minutes = (break_time % 3600) // 60 # break min
            seconds = break_time % 60 # break sec


            newmyembed = discord.Embed(title=f"Break Time!",description=f"Remaining Time = {minutes} : {seconds}", color=random.randint(0, 0xffffff)) #break time message
            newmyembed.add_field(name="Domotoro's Quotes",value=f"{word_day}") # Tomodoro's Quotes
            newmyembed.add_field(name="Pomodoro started by", value=f"{ctx.author.mention}",inline=False)  # pomodoro owner
            await msg.edit(embed=newmyembed)  # break edit message


            break_time -= 1
            await asyncio.sleep(1)


        newmyembed = discord.Embed(title="Break Ended!",color=random.randint(0, 0xffffff)) # break ended message
        await msg.edit(embed=newmyembed)  
        await asyncio.sleep(2)
        newmyembed = discord.Embed(title="Pomodoro is ended. Use !p command to start a pomodoro.",color=random.randint(0, 0xffffff)) # break ended message
        await msg.edit(embed=newmyembed)
        await asyncio.sleep(2)
        
        # Add stat
        with open(stat_source,"r") as f:
          users = json.load(f)

        await pomodorostat.add_xp(users,ctx.author,1) # set pomodoro point
        await pomodorostat.set_key(users,ctx.author,'pomodoro_message_id',None)
        await pomodorostat.add_money(users,ctx.author,100) #add money
  
        with open(stat_source,"w") as f:
          json.dump(users,f,indent=4)
        # End------------
        return






@bot.command()
async def stop(ctx):
  msg_id = pomodorostat.get_key(ctx.author,"pomodoro_message_id") #get message id
  if msg_id != None:
    msg = await ctx.fetch_message(msg_id) # get messsage by id
    await msg.delete() # delete message
    await ctx.send("Pomodoro has been successfully canceled.") # stop pomodoro message
    #start
    with open(stat_source,"r") as f:
      users = json.load(f) 

    await pomodorostat.set_key(users,ctx.author,'pomodoro_message_id',None)  # set message ID

    with open(stat_source,"w") as f:
      json.dump(users,f,indent=4)
    #END
  else:
    print("There is not any pomodoro to stop.")
    return

        


   
#ERROR commands
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.channel.send(f"**``Type {ctx.prefix}help to see correct version of command.``**")
    if isinstance(error,commands.CommandNotFound):
        await ctx.channel.send(f"**``There is no such commmand type {ctx.prefix}help to see correct version of command .``**")
    if isinstance(error,commands.CheckFailure):
        await ctx.channel.send(f"**``You are not authorized to use this command.``**")
    else:
      print(error)




extensions = [
  'cogs.pomodoromarket',

  #Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.



# Starts the bot

bot.run(conf["DISCORD_TOKEN"])  