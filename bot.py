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
        my_file = open("txt/badwords.txt", "r")
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
        await ctx.channel.send(f"/delete {ctx.message.id}")
    #Help Menu
    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.send(f'Questions: (! questions)' + ' Hello: (! hello)' + ' FlipCoin: (! FlipCoin)' + ' Start Raffle: (! beginraffle)'
        + ' Enter Raffle!: (! raffle)' + " End Poll(Admins): (! endpoll)" + '\n' + ' Poll Vote: (! vote A/B) Example: (! vote A)'  +
        ' Poll Start (Admins): (! poll) [question [For spaces insert -]] [option1] [option2] Example: (!pollstart) How-are-you-today? good bad' + 
        ' Help (! help)'+ " End Poll(Admins): (!endpoll)")

    #List of frequently asked questions
    @commands.command()
    async def questions(self, ctx: commands.Context):
        await ctx.send('How long have you been streaming? (!Long)' +
                        "What's My Name? (!Name)" + "How Old Am I? (!Age)" + "Where Am I from? (!From)" + "When Do I Stream? (!Stream)")
    #Flip Coin
    @commands.command()
    async def FlipCoin(self, ctx: commands.Context):
        randomNum = random.randint(1,2)
        await ctx.channel.send(f"/delete {ctx.message.id}")
        if (randomNum == 1) :
            await ctx.send(f"/w {ctx.author.name} Heads WINS!")
        else :
            await ctx.send(f"/w {ctx.author.name} Tails WINS!")
            
    #Question
    @commands.command()
    async def Long(self, ctx: commands.Context):
        await ctx.send('I have been streaming for 2 years')
    #Question
    @commands.command()
    async def Name(self, ctx: commands.Context):
        await ctx.send('Julian Winters')
    #Question
    @commands.command()
    async def Age(self, ctx: commands.Context):
        await ctx.send('20')
    #Question
    @commands.command()
    async def From(self, ctx: commands.Context):
        await ctx.send('I am from New York, Carliona')
    #Question
    @commands.command()
    async def Stream(self, ctx: commands.Context):
        await ctx.send('I stream everyday at 4')
    #Create Poll
    @commands.command()
    async def poll(self, ctx: commands.Context):
        my_file1 = open("txt/pollstart.txt", "r")
        if (my_file1.read() == "False"):
            if (ctx.author.name == "fros7yfeet") :
                message = ctx.message.content.split(" ")
                question = message[1].replace("-", " ")
                option1 = message[2]
                option2 = message[3]
                my_file1 = open("txt/pollstart.txt", "w")
                my_file1.write("True")
                await ctx.send(f"Poll has started!!! \n The question is {question} \n /vote A for {option1} \n /vote B for {option2}")
                await ctx.channel.send(f"/delete {ctx.message.id}")
            else :
                await ctx.channel.send(f"/w {ctx.author.name} You do not have access to this command")
                await ctx.channel.send(f"/delete {ctx.message.id}")
        else:
            await ctx.channel.send(f"There is already an open Poll")
            await ctx.channel.send(f"/delete {ctx.message.id}")
    #Voting
    @commands.command()
    async def vote(self, ctx: commands.Context):
        my_file1 = open("txt/pollstart.txt", "r")
        my_file2 = open("txt/voted.txt", "r")
        
        if (my_file1.read() == "True"):
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
                await ctx.channel.send(f"/{ctx.author.name} You have already voted!")
                await ctx.channel.send(f"/delete {ctx.message.id}")
        else:
            await ctx.send("No poll started come back later")
            await ctx.channel.send(f"/delete {ctx.message.id}")
    #End Poll
    @commands.command()
    async def pollend(self, ctx: commands.Context): 
        running = open("txt/pollstart.txt", "r")
        file1 = open("txt/votes.txt")
        if(running.read() == "True"):
            if(ctx.author.name == "fros7yfeet"):
                aVoteCount = file1.read().count("a")
                bVoteCount = file1.read().count("b")

                await ctx.send(f"Option A has {aVoteCount} and Option B has {bVoteCount}")

                if (aVoteCount > bVoteCount):
                    await ctx.send("Option A has WON!")
                else:
                    await ctx.send("Option B has Won!")

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
    #Begins Raffle
    @commands.command()
    async def beginraffle(self, ctx: commands.Context):
        print(ctx.author.name)
        if('fros7yfeet' == ctx.author.name):
            my_file1 = open("txt/run.txt", "w")
            my_file1.write("True")
            await ctx.send('Entries for the raffle have started. Type !raffle  to join now!!')
            await ctx.channel.send(f"/delete {ctx.message.id}")
        else:
            await ctx.send('You are not the Streamer')
    #enter raffle
    @commands.command()
    async def raffle(self, ctx: commands.Context):
            print(ctx.author.name)
            my_file1 = open("txt/run.txt", "r")
            my_file3 = open("txt/listForRaffle.txt", "r")

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
                await ctx.send("Raffle has not started")
                await ctx.channel.send(f"/delete {ctx.message.id} ")
    #End Raffle
    @commands.command()
    async def endraffle(self, ctx: commands.Context):
        print(ctx.author.name)
        my_file1 = open("txt/run.txt", "r")
        if(my_file1.read() == "True"):
            if(ctx.author.name == "fros7yfeet"):
                my_file1 = open("txt/listForRaffle.txt", "r")
                lines= my_file1.read().split("\n")
                my_file1.close()
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
