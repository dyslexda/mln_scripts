import praw, re, statistics, random, operator, csv, time, collections, io, string, asyncio, discord, os, gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
load_dotenv()
#Discord config
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#Sheets config
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
sheets_client = gspread.authorize(creds)

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
#############################################
    if message.content.startswith('p!sudoku'):
        sheets_client.login()
        guild = discord.utils.get(client.guilds, name=GUILD)
        invite_chan = client.get_channel(513162681558106156)
        invite = await invite_chan.create_invite(max_age = 0, max_uses = 1)
        if message.author.dm_channel:
            pass
        else:
            await message.author.create_dm()
        dm_chan = message.author.dm_channel
        sheet = sheets_client.open_by_key()#Spreadsheet key here
        kc_sheet = sheet.get_worksheet(0)
        rt_sheet = sheet.get_worksheet(1)
        auth_id = str(message.author.id)
        try:
            snowflake_cell = kc_sheet.find(auth_id)
        except:
            kc_sheet.append_row([message.author.name,auth_id,0],value_input_option='USER_ENTERED')
            snowflake_cell = kc_sheet.find(auth_id)
        count_cell = kc_sheet.cell(snowflake_cell.row,snowflake_cell.col+1)
        new_count = int(count_cell.value)+1
        kc_sheet.update_cell(count_cell.row,count_cell.col,new_count)
        user_roles = [message.author.name,auth_id]
        for r in message.author.roles:
            if r.name != '@everyone':
                user_roles.append(str(r.id))
        rt_sheet.append_row(user_roles,value_input_option='USER_ENTERED')
        await dm_chan.send(invite)
        await message.channel.send(f"""{message.author} took the honorable way out. Times sudoku'd: {new_count}""")
        await guild.kick(message.author)

@client.event
async def on_member_join(member):
    sheets_client.login()
    sheet = sheets_client.open_by_key()#Spreadsheet key here
    kc_sheet = sheet.get_worksheet(0)
    rt_sheet = sheet.get_worksheet(1)
    try:
        snowflake_cell = rt_sheet.find(str(member.id))
        role_cells = rt_sheet.row_values(snowflake_cell.row)[2:]
        role_list = []
        for i in role_cells:
            role_list.append(get(member.guild.roles,id=int(i)))
        await member.add_roles(*role_list)
        rt_sheet.delete_row(snowflake_cell.row)
    except:
        pass
    if member.id == 254774534274547713:
        role1 = get(member.guild.roles, id=513430539890589696)
        role2 = get(member.guild.roles, id=679775400762933308)
        role3 = get(member.guild.roles, id=645634682062503937)
        await member.add_roles(role1,role2,role3)

client.run(TOKEN)
