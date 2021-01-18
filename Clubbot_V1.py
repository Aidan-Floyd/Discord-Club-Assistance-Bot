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
            'voluntell' : 'self.voluntell()'
        }

        self.command = command_dict[command]                                                           
        

    async def advance(self):
        await eval(self.command)

    async def voluntell(self):

        try:
            member = self.data.pop(0)
        except:
            global command_dict
            del command_dict[self.author]
        try:
            embed = command_embeds.voluntell(None, member)
            await self.channel.send(embed=embed)
        except:
            return


        
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
            member_list = [member for member in message.guild.members if member.bot == False]

        elif check_command_keywords(['voluntell', 'v'], message) == True:
            await message.guild.chunk()

            member_list = []
            for member in message.guild.members:
                if str(member.status)=='online':
                    if member.bot == False:
                        member_list.append(member)


            #member_list = [member for member in message.guild.members if str(member.status)=='online' or str(member.status)=='' and member.bot==False]
        else:
            return

        random.shuffle(member_list)

        member = member_list.pop(0)

        embed = command_embeds.voluntell(None, member)
        await message.channel.send(embed=embed)

        command_object = commands(message, 'voluntell', member_list)

        global command_dict
        command_dict[message.author] = command_object


    async def run_commands(self, message):
        '''Run all possible commands (Triggered on a per-command basis)
        '''

        try:
            await self.greet(message)
            await self.voluntell(message)

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
        
        # If the bot sent an embed, find out function it's attached to
        embed_name = None
        try:
            embed_name = message.embeds[0].fields[0].name.lower()
        except:
            pass


        emojis = emoji_class()
        name_dict = {
            'voluntell' : 'iterable'
        }
        try:
            if name_dict[embed_name] == 'iterable':
                await message.add_reaction(emojis.next_track)
                await message.add_reaction(emojis.stop_sign)
        except:
            pass

        return

    commands = command_init()

    if message.content.startswith('!'):
        await commands.run_commands(message)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    global command_dict

    emojis = emoji_class()

    reaction_dict = {
        emojis.stop_sign : 'command_dict.pop(user)',
        emojis.next_track : 'advance'
    }

    reaction_action = reaction_dict[reaction.emoji]

    '''This whole convoluted section allows the exec function to reassign local variables.
    For security reasons, exec doesn't let you do this in an elegant way because of its
    potential use by malicious actors. Even if you've hardcoded in the strings. And guess what? It doesn't even work'''

    #new_locals = {}
    try:
        exec(reaction_action)
    except:
        pass
    #for k,v in new_locals.items(): locals()[k] = v

    '''End Convolution'''

    flag = reaction_action
    
    if flag == 'advance':
        command_object = command_dict[user]
        await command_object.advance()


if __name__ == '__main__':

    # Boot Up
    if path.exists('token.txt'):
        with open('token.txt') as tokenFile:
            token = tokenFile.read() 
            client.run(token)
            
    else:
        with open('token.txt', "w") as token:
            token.write('')
        raise EOFError("No Token.txt found. Please add a token")
        