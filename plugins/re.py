from motobot import command, sink
from random import choice
import re


patterns_key = "re_patterns"


@sink()
def regex_sink(bot, nick, channel, message):
    for pattern, response in get_patterns(bot.database):
        if pattern.search(message):
            return parse_response(response, nick)


def parse_response(response, nick):
    response = choice(response.split('|'))
    return response.replace('{nick}', nick)


@command('re')
def regex_command(bot, nick, channel, message, args):
    arg = args[1].lower()
    if arg == 'add':
        add_regex(' '.join(args[2:]), bot.database)
        response = "Pattern added successfully."
    elif arg == 'del':
        response = rem_regex(' '.join(args[2:]), bot.database)
    elif arg == 'show':
        response = show_patterns(bot.database)
    else:
        response = "Unrecognised argument."

    return response


parse_pattern = re.compile(r'^(.*?)(?: ?)<=>(?: ?)(.*)')


def add_regex(string, database):
    pattern, response = parse_pattern.match(string).groups()

    patterns = get_patterns(database)
    patterns.append((re.compile(pattern, re.IGNORECASE), response))
    save_patterns(database, patterns)


def rem_regex(string, database):
    removed = False
    patterns = get_patterns(database)
    for pattern, response in patterns:
        if pattern.search(string):
            patterns.remove((pattern, response))
            save_patterns(database, patterns)
            return "Pattern matching the string have been removed."
    return "No patterns matched the string."


def show_patterns(database):
    patterns = get_patterns(database)
    string = ''

    for pattern, response in patterns:
        app = "{}: {};".format(pattern.pattern, response)
        string += app
    return string


patterns_cache = None


def get_patterns(database):
    global patterns_cache
    if patterns_cache is None:
        patterns_cache = [(re.compile(x, re.I), y) \
            for x, y in database.get_val(patterns_key, [])]
    return patterns_cache


def save_patterns(database, patterns):
    global patterns_cache
    patterns_cache = patterns
    database.set_val(patterns_key, [(x.pattern, y) for x, y in patterns])
