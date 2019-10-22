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
        if not self.playing:
            self.answer = random.randint(self.min,self.max)
            self.left = self.min
            self.right = self.max
            self.playing = True
            return "[Room {}] I have chosen a number! try guess it!({}~{}){}".format(self.room,self.left,self.right,self.answer)
        else:
            return "[Room {}] This game is playing! ({}~{})".format(self.room,self.left,self.right)

    def guess(self,author,guess_):
        if self.playing:
            if not guess_ in range(self.left, self.right+1):
                return "[Room {}] {} guess a number {}, out of range~({}~{})".format(self.room,author,guess_,self.left,self.right)
            if guess_ == self.answer:
                self.playing = False
                return "[Room {}] {} got the answer!".format(self.room, author)
            elif guess_ > self.answer:
                self.right = guess_
                return "[Room {}] {} guess a number {}, too big!({}~{})".format(self.room,author,guess_,self.left,self.right)
            else:
                self.left = guess_
                return "[Room {}] {} guess a number {}, too small!({}~{})".format(self.room,author,guess_,self.left,self.right)
        else:
            return "[Room {}] No game is running, call the owner: {}".format(self.room,self.owner)
    
    def status(self):
        if self.playing:
            return "[Room {}] game is running! ({}~{})".format(self.room,self.left,self.right)
        else:
            return "[Room {}] No game is running, call the owner: {}".format(self.room,self.owner)



bot = commands.Bot(command_prefix=':',description="A bizarre bot")
game = GuessNumber(0,1000)
user_room = {}    #all keys are str
room_dict = {}
id_counter = 1000

#developer_check
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

#abandoned command
@bot.command()
async def play(ctx,*args):
    if len(args) == 0:
        await ctx.send("\"guessNumber\":play guessNumber")
    elif str(args[0]) == "guessNumber":
        await ctx.send("playing guessNumber...")
        await ctx.send(game.play())
    else:
        await ctx.send('Unknown Command !!')

#guessNumber
@bot.command()
async def g(ctx,number = -955536):
    if number != -955536:
        result = game.guess(number)
        await ctx.send(result)
    else:
        await ctx.send("Please enter a number!")

@bot.command()
async def gnex(ctx,*args):
    author = ctx.author.name
    if len(args) == 0:
        await ctx.send("use \"create\" to create a room")
        await ctx.send("use \"join [room]\" to join a exist room")
        await ctx.send("use \"myroom\" to check who you are")
    elif args[0] == "create":
        global id_counter
        room = str(id_counter)
        room_dict[room] = {"id":room,"name":"guessNumberEX","game":guessNumberEX(room,ctx.author.name),"owner":ctx.author.name,"member":[]}
        user_room[ctx.author.name] = {"guessNumberEX":room}
        await ctx.send("gnex-Room {} has created! {} call your friend to join now!".format(room,ctx.author.name))
        id_counter += 1
    elif args[0] == "join":
        if len(args) >= 2:
            room_id = str(args[1])
            if room_id in room_dict.keys():
                if room_dict[room_id]["name"] == "guessNumberEX":
                    user_room[ctx.author.name] = {"guessNumberEX":room_id}
                    if not author in room_dict[room_id]["member"]:
                        room_dict[room_id]["member"].append(ctx.author.name)
                    await ctx.send(ctx.author.name +" join the Room: {}".format(room_id))
                else:
                    await ctx.send("Room {} is not a gnex-room! Sorry {}".format(room_id,author))
            else:
                await ctx.send("Room {} not found!".format(room_id))
        else:
            await ctx.send("Please Enter Room ID !")
    elif args[0] == "myroom":
        if author in user_room.keys():
            if "guessNumberEX" in user_room[author].keys():
                room_id = user_room[author]["guessNumberEX"]
                owner = room_dict[room_id]["owner"]
                await ctx.send("{} is in gnex-{}, owner is {}".format(author,room_id,owner))
            else:
                await ctx.send("{} you are not in a gnex-room!".format(author))
        else:
            await ctx.send("{} you are not in any room! Create one or Join one".format(author))
    elif args[0] == "play":
        if author in user_room.keys():
            if "guessNumberEX" in user_room[author].keys():
                room = room_dict[user_room[author]["guessNumberEX"]]
                if author == room["owner"]:
                    result =  room["game"].play()
                    await ctx.send(result)
                else :
                    await ctx.send("{} you are not the owner of this gnex-room! call {}".format(author,room["owner"]))
            else:
                await ctx.send("{} you are not in a gnex-room!".format(author))
        else:
            await ctx.send("{} you are not in any room! Create one or Join one".format(author))
    elif args[0] == "guess":
        if author in user_room.keys():
            if "guessNumberEX" in user_room[author].keys():
                room = room_dict[user_room[author]["guessNumberEX"]]
                if len(args) >= 2:
                    result = room["game"].guess(author = author,guess_ = int(args[1]))
                    await ctx.send(result)
                else:
                    await ctx.send("{}, please enter a number!".format(author))
            else:
                await ctx.send("{} you are not in a gnex-room!".format(author))
        else:
            await ctx.send("{} you are not in any room! Create one or Join one".format(author))
    elif args[0] == "status":
        if author in user_room.keys():
            if "guessNumberEX" in user_room[author].keys():
                room = room_dict[user_room[author]["guessNumberEX"]]
                result = room["game"].status()
                await ctx.send(result)
            else:
                await ctx.send("{} you are not in a gnex-room!".format(author))
        else:
            await ctx.send("{} you are not in any room! Create one or Join one".format(author))
    else:
        await ctx.send("Unknown Command !!")

#help instruction
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