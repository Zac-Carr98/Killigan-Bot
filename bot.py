# bot.py
import asyncio
import datetime
import os

from discord.ext.commands import Bot
from discord.utils import get

from bot_helper import *
from discord_ui_extensions import *

from discord.ext import commands
import discord
from dotenv import load_dotenv

from asyncio import TimeoutError

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)
bot = Bot(intents=intents, Client=client, command_prefix=commands.when_mentioned_or("/"))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Like, hows it goin\' {member.name}?'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    lower_message = message.content.lower()
    author_name = message.author.display_name

    if 'killigan' in lower_message:
        thoughts_list = ['think', 'thought', 'mind']
        if any(substring in lower_message for substring in thoughts_list):
            response = killigan_thoughts_response(author_name)
            await message.channel.send(response)
        elif 'd20' in lower_message:
            response = roll_d20_response(author_name)
            await message.channel.send(response)
        elif 'help' in lower_message:
            response = help_response(author_name)
            await message.channel.send(response)
        elif 'schedule' in lower_message:

            view = ConfirmScheduleView()
            try:
                await message.channel.send("Did you wanna schedule a new session?", view=view)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry chief, can\'t hang around all day')
        else:
            response = bad_command_response(author_name)
            await message.channel.send(response)


client.run(TOKEN)
