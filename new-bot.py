import datetime
import discord
import random
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
import pytz

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

DISCORD_TOKEN = TOKEN


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(name='roll-d20')
async def roll_d20(ctx):
    if ctx.author == bot.user:
        return

    roll = random.randint(1, 20)
    response = ""
    if roll == 1:
        response = "Oh, that's just the way I like it! Nothing but bad news."
    elif roll == 2:
        response = "Dude, harsh. That's like, totally not cool."
    elif roll == 3:
        response = "That's a bummer man, but don't worry, it could be worse."
    elif roll == 4:
        response = "Ha, sucks to be you. But hey, at least it's not me."
    elif roll == 5:
        response = "Ouch, that's gotta hurt. I recommend a nice long bender to get over it."
    elif roll == 6:
        response = "Well, that's not great. But it's not the end of the world either."
    elif roll == 7:
        response = "Ah, too bad. But you win some, you lose some, you know?"
    elif roll == 8:
        response = "Haha, wow, that's pretty mediocre. Sounds like my love life."
    elif roll == 9:
        response = "That's not great, but it's not the worst thing that could happen."
    elif roll == 10:
        response = "Hey, average is pretty good in my book. That's like, a solid C."
    elif roll == 11:
        response = "Meh, not great, not terrible. Just like the food in Barovia."
    elif roll == 12:
        response = "Haha, oh man, that's pretty funny. Not great, but funny."
    elif roll == 13:
        response = "That's like, totally unlucky dude. You should buy a lottery ticket, just in case."
    elif roll == 14:
        response = "Eh, not great, not terrible. Kinda like my hygiene."
    elif roll == 15:
        response = "Hey, that's not bad! You're like, halfway there to greatness."
    elif roll == 16:
        response = "Whoa, that's pretty good! You must have some killer karma or something."
    elif roll == 17:
        response = "That's like, totally gnarly dude! You're basically a rock star now."
    elif roll == 18:
        response = "Oh, hell yeah! That's like, some epic stuff right there."
    elif roll == 19:
        response = "Dude, that's amazing! You're basically a demigod or something."
    elif roll == 20:
        response = "Holy cow! That's like, the best thing ever! You should probably retire now, " \
                   "it's not gonna get better than this."

    await ctx.channel.send(f"You rolled a {roll}. {response}")


# define the form
form = {"name": {"question": "What is the name of the event?", "answer": None},
        "date": {"question": "What date is the event? (YYYY-MM-DD)", "answer": None},
        "time": {"question": "What time is the event? (24-hour format)", "answer": None},
        "voice_channel": {"question": "What voice channel will the event take place in?", "answer": None},
        "role": {"question": "What is the name of the role associated with the event?", "answer": None}}

# define the event reminder message in the style of Killigan
reminder_message = "What's up dudes and dudettes! Just a friendly reminder that you have an event scheduled for " \
                   "tomorrow at {} in the {} voice channel. Get stoked and don't forget to bring your own Skooma!"


@bot.command(name='schedule-event')
async def schedule_event(ctx):
    # create the form embed and send it to the channel
    embed = discord.Embed(title="Event Scheduling Form",
                          description="Please fill out the following information to schedule your event:")
    for question in form:
        embed.add_field(name=form[question]["question"], value=form[question]["answer"], inline=False)
    form_message = await ctx.send(embed=embed)

    # wait for responses to the form
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    for question in form:
        response = await bot.wait_for("message", check=check)
        form[question]["answer"] = response.content
        embed.set_field_at(list(form.keys()).index(question),
                           name=form[question]["question"],
                           value=form[question]["answer"],
                           inline=False)
        await form_message.edit(embed=embed)

    # schedule the event
    event_date = form["date"]["answer"]
    event_time = form["time"]["answer"]
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=form["voice_channel"]["answer"])
    role = discord.utils.get(ctx.guild.roles, name=form["role"]["answer"])

    timezone = pytz.timezone("US/Central")
    event_time_obj = datetime.datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
    event_time_obj = timezone.localize(event_time_obj)

    event_name = form["name"]["answer"]
    event = await bot.loop.create_task(voice_channel.guild.create_scheduled_event(name=event_name,
                                                                                  start_time=event_time_obj,
                                                                                  channel=voice_channel))
    await ctx.send(f"Event created with the name {event.name} and the scheduled time {event.start_time}")

    # send event reminders to the associated role
    seconds_in_day = 86400
    await asyncio.sleep((event.start_time - datetime.datetime.now(timezone)).total_seconds() - seconds_in_day)
    reminder_members = [member for member in role.members if not member.bot]
    for member in reminder_members:
        await member.send(reminder_message.format(event_time, voice_channel.name))


# the list of commands currently implemented by killigan bot
command_list = {"!help": "I'll, like, let you know what all I can do right now.",
                "!roll": "Let me roll that d20 for you and give it my oen personal spin.",
                "!schedule-event": "You tell me when, where, and who, and I'll set up an event, and send out a reminder"
                                   "one day before it happens."
                }


@bot.command(name='help')
async def help_command(ctx):
    if ctx.author == bot.user:
        return

    help_message = f"How's it going, bromigo? This is the one-stop killigan help screen-message-dialogue-thingy." \
                   f"Kinda let that one get away from me, but here's a list of my commands anyways:"

    for command, description in command_list.items():
        help_message += f"{command}: {description}\n"

    await ctx.channel.send(help_message)

bot.run(DISCORD_TOKEN)
