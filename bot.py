import socket,threading,random,os
from twitchio.ext import commands



# set up the bot
# bot = commands.Bot(
#     token=os.environ['TMI_TOKEN'],
#     client_id=os.environ['CLIENT_ID'],
#     nick=os.environ['BOT_NICK'],
#     prefix=os.environ['BOT_PREFIX'],
#     initial_channels=[os.environ['CHANNEL']]
# )


class Bot(commands.Bot):


    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send('test passed!')


bot = Bot()
bot.run()


#VICTOR UPDATE!!!

# @bot.command(name='beginraffle')
# async def event_ready():
#     channelname = 'fro7yfeet' #Set the channel name here (No need for # that is done on for you)
#     nick = os.environ['BOT_NICK']  # create an account for your bot on twitch then set you bot name here
#     password = 'oauth:uf075iioydjehomm7ni6kfborwdcmi' #get your bots oath from http://www.twitchapps.com/tmi/
#     # Do Not change anything below unless you know what your doing

#     queue = 13 
#     channel = '#'+channelname
#     server = 'irc.twitch.tv'
#     irc = socket.socket()
#     irc.connect((server, 6667)) 
#     irc.send('PASS ' + password + '\r\n')
#     irc.send('NICK ' + nick + '\r\n')
#     irc.send('JOIN ' + channel + '\r\n')
#     rafflelist = []
#     beginraffle = "Entries for the raffle have started. Type !raffle  to join now!!"
#     print (beginraffle);
#     irc.send('PRIVMSG ' + channel + ' :' + beginraffle + '\r\n')
#     def rafflesave():
#         rafflelist.append(user)
#     def run_raffle():
#         print (rafflelist)
#         winner = random.choice(rafflelist)
#         rafflewinner = winner + " is the winner!! :)"
#         irc.send('PRIVMSG ' + channel + ' :' + rafflewinner + '\r\n')
#         print (winner) + ' won the raffle!!!'
#         os._exit(0)
#     def message(msg):
#         global queue
#         queue = 5
#         if queue < 20: 
#             irc.send('PRIVMSG ' + channel + ' :' + msg + '\r\n')
#         else:
#             print ('Message deleted')
#     def queuetimer(): 
#         global queue
#         queue = 0
#         threading.Timer(30,queuetimer).start()
#     queuetimer()
#     while True:
#         tilthack = irc.recv(1204)
#         user = tilthack.split(':')[1]
#         user = user.split('!')[0] 
#         if tilthack.find('PING') != -1:
#             irc.send(tilthack.replace('PING', 'PONG')) 
#         if tilthack.find('!raffle') != -1: 
#                 if any(word in user for word in rafflelist):
#                     message(user + ' has already entered :)')
#                 else:
#                     rafflesave()
#                     message(user + ' has been added to the raffle :) '+ str(len(rafflelist)) + ' user(s) have joined the raffle.')
#                     print (rafflelist) 
#                     print (len(rafflelist)), 'user(s) have joined'
#         if tilthack.find('!runraffle') != -1:
#             run_raffle()

