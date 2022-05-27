import socket,threading,random,os
from time import time
from twitchio.ext import commands, eventsub

class Bot(commands.Bot):
    run = False;
    
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)
        keywords = []
        my_file = open("badwords.txt", "r")
        keywords = my_file.read()

        #Checks for specific words and deletes it and times user out
        if(message.content in keywords) : 
            message_id = message.tags['id']
            timeout = 120
            reason = "Automatic timeout from Bot due to message contained badword"
            await message.channel.send(f"Thats a badword {message.author.name} so your message has been deleted")
            await message.channel.send(f"/delete {message_id}")
            await message.channel.send(f"/timeout {message.author.name} {timeout} {reason}]")

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)


    #Says Hello back
    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
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

    @commands.command(name = 'beginraffle')
    async def beginraffle(self, ctx: commands.Context, message):
        if('impishvictor24' == {message.author.name}):
            await ctx.send('Entries for the raffle have started. Type !raffle  to join now!!')
            run = True;
        else:
            await ctx.send('You are not the Streamer')
    
    @commands.command(name = 'raffle')
    async def beginraffle(self, ctx: commands.Context, message):
        if(run == True):
            print(message.content)
            keywords = []
            my_file2 = open("listForRaffle.txt", "r")
            keywords = my_file2.read()
            my_file2.append(message.author.name + '\n')
            await ctx.send('{message.author.name} has entered the raffle!')
        else:
            await ctx.send('The Raffle has not started')
    
    @commands.command(name = 'runraffle')
    async def beginraffle(self, ctx: commands.Context, message):
        if(run == True):
            if('impishvictor24' == {message.author.name}):
                random_people = random.choice(my_file2)
                await ctx.send('{random_people} has won the raffle')
                run = False;
        else:
            await ctx.send('You are not the Streamer')

bot = Bot()
bot.run()
