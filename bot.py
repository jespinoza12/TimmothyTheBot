import socket,threading,random,os
from time import time
from twitchio.ext import commands, eventsub

class Bot(commands.Bot):

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

    @commands.command()
    async def beginraffle(self, ctx: commands.Context):
        await ctx.send("Entries for the raffle have started. Type !raffle  to join now!!")
        channelname = 'fro7yfeet' #Set the channel name here (No need for # that is done on for you)
        nick = os.environ['BOT_NICK']  # create an account for your bot on twitch then set you bot name here
        password = 'uf075iioydjehomm7ni6kfborwdcmi' #get your bots oath from http://www.twitchapps.com/tmi/
        # Do Not change anything below unless you know what your doing

        queue = 13 
        channel = '#'+channelname
        server = 'irc.twitch.tv'
        irc = socket.socket()
        irc.connect((server, 6667)) 
        irc.send('PASS ' + password + '\r\n')
        irc.send('NICK ' + nick + '\r\n')
        irc.send('JOIN ' + channel + '\r\n')
        rafflelist = []
        beginraffle = "Entries for the raffle have started. Type !raffle  to join now!!"
        print (beginraffle)
        irc.send('PRIVMSG ' + channel + ' :' + beginraffle + '\r\n')
        def rafflesave():
            rafflelist.append(user)
        def run_raffle():
            print (rafflelist)
            winner = random.choice(rafflelist)
            rafflewinner = winner + " is the winner!! :)"
            irc.send('PRIVMSG ' + os.environ['CHANNEL'] + ' :' + rafflewinner + '\r\n')
            print (winner) + ' won the raffle!!!'
            os._exit(0)
        def message(msg):
            global queue
            queue = 5
            if queue < 20: 
                irc.send('PRIVMSG ' + channel + ' :' + msg + '\r\n')
            else:
                print ('Message deleted')
        def queuetimer(): 
            global queue
            queue = 0
            threading.Timer(30,queuetimer).start()
        queuetimer()
        while True:
            tilthack = irc.recv(1204)
            user = tilthack.split(':')[1]
            user = user.split('!')[0] 
            if tilthack.find('PING') != -1:
                irc.send(tilthack.replace('PING', 'PONG')) 
            if tilthack.find('!raffle') != -1: 
                    if any(word in user for word in rafflelist):
                        message(user + ' has already entered :)')
                    else:
                        rafflesave()
                        message(user + ' has been added to the raffle :) '+ str(len(rafflelist)) + ' user(s) have joined the raffle.')
                        print (rafflelist) 
                        print (len(rafflelist)), 'user(s) have joined'
            if tilthack.find('!runraffle') != -1:
                run_raffle()

bot = Bot()
bot.run()
