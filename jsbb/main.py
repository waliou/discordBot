import json
import discord
import random
from discord.ext import commands

auth = json.load(open('auth.json','r'))

class GuessNumber():
    def __init__(self,min_,max_):
        self.min = min_
        self.max = max_
        self.left = self.min
        self.right = self.max
        self.answer = 0
        self.playing = False

    def config(self,min_,max_):
        self.min = min_
        self.max = max_
        self.playing = False
        return "Range Change to ({}~{})".format(self.min,self.max)

    def play(self):
        if self.playing:
            return "The Game is already playing!({}~{})".format(self.left,self.right)
        else:
            self.playing = True
            self.answer = random.randint(self.min,self.max)
            self.left = self.min
            self.right = self.max
            return "I have chosen a number, use \":g [number]\" to guess it({}~{}) {}".format(self.min,self.max,self.answer)

    def guess(self,guess_):
        if not self.playing:
            return "guessNumber is not playing, try \":play guessNumber\" to start a game"
        else:
            if not guess_ in range(self.left,self.right+1):
                return "out of range!! ({}~{})".format(self.left,self.right)
            elif guess_ == self.answer:
                self.playing = False
                return "congratulation! you got the number {}!!".format(self.answer)
            elif guess_ < self.answer:
                self.left = guess_
                return "too small({}~{})".format(self.left,self.right)
            else:
                self.right = guess_
                return "too big({}~{})".format(self.left,self.right)


class guessNumberEX():
    def __init__(self,room,owner,min_ = 0,max_ = 1000):
        self.room = str(room)
        self.owner = owner
        self.min = min_
        self.max = max_
        self.left = self.min
        self.right = self.max
        self.answer = 0
        self.playing = False

    def get_name(self):
        return "guessNumberEX"

    def play(self):
        pass



bot = commands.Bot(command_prefix=':',description="A bizarre bot")
game = GuessNumber(0,1000)
room_distribute = {}    #all keys are str
game_list = {}
id_counter = 1000

@bot.event
async def on_ready():
    print("J\'sBB is open!")
    print(bot.user.name)
    print(bot.user.id)

@bot.command()
async def repeat(ctx,*args):
    await ctx.send("".join(args))

@bot.command()
async def broadcast(ctx,*args):
    for guild in bot.guilds:
        for channel in guild.channels:
            if type(channel) == discord.channel.TextChannel:
                await channel.send("吃我的全頻廣播啦")

@bot.command()
async def play(ctx,*args):
    if len(args) == 0:
        await ctx.send("\"guessNumber\":play guessNumber")
    elif str(args[0]) == "guessNumber":
        await ctx.send("playing guessNumber...")
        await ctx.send(game.play())
    elif str(args[0]) == "guessNumberEX":
        if str(args[1]) == "create":
            game_list[str(id_counter)] = guessNumberEX(id_counter,ctx.author.name)
            room_distribute[ctx.author.name] = {"guessNumberEX":str(id_counter)}
            id_counter+=1
        elif str(args[1]) == "join":
            if len(args) < 3:
                await ctx.send("Please enter Room ID")
            else:
                room = args[2]
                if str(room) in game_list.keys:
                    room_distribute[ctx.author.name] = {"guessNumberEX":str(room)}
                else:
                    await ctx.send("Room ID:{} Not Found!!".format(room))
    else:
        await ctx.send('Unknown Command !!')

@bot.command()
async def g(ctx,number = -955536):
    if number != -955536:
        result = game.guess(number)
        await ctx.send(result)
    else:
        await ctx.send("Please enter a number!")

bot.remove_command("help")
@bot.command()
async def help(ctx,*arg):
    embed = discord.Embed(title="JoJo's bizarre bot Manual!",description="JSBB version alpha0.0.1",color=0xffff00)
    embed.add_field(name=":repeat [content]",value="repeat what u say to jsbb")
    embed.add_field(name=":test", value="**DON'T USE IT UNLESS NECESSARY**do anything developer need")
    embed.add_field(name=":play [game]",value = "play some game with jsbb")
    embed.add_field(name=":g [number]",value = "when guessNumber is playing, use it to guess number")
    embed.set_author(name = "wa_liou")
    await ctx.send(embed = embed)

bot.run(auth['Token'])