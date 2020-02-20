import praw, re, statistics, random, operator, csv, time, collections, io, string, asyncio, discord, os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

kick_perms = [202278109708419072,201806047478939649,281586814471634945]

client = discord.Client()
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = discord.utils.get(client.guilds, name=GUILD)
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('p!hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('p!kickJZ'):
        guild = discord.utils.get(client.guilds, name=GUILD)
        if message.author.id in kick_perms:
            jz = client.get_user(254774534274547713)
            invite_chan = client.get_channel(513162681558106156)
            invite = await invite_chan.create_invite(max_age = 0, max_uses = 1)
            if jz.dm_channel:
                pass
            else:
                await jz.create_dm()
            dm_chan = jz.dm_channel
            await dm_chan.send(invite)
            await message.channel.send(f"""{message.author} can kick. Bye.""")
            await guild.kick(jz)
        else:
            await message.channel.send(f"""Silly {message.author}, kicks are for Mack""")

@client.event
async def on_member_join(member):
    if member.id == 254774534274547713:
        role1 = get(member.guild.roles, id=513430539890589696)
        role2 = get(member.guild.roles, id=679775400762933308)
        role3 = get(member.guild.roles, id=645634682062503937)
        await member.add_roles(role1,role2)

client.run(TOKEN)
