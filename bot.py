import socket,threading,random,os
from twitchio.ext import commands

# set up the bot
bot = commands.Bot(
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)

    if 'hello' in ctx.content.lower():
        await ctx.channel.send(f"Hi, @{ctx.author.name}!")


@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

@bot.command(name='beginraffle')
async def event_ready():
    channelname = 'fro7yfeet' #Set the channel name here (No need for # that is done on for you)
    nick = os.environ['BOT_NICK']  # create an account for your bot on twitch then set you bot name here
    password = 'oauth:uf075iioydjehomm7ni6kfborwdcmi' #get your bots oath from http://www.twitchapps.com/tmi/
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
    print (beginraffle);
    irc.send('PRIVMSG ' + channel + ' :' + beginraffle + '\r\n')
    def rafflesave():
        rafflelist.append(user)
    def run_raffle():
        print (rafflelist)
        winner = random.choice(rafflelist)
        rafflewinner = winner + " is the winner!! :)"
<<<<<<< Updated upstream
        irc.send('PRIVMSG ' + os.environ['CHANNEL'] + ' :' + rafflewinner + '\r\n')
=======
        irc.send('PRIVMSG ' + channel + ' :' + rafflewinner + '\r\n')
>>>>>>> Stashed changes
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

if __name__ == "__main__":
    bot.run()
