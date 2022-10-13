
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
vk_packet = config.get('vk_packet', True)

# start and connect application
Application().start(cmd_line, work_dir=config.get('work_dir'))
time.sleep(interval)
app = Application().connect(path=cmd_line)
time.sleep(interval)

# actions
for action in config['actions']:
    if action['type'] == 'key':
        keyboard.send_keys(
            action['value'], with_spaces=True, vk_packet=vk_packet)
    elif action['type'] == 'input':
        value = action['value']
        value = input(f'{value}:')
        keyboard.send_keys(value, with_spaces=True, vk_packet=vk_packet)
        app.top_window().set_focus()

    time.sleep(interval)
