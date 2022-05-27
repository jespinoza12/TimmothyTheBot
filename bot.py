from ast import keyword
from cProfile import run
from pickle import TRUE
import socket,threading,random,os
from time import time
from typing import Counter
from unicodedata import name
from twitchio.ext import commands, eventsub

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
    global run
    async def event_message(self, message):
        if message.echo:
            return

        print(message.content)
        keywords = []
        my_file = open("badwords.txt", "r")
        keywords = my_file.read()

        if(message.content in keywords) : 
            message_id = message.tags['id']
            timeout = 120
            reason = "Automatic timeout from Bot due to message contained badword"
            await message.channel.send(f"Thats a badword {message.author.name} so your message has been deleted")
            await message.channel.send(f"/delete {message_id}")
            await message.channel.send(f"/timeout {message.author.name} {timeout} {reason}]")
        await self.handle_commands(message)


    #Says Hello back
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')


    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send(f'Questions: (!questions)' + '\n' + 'Hello: (!hello)' + '\n' + 'FlipCoin: (!FlipCoin)' + '\n' + 'Raffle: (!beginraffle)(for admins)' + '\n' + 'Enter Raffle!: (!enterRaffle)' 
        + '\n' + 'Vote Option A: (!voteA)' + '\n' + 'Vote Option B: (!voteB)' + '\n' + 'Help (!help)')


    @commands.command()
    async def questions(self, ctx: commands.Context):
        await ctx.send('How long have you been streaming? (!Long)' + '\n' +
                        "What's My Name? (!Name)" + '\n' + "How Old Am I? (!Age)" + '\n' + "Where Am I from? (!From)" + '\n' + "When Do I Stream? (!Stream)")

    @commands.command()
    async def poll(self, ctx: commands.Context):
        if (ctx.author.name == "fros7yfeet") :
            await ctx.send("https://strawpoll.com/polls/e6Z2e13P5gN")
        else :
            await ctx.send(f"/w {ctx.author.name} You do not have access to this command")
    
    @commands.command()
    async def FlipCoin(self, ctx: commands.Context):
        randomNum = random.randint(1,2)
        if (randomNum == 1) :
            await ctx.send(f"/w {ctx.author.name} Heads WINS!")
        else :
            await ctx.send(f"/w {ctx.author.name} Tails WINS!")

    @commands.command()
    async def Long(self, ctx: commands.Context):
        await ctx.send('I have been streaming for 2 years')

    @commands.command()
    async def Name(self, ctx: commands.Context):
        await ctx.send('Julian Winters')

    @commands.command()
    async def Age(self, ctx: commands.Context):
        await ctx.send('20')

    @commands.command()
    async def From(self, ctx: commands.Context):
        await ctx.send('I am from New York, Carliona')

    @commands.command()
    async def Stream(self, ctx: commands.Context):
        await ctx.send('I stream everyday at 4')

    @commands.command()
    async def beginraffle(self, ctx: commands.Context):
        print(ctx.author.name)
        if('fros7yfeet' == ctx.author.name):
            my_file1 = open("run.txt", "w")
            my_file1.write("True")
            await ctx.send('Entries for the raffle have started. Type !raffle  to join now!!')
        else:
            await ctx.send('You are not the Streamer')
    
    @commands.command()
    async def raffle(self, ctx: commands.Context):
            print(ctx.author.name)
            my_file1 = open("run.txt", "r")
            my_file3 = open("listForRaffle.txt", "r")
            
            if (my_file1.read() == "True"):
                if (ctx.author.name not in my_file3.read()) :
                    my_file1 = open("listForRaffle.txt", "a")
                    my_file1.write(f"{ctx.author.name} \n")
                    my_file1.close()
                    await ctx.send(f"{ctx.author.name} has entered the raffle!")
                else :
                    await ctx.send(f"/w {ctx.author.name} You have already entered this raffle!")
            else :
                await ctx.send("Raffle has not started")
    
    @commands.command()
    async def endraffle(self, ctx: commands.Context):
        print(ctx.author.name)
        my_file1 = open("run.txt", "r")
        if(my_file1.read() == "True"):
            if(ctx.author.name == "fros7yfeet"):
                my_file1 = open("listForRaffle.txt", "r")
                lines= my_file1.read().split("\n")
                my_file1.close()
                random_person = random.choice(lines)
                print(random_person)
                await ctx.send(f"{random_person} has won the raffle")
                with open("listForRaffle.txt", "w") as f:
                    f.write("")
                with open("run.txt", "w") as f:
                    f.write("False")
            else:
                await ctx.send("You are not the Streamer")
        else: 
            await ctx.send("Raffle has not started")

bot = Bot()
bot.run()
