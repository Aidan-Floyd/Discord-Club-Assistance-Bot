import asyncio
import discord
import random

from os import path
from discord import Colour

# Setup Discord API under the hood
intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

# Define Embeds

class command_embeds:

    def __init__(self):
        pass

    def voluntell(self, member):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.add_field(name='Voluntell', value=f"You're up next {member.mention}!", inline=False)
        return embed

class emoji_class:

    def __init__(self):

        self.stop_sign = '\U0001F6D1'
        self.next_track = '\U000023ED'


# Stored in a pattern of [message.author] : command_classobject
command_dict = {} 


class commands:

    def __init__(self, message, command, data):
        
        # Define the parameters needed to output to the right place

        self.author = message.author
        self.channel = message.channel
        
        # Data inputted can vary, check commands for specific requirements
        self.data = data

        # Identify the command needed
        command_dict = {
            ['voluntell'] : 'self.voluntell'
        }

        self.command = command_dict[command]                                                           
        

    def advance(self):
        await eval(self.command)

    async def voluntell(self):

        try:
            member = self.data.pop(0)
        except:
            global command_dict
            del command_dict[self.author]
        embed = command_embeds.voluntell(None, member)
        await self.channel.send(embed=embed)


        
class command_init:

    def __init__(self):
        pass

    async def greet(self, message):
        '''Get Clubbot to say hi
        '''

        greetings = [
            "hello",
            "hi",
            "hiya",
            "yo",
            "good day"
        ]
        if check_command_keywords(greetings, message) == True:
            await message.channel.send(f'Hello {message.author.display_name}!')
     
    async def voluntell(self, message):
        '''Iterate through a list of current members at random
        '''

        if check_command_keywords(['voluntell all', 'v all'], message) == True:
            await message.guild.chunk()
            member_list = [member for member in message.guild.members ]#if member.bot == False]

        elif check_command_keywords(['voluntell', 'v'], message) == True:
            await message.guild.chunk()
            member_list = [member for member in message.guild.members if str(member.status)=='online' and member.bot==False]
        else:
            pass

        random.shuffle(member_list)

        for member in member_list:
            embed = command_embeds.voluntell(None, member)
            await message.channel.send(embed=embed)

        command_object = commands(message, 'voluntell', member_list)

        global command_dict
        command_dict[message.author].append(command_object)


    async def run_commands(self, message):
        '''Run all possible commands (Triggered on a per-command basis)
        '''
        try:
            await asyncio.wait_for([
                self.greet(message),
                self.voluntell(message)
            ], timeout=3600)
        except asyncio.TimeoutError:
            pass

def check_command_keywords(keywords, message):
    '''Given a set of keywords and a message determine if a function is triggered. 
    Returns bool 
    '''
    present_keywords = [i for i in keywords if((i + ' ') in (message.content.lower() + ' '))]
    if len(present_keywords) > 0:
        return True
    else:
        return False



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        embed_name = message.Embeds[0].fields[0].name.lower()

        emojis = emoji_class()
        name_dict = {
            ['voluntell'] : 'iterable'
        }

        if name_dict[embed_name] == 'iterable':
            message.add_reaction(emojis.next_track)
            message.add_reaction(emojis.stop_sign)

        pass

    commands = command_init()

    if message.content.startswith('!'):
        await commands.run_commands(message)

@client.event
async def on_reaction_add(reaction):
    if reaction.author == client.user:
        pass

    global command_dict

    emojis = emoji_class()
    advance_flag = False

    reaction_dict = {
        [emojis.stop_sign] : 'command_dict.pop(reaction.author)',
        [emojis.next_track] : 'advance_flag = True'
    }

    eval(reaction_dict[reaction.emoji])

    if advance_flag == True:

        command_object = command_dict[reaction.author]
        command_object.advance()




# Boot Up
if path.exists('token.txt'):
    with open('token.txt') as tokenFile:
        token = tokenFile.read() 
        client.run(token)
        
else:
    with open('token.txt', "w") as token:
        token.write('')
    raise EOFError("No Token.txt found. Please add a token")
    