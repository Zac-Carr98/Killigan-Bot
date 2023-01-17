import datetime
import random
import re


def parse_date_time(date, time, now):
    format_date = "%m/%d/%Y"
    format_time = "%H:%M"

    date_formatted = datetime.datetime.strptime(date, format_date).date()
    time_formatted = datetime.datetime.strptime(time, format_time).time()

    tz = now.tzinfo

    return datetime.datetime(year=date_formatted.year, month=date_formatted.month, day=date_formatted.day,
                             hour=time_formatted.hour, minute=time_formatted.minute, tzinfo=tz)


def test(date):
    # format_data = "%m/%d/%Y"
    format_time = "%H:%M"

    date_formatted = datetime.datetime.strptime(date, format_time).time()
    print(date_formatted)


def italicize_string(string):
    return '*' + string + '*'


def bold_string(string):
    return '**' + string + '**'


def killigan_thoughts_response(user_name):
    killigan_quotes = [
        'This does NOT look good my dudes...',
        'Righteous!',
        'Is there, like, anymore wine?',
        f'I don\'t know {user_name}, what do ' + italicize_string(bold_string("YOU")) + ' think?',
        f'If I don\'t get some more Skooma soon, dipping.',
        'Busta move',
    ]

    return random.choice(killigan_quotes)


def roll_d20_response(user_name):
    result = random.randint(1, 20)
    response = f'**{result}**'
    if result == 1:
        return response + " " + italicize_string(f'That\'s a mad bummer, bro')
    elif result == 2:
        return response + " " + italicize_string(f'Well, I guess it could\'ve been worse')
    elif result == 3:
        return response + " " + italicize_string(f'**KAW KAW**')
    elif result == 4:
        return response + " " + italicize_string(f'Big yikes, my guy')
    elif result == 5:
        return response + " " + italicize_string(f'I\'m gonna need some more Skooma if you keep rolling like this')
    elif result == 6:
        return response + " " + italicize_string(f'I mean, its definitely not a good roll man')
    elif result == 7:
        return response + " " + italicize_string(f'Sahhh dude, that\'s not gonna quite cut it')
    elif result == 8:
        return response + " " + italicize_string(f'jksadhfkujas')
    elif result == 9:
        return response + " " + italicize_string(f'jksadhfkujas')
    elif result == 10:
        return response + " " + italicize_string(f'This is definitely one of the rolls I\'ve ever seen')
    elif result == 11:
        return response + " " + italicize_string(f'Well, it could have been worse, but not by much!')
    elif result == 12:
        return response + " " + italicize_string(f'jksadhfkujas')
    elif result == 13:
        return response + " " + italicize_string(f'asdfgasedfa')
    elif result == 14:
        return response + " " + italicize_string(f'Well, it could have been worse, but not by much!')
    elif result == 15:
        return response + " " + italicize_string(f'Now we\'re cooking with moon sugar')
    elif result == 16:
        return response + " " + italicize_string(f'jksadhfkujas')
    elif result == 17:
        return response + " " + italicize_string(f'jksadhfkujas')
    elif result == 18:
        return response + " " + italicize_string(f'Bros, {user_name} is on Fire!')
    elif result == 19:
        return response + " " + italicize_string(f'Now this that Skooma hittin\'!')
    elif result == 20:
        return response + " " + italicize_string(f'Now **this**, {user_name}, **this** is gonna be good')


def bad_command_response(user_name):
    bad_command_responses = [
        "I don't know what that means, my dude...",
        f'I\'m gonna be honest {user_name}, that doesn\'t make any sense.',
        f'If you\'re gonna talk crazy {user_name}, I\'m gonna go find something shiny.',
        f'Can you repeat that? I\'m a bit of a bird brain.',
        'Sorry, bro I was squawkin\' somewhere else, what did you say?'
    ]

    return random.choice(bad_command_responses)


def help_response(user_name):
    help_string = "Well, I don't know about helping, but my current commands are: \n" \
                  "     **Killigan, (thought, think, mind) ?** - Get a peak into the mind of Killigan\n" \
                  "     **Killigan, roll a d20** - Roll a d20, and get an official Killigan reaction to your result\n" \
                  "     **Killigan, help** - Get this command again" \
                  "\n" \
                  "\n" \
                  "I'm not too smart right now, but if you have any suggestions, questions, or bug reports," \
                  " be sure to let Zac (JollyGreen) know!"

    return help_string
