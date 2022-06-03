import random,os
from twitchio.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])    

    async def event_message(self, message):
        if message.echo:
            return 
        
        print(message.content)
        keywords = []
        message1 = message.content.split("!")
        message_lower = "!" + message1[1].lower()
        message.content = message_lower
        print(message_lower)
        my_file = open("txt/badwords.txt", "r")
        keywords = my_file.read()
        if(message.content in keywords) : 
            message_id = message.tags['id']
            timeout = 120
            reason = "Automatic timeout from Bot due to message contained badword"
            if (message.author.name == 'fros7yfeet'):
                await message.channel.send(f"Thats a badword {message.author.name} so your message has been deleted")
            else:
                await message.channel.send(f"/w {message.author.name} Thats a badword so your message has been deleted")
            await message.channel.send(f"/delete {message_id}")
            await message.channel.send(f"/timeout {message.author.name} {timeout} {reason}]")
        await self.handle_commands(message)
    #Says Hello back
    @commands.command()
    async def hello(self, ctx: commands.Context):
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send(f'Hello {ctx.author.name}!')
            await ctx.channel.send(f"/delete {ctx.message.id}")
        else:
            await ctx.channel.send(f"/w {ctx.author.name} Hello")
            await ctx.channel.send(f"/delete {ctx.message.id}")
    #Help Menu
    @commands.command()
    async def help(self, ctx: commands.Context):
        prompt ="(!questions), (!hello), (!flipcoin), (!beginraffle)(Admin), (!endpoll)(Admin), Create Poll(Admin): (!poll How-are-you-today? good bad), (!help), !opensong(Admin), !requestsong: (!requestsong mr-brightside the-killers) !endrequests(Admin)"
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send(f'(!questions),' + ' (!hello),' + ' (!flipcoin),' + ' (!beginraffle)(Admin),'
            + " (!endpoll)(Admin),"  + ' Create Poll(Admin): (!poll How-are-you-today? good bad),' + 
            ' (!help),' + ' !opensong(Admin),' + " !requestsong: (!requestsong mr-brightside the-killers)," + "!endrequests(Admin)") 
        else:
            await ctx.channel.send(f"/w {ctx.author.name} {prompt}")

    #List of frequently asked questions
    @commands.command()
    async def questions(self, ctx: commands.Context):
        prompt = "How long have you been streaming?(!Long), What's My Name? (!name), How Old Am I? (!age), Where Am I from? (!home), When Do I Stream? (!stream)"
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send('How long have you been streaming? (!Long)' +
                    "What's My Name? (!name)" + "How Old Am I? (!age)" + "Where Am I from? (!home)" + "When Do I Stream? (!stream)")
        else:
            await ctx.channel.send(f"/w {ctx.author.name} {prompt}")
            
    #Flip Coin
    @commands.command()
    async def flipcoin(self, ctx: commands.Context):
        randomNum = random.randint(1,2)
        await ctx.channel.send(f"/delete {ctx.message.id}")
        if (randomNum == 1) :
            if (ctx.author.name == 'fros7yfeet'):
                await ctx.send(f"{ctx.author.name} Heads WINS!")
            else:
                await ctx.channel.send(f"/w {ctx.author.name} Heads WINS!")
        else :
            if (ctx.author.name == 'fros7yfeet'):
                await ctx.send(f"{ctx.author.name} Tails WINS!")
            else:
                await ctx.channel.send(f"/w {ctx.author.name} Tails WINS!")
            
    #Question
    @commands.command()
    async def long(self, ctx: commands.Context):
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send('I have been streaming for 2 years')
        else:
            await ctx.send(f"/w {ctx.author.name} I have been streaming for 2 years")
    #Question
    @commands.command()
    async def name(self, ctx: commands.Context):
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send('Julian Winters')
        else:
            await ctx.channel.send(f"/w {ctx.author.name} Julian Winters")
    #Question
    @commands.command()
    async def age(self, ctx: commands.Context):
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send('20')
        else:
            await ctx.channel.send(f"/w {ctx.author.name} 20")
    #Question
    @commands.command()
    async def home(self, ctx: commands.Context):
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send('I am from New York, Carliona')
        else:
            await ctx.channel.send(f"/w {ctx.author.name} I am from New York, Carliona")
        
    #Question
    @commands.command()
    async def stream(self, ctx: commands.Context):
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send('I stream everyday at 4')
        else:
            await ctx.channel.send(f"/w {ctx.author.name} I stream everyday at 4")
    #Create Poll
    @commands.command()
    async def poll(self, ctx: commands.Context):
        my_file1 = open("txt/pollstart.txt", "r")
        admins = open("txt/admins.txt", "r")
        try:
            if (my_file1.read() == "False"):
                if (ctx.author.name in admins.read()) :
                    message = ctx.message.content.split(" ")
                    question = message[1].replace("-", " ")
                    option1 = message[2]
                    option2 = message[3]
                    my_file1 = open("txt/pollstart.txt", "w")
                    my_file1.write("True")
                    await ctx.send(f"Poll has started!!! \n The question is {question} \n !vote A for {option1} \n !vote B for {option2}")
                    await ctx.channel.send(f"/delete {ctx.message.id}")
                else :
                    await ctx.channel.send(f"/w {ctx.author.name} You do not have access to this command")
                    await ctx.channel.send(f"/delete {ctx.message.id}")
            else:
                await ctx.channel.send(f"There is already an open Poll")
                await ctx.channel.send(f"/delete {ctx.message.id}")
        except:
            await ctx.send("Try Again but replace the spaces with - or Only limit yourself to two options or There was a typo")
    #Voting
    @commands.command()
    async def vote(self, ctx: commands.Context):
        my_file1 = open("txt/pollstart.txt", "r")
        my_file2 = open("txt/voted.txt", "r")
        message = ctx.message.content.split(" ")
        vote = message[1].lower()
        if (ctx.author.name == 'fros7yfeet'):
            await ctx.send("You cant vote on your own poll silly")
        else:
            if (my_file1.read() == "True"):
                if (vote == 'a') or (vote == 'b'):
                    if (ctx.author.name not in my_file2.read()) :
                        message = ctx.message.content.split(" ")
                        vote = message[1].lower()
                        my_file3 = open("txt/voted.txt", "a")
                        my_file4 = open("txt/votes.txt", "a")
                        my_file3.write(f"{ctx.author.name} \n")
                        my_file4.write(f"{vote}")
                        await ctx.send(f"{ctx.author.name} has voted!")
                        await ctx.channel.send(f"/delete {ctx.message.id}")
                    else:
                        await ctx.channel.send(f"/w {ctx.author.name} You have already voted!")
                        await ctx.channel.send(f"/delete {ctx.message.id}")
                else: 
                    await ctx.channel.send(f"/w {ctx.author.name} You cannot vote anything but A and B")
                    await ctx.channel.send(f"/delete {ctx.message.id}")
            else:
                await ctx.channel.send(f"/w {ctx.author.name} No poll started come back later")
                await ctx.channel.send(f"/delete {ctx.message.id}")
    #End Poll
    @commands.command()
    async def pollend(self, ctx: commands.Context): 
        running = open("txt/pollstart.txt", "r")
        file1 = open("txt/votes.txt")
        admins = open("txt/admins.txt", "r")
        if(running.read() == "True"):
            if(ctx.author.name in admins.read()):
                aVoteCount = file1.read().count("a")
                bVoteCount = file1.read().count("b")
                await ctx.send(f"Option A has {aVoteCount} and Option B has {bVoteCount}")

                if (aVoteCount > bVoteCount):
                    await ctx.send("Option A has WON!")
                if (aVoteCount == bVoteCount):
                    await ctx.send("Its a TIE!!!")
                if (aVoteCount < bVoteCount):
                    await ctx.send("Option B has WON!")
                with open("txt/voted.txt", "w") as f:
                    f.write("")
                with open("txt/votes.txt", "w") as f:
                    f.write("")
                with open("txt/pollstart.txt", "w") as f:
                    f.write("False")

                await ctx.channel.send(f"/delete {ctx.message.id} ")
            else:
                await ctx.send("You are not the Streamer")
                await ctx.channel.send(f"/delete {ctx.message.id} ")
        else: 
            await ctx.send("Raffle has not started")
            await ctx.channel.send(f"/delete {ctx.message.id} ")
    
    #open song requests
    @commands.command()
    async def opensong(self, ctx: commands.Context):
        my_file1 = open("txt/requestStart.txt", "r")
        admins = open("txt/admins.txt", "r")
        try:
            if (my_file1.read() == "False"):
                if (ctx.author.name in admins.read()) :
                    my_file1 = open("txt/requestStart.txt", "w")
                    my_file1.write("True")
                    await ctx.send(f"Song Requests are now open, one request per person")
                    await ctx.channel.send(f"/delete {ctx.message.id}")
                else :
                    await ctx.channel.send(f"/w {ctx.author.name} You do not have access to this command")
                    await ctx.channel.send(f"/delete {ctx.message.id}")
            else:
                await ctx.channel.send(f"song requests are already open")
                await ctx.channel.send(f"/delete {ctx.message.id}")
        except:
            await ctx.send("Try Again")
    #request a song
    @commands.command()
    async def requestsong(self, ctx: commands.Context):
            my_file1 = open("txt/requestStart.txt", "r")
            my_file2 = open("txt/songsRequested.txt", "r")
            message = ctx.message.content.split(" ")
            request = message[0]
            if (ctx.author.name == 'fros7yfeet'):
                await ctx.send("You cant request for yourself silly")
            else:
                if (my_file1.read() == "True"):
                    if (ctx.author.name not in my_file2.read()) :
                        message = ctx.message.content.split(" ")
                        songname = message[1]
                        songartist = message[2]
                        my_file3 = open("txt/songsRequested.txt", "a")
                        my_file4 = open("txt/songsRequested.txt", "a")
                        my_file3.write(f"{ctx.author.name}: \n")
                        my_file4.write(f"{songname} \n")
                        my_file4.write(f"{songartist}")
                        await ctx.send(f"/w {ctx.author.name} has requested a song!")
                    else:
                        await ctx.channel.send(f"/w {ctx.author.name} You have already requested a song!")
                        await ctx.channel.send(f"/delete {ctx.message.id}")
                else:
                    await ctx.channel.send(f"/w {ctx.author.name} song requests are not open come back later")
                    await ctx.channel.send(f"/delete {ctx.message.id}")
    #close song requests
    @commands.command()
    async def endrequests(self, ctx: commands.Context): 
        running = open("txt/requestStart.txt", "r")
        file1 = open("txt/songsRequested.txt")
        admins = open("txt/admins.txt", "r")
        if(running.read() == "True"):
            if(ctx.author.name in admins.read()):
                with open("txt/songsrequested.txt", "w") as f:
                    f.write("")
                with open("txt/requestStart.txt", "w") as f:
                    f.write("False")

                await ctx.channel.send(f"/delete {ctx.message.id} ")
            else:
                await ctx.send("You dont have the perms to use this command")
                await ctx.channel.send(f"/delete {ctx.message.id} ")
        else: 
            await ctx.send("song requests werent started")
            await ctx.channel.send(f"/delete {ctx.message.id} ")
    #Begins Raffle
    @commands.command()
    async def beginraffle(self, ctx: commands.Context):
        user = ctx.author.name
        admins = open("txt/admins.txt", "r")
        if( user in admins.read()):
            my_file1 = open("txt/run.txt", "w")
            my_file1.write("True")
            await ctx.send('Entries for the raffle have started. Type !raffle  to join now!!')
            await ctx.channel.send(f"/delete {ctx.message.id}")
        else:
            await ctx.channel.send(f'/w {ctx.author.name} You are not the Streamer')
    #enter raffle
    @commands.command()
    async def raffle(self, ctx: commands.Context):
            print(ctx.author.name)
            my_file1 = open("txt/run.txt", "r")
            my_file3 = open("txt/listForRaffle.txt", "r")
            if (ctx.author.name == 'fros7yfeet'):
                await ctx.send("You cant enter your own raffle silly")
            else:
                if (my_file1.read() == "True"):
                    if (ctx.author.name not in my_file3.read()) :
                        my_file1 = open("txt/listForRaffle.txt", "a")
                        my_file1.write(f"{ctx.author.name} \n")
                        my_file1.close()
                        await ctx.send(f"{ctx.author.name} has entered the raffle!")
                        await ctx.channel.send(f"/delete {ctx.message.id}")
                    else :
                        await ctx.channel.send(f"/w {ctx.author.name} You have already entered this raffle!")
                        await ctx.channel.send(f"/delete {ctx.message.id}")
                else :
                    await ctx.channel.send(f"/w {ctx.author.name} Raffle has not started")
                    await ctx.channel.send(f"/delete {ctx.message.id}")
    #End Raffle
    @commands.command()
    async def endraffle(self, ctx: commands.Context):
        print(ctx.author.name)
        my_file1 = open("txt/run.txt", "r")
        admins = open("txt/admins.txt", "r")
        if(my_file1.read() == "True"):
            if(ctx.author.name in admins.read()):
                my_file2 = open("txt/listForRaffle.txt", "r")
                lines= my_file2.read().split("\n")
                my_file2.close()
                random_person = random.choice(lines)
                print(random_person)
                await ctx.send(f"{random_person} has won the raffle")
                with open("txt/listForRaffle.txt", "w") as f:
                    f.write("")
                with open("txt/run.txt", "w") as f:
                    f.write("False")
                await ctx.channel.send(f"/delete {ctx.message.id} ")
            else:
                await ctx.send("You are not the Streamer")
                await ctx.channel.send(f"/delete {ctx.message.id} ")
        else: 
            await ctx.send("Raffle has not started")
            await ctx.channel.send(f"/delete {ctx.message.id} ")


bot = Bot()
bot.run()
