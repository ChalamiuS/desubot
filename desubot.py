from motobot import IRCBot, IRCLevel
from json import load
import desubot as this
import threading
import traceback

def worker():
    this.bot.run()

def main():
    this.bot.load_plugins('plugins')
    this.bot.load_database('desubot.json')
    this.bot.join('#MotoChan')
    this.bot.join('#animu')
    this.bot.join('#anime-planet.com')
    this.bot.join('#bakalibre')
    this.bot.join('#ap-marathon')
    
    thread = threading.Thread(target=worker)
    thread.start()

    running = True
    while running:
        try:
            msg = input()
            if msg.startswith(':'):
                this.bot.reload_plugins()
            elif msg.startswith('?'):
                this.bot.load_database('desubot.json')
            else:
                this.bot.send(msg)
        except KeyboardInterrupt:
            running = False
            this.bot.disconnect()
        except:
            traceback.print_exc()

if __name__ == '__main__':
    main()

else:
    config_filename = 'desubot_config.json'
    config_file = open(config_filename, 'r')
    config = load(config_file)
    bot = IRCBot(config)
