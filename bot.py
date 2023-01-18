# bot.py
import asyncio
import datetime
import os

from discord.ext.commands import Bot

from bot_helper import *

from discord.ext import commands
import discord
from dotenv import load_dotenv

from asyncio import TimeoutError

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)
bot = Bot(intents=intents, Client=client, command_prefix=commands.when_mentioned_or("/"))


# class Bot(commands.Bot):
#     def __init__(self):
#         intents = discord.Intents.default()
#         intents.message_content = True
#
#         super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)
#
#     async def on_ready(self):
#         print(f'Logged in as {self.user} (ID: {self.user.id})')
#         print('------')


class MyView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = Scheduler()
        await interaction.response.send_modal(modal)
        await modal.wait()

    @discord.ui.button(label='No', style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('No problemo, I won\'t schedule anything.', ephemeral=True)
        self.stop()


class NameInput(discord.ui.TextInput):
    def __init__(self, *, label='Session Name'):
        super().__init__(label=label)
        self.placeholder = 'New Session'
        self.default = 'New Session'
        self.required = True
        self.custom_id = 'Name_Input'


class DateInput(discord.ui.TextInput):
    def __init__(self, *, label='Date'):
        super().__init__(label=label)
        self.placeholder = 'MM/DD/YYYY'
        self.required = True
        self.min_length = 10
        self.max_length = 10
        self.custom_id = 'Date_Input'


class StartTimeInput(discord.ui.TextInput):
    def __init__(self, *, label='Start Time'):
        super().__init__(label=label)
        self.placeholder = '12:00 PM'
        self.required = True
        self.min_length = 4
        self.max_length = 5
        self.custom_id = 'Start_Time_Input'


class Scheduler(discord.ui.Modal, title='Session Scheduler'):
    name = NameInput()
    date = DateInput()
    start_time = StartTimeInput()

    async def on_submit(self, interaction: discord.Interaction):
        text_fields = interaction.data['components']

        name = text_fields[0]['components'][0]['value']
        inputStartTime = text_fields[1]['components'][0]['value'] + " " + text_fields[2]['components'][0]['value']

        startDateTime = parse_date_time(inputStartTime)

        # TODO add voice channel verification
        vchannel = None
        for channel in interaction.guild.voice_channels:
            if channel.name == "General":
                vchannel = channel

        try:
            await discord.guild.Guild.create_scheduled_event(interaction.guild,
                                                             name=name,
                                                             start_time=startDateTime,
                                                             channel=vchannel)

            await interaction.response.send_message("Sick nasty brah, I'll get that hammered away for you.",
                                                    ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Sorry broham, the head honcho said I'm not \"responsible\" "
                                                    "enough to do that")


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

            view = MyView()
            try:
                await message.channel.send("Did you wanna schedule a new session?", view=view)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry chief, can\'t hang around all day')
        else:
            response = bad_command_response(author_name)
            await message.channel.send(response)


client.run(TOKEN)
