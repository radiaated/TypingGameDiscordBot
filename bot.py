import discord
from discord.ext import commands
import typing
import datetime
import speed_algorithm as spalgo
import db_handler
import aiohttp
import io
import asyncio
import os


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():

    print(f'We have logged in as {client.user}')
    await client.tree.sync()

@client.tree.command(name="play", description="Play")
async def play(interaction):
    await interaction.response.defer()
    
    p_data = db_handler.db_get_paragraph()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(p_data["img"]) as resp:
            if resp.status != 200:
                return await interaction.followup.send('> Could not fetch image...')
            data = io.BytesIO(await resp.read())
            await interaction.followup.send(file=discord.File(data, f'aalutype-p.jpg'))

    try:
        t1 = datetime.datetime.utcnow()

        def check(m):
            return m.channel == interaction.channel

        msg = await client.wait_for('message', check=check, timeout=300)
        t2 = datetime.datetime.utcnow()

        diff = (t2-t1).total_seconds()

        wpm = spalgo.algo(p_data["paragraph"], msg.content, diff)

        db_handler.db_insert_users_pb(interaction.user.id, interaction.user, {"wpm": wpm})
    
        await interaction.channel.send('> {.author}, your wpm is `{wpm} wpm`'.format(msg, wpm=wpm), reference=msg)

    except asyncio.TimeoutError:

        await interaction.channel.send(f"> {interaction.user}, you timed out.", reference=interaction.message)
    

    


@client.tree.command(name="top", description="Top 10")
async def top(interaction):
    await interaction.response.defer()
   
    topten = db_handler.db_view_topten()

    res_msg = '> ### Top 10 Rankings'

    for ind, val in enumerate(topten):
        res_msg += f"\n> {f'**{ind + 1}.**' if ind + 1 > 3 else ':first_place:' if ind + 1 == 1 else ':second_place:' if ind +1 == 2 else ':third_place:' }  {val[0]} - `{val[1]} wpm`"


    await interaction.followup.send(res_msg)



@client.tree.command(name="pb", description="Find Personal Best")
async def pb(interaction, user: typing.Optional[discord.Member]):
    await interaction.response.defer()

    mentioned_user = user if user != None else interaction.user
   
    pb = db_handler.db_view_user_pb(mentioned_user.id)

    reply_msg = f"> **{mentioned_user.name}\'s** personal best is `{pb} wpm`." if pb != None else f"**{mentioned_user.name}** has no playing history"

    await interaction.followup.send(reply_msg) 


       
       

client.run(os.environ.get("BOT_TOKEN"))
