from motobot import command, match, IRCLevel
from random import uniform, randint
from time import time


desu_key = 'desu_plugin_data'
desu_time_guard = {}


def can_desu(nick):
    last_desus = desu_time_guard.get(nick, [0, 0, 0, 0, 0,])
    current_time = time()

    ret = not all(current_time - x <= 5 * 60 for x in last_desus)
    if ret:
        last_desus.pop(0)
        last_desus.append(current_time)
        desu_time_guard[nick] = last_desus
    return ret


def generate_spam(str):
    """ The needless variables are for later, when stats are added. """
    un = uniform(0, 1) < 0.01
    number = randint(1, 30)
    string = 'un' + str if un else str * number
    return un, number, string


@match(r'^desu( *)$')
def desu_match(message, database):
    if can_desu(message.nick):
        un, number, string = generate_spam('desu')
        update_stats(database, message.nick, un, number)
        return string
    else:
        return "You've desu'd too recently to desu again."


@match(r'^baka( *)$', IRCLevel.op)
def baka_match(message, database):
    un, number, string = generate_spam('baka')
    return string


@match(r'^nya(a+)?n*?(\W|$)')
def nyan_match(message, database):
    num = int(round(normalvariate(15, 3)))
    return 'Ny' + 'a' * num + '~'


"""
@command('desu')
@command('desustats')
def desu_command(message, database):
    args = message.message.split(' ')
    if len(args) <= 1:
        stats = database.get_val(desu_key, {})
        scores = sorted(
            [(x[0], x[1][1]) for x in stats.items()],
            key=lambda item: item[1],
            reverse=True
        )

        response = "Users with most desus: "
        for nick, score in scores[0:5]:
            response += "{} ({}); ".format(nick, score)
        return response

    else:
        nick = ' '.join(args[1:]).rstrip()
        stats = database.get_val(desu_key, {}).get(nick)
        if stats == None:
            return "I have no desu stats for {}.".format(nick)
        else:
            return "{} has desu'd {} times and gotten {} desus, " \
                   "with an average of {} desus. " \
                   "They have been undesu'd {} times.".format(
                        nick, stats[0], stats[1], stats[1]/ stats[0], stats[2]
                    )
"""


@command('desu')
@command('desustats')
def desu_command(message, database):
    args = message.message.split(' ')
    nick = ''
    if len(args) <= 1:
        nick = message.nick
    else:
        nick = ' '.join(args[1:]).rstrip()
    
    stats = database.get_val(desu_key, {}).get(nick)
    if stats == None:
        return "I have no desu stats for {}.".format(nick)
    else:
        return "{} has desu'd {} times and gotten {} desus, " \
               "with an average of {} desus. " \
               "They have been undesu'd {} times.".format(
                    nick, stats[0], stats[1], stats[1]/ stats[0], stats[2]
                )


def update_stats(database, nick, un, number):
    stats = database.get_val(desu_key, {})
    userstats = stats.get(nick, [0, 0, 0])

    userstats[0] += 1
    if un:
        userstats[2] += 1
    else:
        userstats[1] += number

    stats[nick] = userstats
    database.set_val(desu_key, stats)
