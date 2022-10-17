
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

# close if already running
try:
    app = Application().connect(path=cmd_line, timeout=1)
    app.kill()
except Exception as e:
    pass
time.sleep(interval)

# start application
Application().start(cmd_line, work_dir=config.get('work_dir'))
time.sleep(interval)

# connect application
app = Application().connect(path=cmd_line)
time.sleep(interval)

# set focus
app.top_window().set_focus()

# actions
for action in config['actions']:
    act_type = action['type']
    act_value = action.get('value')

    if act_type == 'key':
        keyboard.send_keys(
            action['value'], with_spaces=True, vk_packet=vk_packet)
    elif act_type == 'input':
        value = input(f'{act_value}:')
        app.top_window().set_focus()
        keyboard.send_keys(value, with_spaces=True, vk_packet=vk_packet)
    elif act_type == 'wait':
        time.sleep(act_value)

    time.sleep(interval)
