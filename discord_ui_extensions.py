import discord
from discord.utils import get
from bot_helper import *


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
        self.placeholder = '15:30'
        self.default = '15:30'
        self.required = True
        self.min_length = 4
        self.max_length = 5
        self.custom_id = 'Start_Time_Input'


class RoleSelect(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(placeholder="Select a Role", custom_id="role_select", max_values=1)


class VoiceChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(placeholder="Select a Voice Channel", custom_id="channel_select",
                         channel_types=[discord.ChannelType.voice], max_values=1)


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
        vChannel = None
        for channel in interaction.guild.voice_channels:
            if channel.name == "General":
                vChannel = channel

        try:
            await discord.guild.Guild.create_scheduled_event(interaction.guild,
                                                             name=name,
                                                             start_time=startDateTime,
                                                             channel=vChannel)
            await self.reminder(startDateTime, interaction)

            await interaction.response.send_message("Sick nasty brah, I'll get that hammered away for you.",
                                                    ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Sorry broham, the head honcho said I'm not \"responsible\" "
                                                    "enough to do that", ephemeral=True)

    async def reminder(self, future, interaction):

        role = 1065304097911218177
        message = ", don't forget about the session tomorrow, my dude."
        now = datetime.datetime.now().astimezone()
        delta = (future - now).total_seconds()

        # await asyncio.sleep(delta)

        role = get(interaction.guild.roles, id=int(role))

        for user in interaction.guild.members:
            if role in user.roles:
                userDM = await user.create_dm() if (user.dm_channel is None) else user.dm_channel
                if userDM is not None:
                    await userDM.send(user.name + message)


class ConfirmScheduleView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = SelectView()

        await interaction.response.send_message("Sweeeet. What role and channel is this party gonna be in?",
                                                view=view,
                                                ephemeral=True)
        # modal = Scheduler()
        # await interaction.response.send_modal(modal)
        # await modal.wait()

    @discord.ui.button(label='No', style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('No problemo, I won\'t schedule anything.', ephemeral=True)
        self.stop()


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

        self.roleSelect = RoleSelect()
        self.vChannelSelect = VoiceChannelSelect()

        self.add_item(self.roleSelect)
        self.add_item(self.vChannelSelect)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        modal = Scheduler()
        await interaction.response.send_modal(modal)
        await modal.wait()

    # def check_inputs(self, values):