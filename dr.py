
import argparse
import json
import time

from pywinauto.application import Application
from pywinauto import keyboard

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-c', '--config', help='config file',
                    type=str, required=True)

args = parser.parse_args()


# load config
with open(args.config) as f:
    config = json.load(f)

interval = config['interval']
cmd_line = config['cmd_line']

# start and connect application
Application().start(cmd_line, work_dir=config.get('work_dir'))
time.sleep(interval)
app = Application().connect(path=cmd_line)

# actions
for action in config['actions']:
    if action['type'] == 'key':
        keyboard.send_keys(action['value'], with_spaces=True,
                           with_tabs=True, with_newlines=True)
    elif action['type'] == 'focus':
        app.top_window().set_focus()
