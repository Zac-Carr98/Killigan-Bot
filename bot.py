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
        # await interaction.response.send_message("You clicked the button!", ephemeral=True)

        modal = Scheduler()
        await interaction.response.send_modal(modal)
        await modal.wait()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.stop()


# class TextInput(discord.ui.TextInput):
#     def __init__(self, label):
#         super().__init__(label=label, type=)
#
#     async def button_callback(self, interaction: discord.Interaction):
#         await interaction.response.send_message("You clicked the button!", ephemeral=True)


# class TextView(discord.ui.View):
#     def __init__(self, *, timeout=180):
#         super().__init__(timeout=timeout)
#         self.value = None
#
#         self.add_item(discord.ui.TextInput(label="my textbox"))

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


class EndTimeInput(discord.ui.TextInput):
    def __init__(self, *, label='End Time'):
        super().__init__(label=label)
        self.placeholder = '12:00 PM'
        self.required = True
        self.min_length = 4
        self.max_length = 5
        self.custom_id = 'End_Time_Input'


class Scheduler(discord.ui.Modal, title='Session Scheduler'):
    name = NameInput()
    date = DateInput()
    start_time = StartTimeInput()
    end_time = EndTimeInput()

    async def on_submit(self, interaction: discord.Interaction):
        text_fields = interaction.data['components']

        name = text_fields[0]['components'][0]['value']
        startDateTime = parse_date_time(text_fields[1]['components'][0]['value'],
                                        text_fields[2]['components'][0]['value'],
                                        interaction.created_at)
        endDateTime = parse_date_time(text_fields[1]['components'][0]['value'],
                                      text_fields[3]['components'][0]['value'],
                                      interaction.created_at)

        # startDateTime = parse_date_time("08/05/2023", '12:00 pm', discord.utils.utcnow())
        # endDateTime = parse_date_time("08/05/2023", '01:00 pm', discord.utils.utcnow())

        vchannel = None
        for channel in interaction.guild.voice_channels:
            if channel.name == "General":
                vchannel = channel

        # TODO add voice channel verification
        try:
            await discord.guild.Guild.create_scheduled_event(interaction.guild,
                                                             name=name,
                                                             start_time=startDateTime,
                                                             end_time=endDateTime,
                                                             channel=vchannel)

            await interaction.response.send_message("Sick nasty brah, I'll get that hammered away for you.",
                                                    ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I dont have permission to do that")

        # except:
        #     await interaction.response.send_message(
        #         "Just hit something gnarly brah, gonna have to give that another go")


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
            try:
                MyView()
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry chief, can\'t hang around all day')

        # response = "Sure broham, what day were you thinking? (Remember, I only need dd/mm/yy"
        # await message.channel.send(response)
        #
        # try:
        #     reply = await client.wait_for('message', timeout=5.0)
        #     await message.channel.send(f'{reply.content} Is this the right date?')
        #
        #     try:
        #         reply2 = await client.wait_for('message, timeout=5.0')
        #         await message.channel.send(f'{reply2.content} is this the right time?')
        #
        #         try:
        #             await message.channel.send("Sick nasty brah, I'll get that hammered away for you.")
        #             message.guild.q()
        #
        #         except asyncio.TimeoutError:
        #             return await message.channel.send(f'Sorry chief, can\'t hang around all day')
        #
        #     except asyncio.TimeoutError:
        #         return await message.channel.send(f'Sorry chief, can\'t hang around all day')
        #
        # except asyncio.TimeoutError:
        #     return await message.channel.send(f'Sorry chief, can\'t hang around all day')
        else:
            response = bad_command_response(author_name)
            await message.channel.send(response)


client.run(TOKEN)
