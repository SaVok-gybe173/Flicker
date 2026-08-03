from pynput.mouse import Button, Controller
from pyfiglet import Figlet
from rich.highlighter import Highlighter
from rich.console import Console
from termcolor import cprint

import keyboard
import time
import configparser
import os
import re

class MoneyHighlighter(Highlighter):
     def highlight(self, text):
        # Красим все '/' в зелёный
        for match in re.finditer(r'/', text.plain):
            text.stylize("bold blue", match.start(), match.end())
        # Все '\' в синий (обратный слэш надо экранировать)
        for match in re.finditer(r'\\', text.plain):
            text.stylize("bold blue", match.start(), match.end())
        

console = Console(highlighter=MoneyHighlighter())
flr = Figlet(font='slant')  # Более стильный шрифт
ascii_art = flr.renderText("Flicker")
console.print(ascii_art, style="bold green")

settings_name = "settings.ini"
config = configparser.ConfigParser()
mouse = Controller()

is_update = True
try:
    if os.path.isfile(settings_name):
        config.read(settings_name, "utf-8")
        float(config.get('SETTINGS', 'time')) 
        (int(config.get('POSITION1', 'x')), int(config.get('POSITION1', 'y')))
        (int(config.get('POSITION2', 'x')), int(config.get('POSITION2', 'y')))
        int(config.get('POSITION1', 'count'))
        int(config.get('POSITION2', 'count'))
        config.get('SETTINGS', 'start_stop')
        config.get('SETTINGS', 'position1')
        config.get('SETTINGS', 'position2')
        config.get('SETTINGS', 'alignment') # alignment
        config.get('SETTINGS', 'stop')
        is_update = False
    
except: ...

if is_update:
    config.add_section('SETTINGS')
    config.set('SETTINGS', 'time', '0.05')
    config.set('SETTINGS', 'start_stop', '1')
    config.set('SETTINGS', 'position1', '8')
    config.set('SETTINGS', 'position2', '9')
    config.set('SETTINGS', 'stop', 'f7')
    config.set('SETTINGS', 'alignment', '2')

    config.add_section("POSITION1")
    config.add_section("POSITION2")
    config.set('POSITION1', 'x', '0')
    config.set('POSITION1', 'y', '0')
    config.set('POSITION1', 'count', '2')

    config.set('POSITION2', 'x', '0')
    config.set('POSITION2', 'y', '0')
    config.set('POSITION2', 'count', '1')

    with open(settings_name, "w", encoding="utf-8") as f:
        config.write(f)

_time = float(config.get('SETTINGS', 'time')) 

position1 = (int(config.get('POSITION1', 'x')), int(config.get('POSITION1', 'y')))
position2 = (int(config.get('POSITION2', 'x')), int(config.get('POSITION2', 'y')))
count1 = int(config.get('POSITION1', 'count'))
count2 = int(config.get('POSITION2', 'count'))

start_stop = config.get('SETTINGS', 'start_stop')
key_position1 = config.get('SETTINGS', 'position1')
key_position2 = config.get('SETTINGS', 'position2')
key_stop = config.get('SETTINGS', 'stop')
key_alignment = config.get('SETTINGS', 'alignment')

stop_flag = True
while_flag = True

print(f"""
https://github.com/SaVok-gybe173

Нажмите на {start_stop} для остановки/запуска.
Нажмите на {key_alignment} что бы выравнить.

Нажмите на {key_position1} для изменения начальныйх кординат.
Нажмите на {key_position2} для изменения конечных кординат.

Нажмите на {key_stop} для полной остановки.
""")

def alignment():
    global mouse, stop_flag
    stop_flag = True
    mouse.press(Button.left)
    time.sleep(_time)
    mouse.position = position1
    time.sleep(_time)
    mouse.release(Button.left)
    print(f"Клавиша {key_alignment} нажата, выравнивание...")
keyboard.add_hotkey(key_alignment, alignment)

def on():
    global mouse, position2
    position2 = mouse.position
    config.set('POSITION2', 'x', str(position2[0]))
    config.set('POSITION2', 'y', str(position2[1]))
    print(f"Клавиша {key_position2} нажата...")
    with open(settings_name, "w", encoding="utf-8") as f:
            config.write(f)
keyboard.add_hotkey(key_position2, on)

def on():
    global mouse, position1
    position1 = mouse.position
    config.set('POSITION1', 'x', str(position1[0]))
    config.set('POSITION1', 'y', str(position1[1]))
    print(f"Клавиша {key_position1} нажата...")
    with open(settings_name, "w", encoding="utf-8") as f:
            config.write(f)
keyboard.add_hotkey(key_position1, on)

def on_esc():
    global while_flag
    while_flag = not while_flag
    print(f"Клавиша {key_stop} нажата, останавливаем...")
keyboard.add_hotkey(key_stop, on_esc)

def on_esc():
    global stop_flag
    stop_flag = not stop_flag
    print(f"Клавиша {start_stop} нажата...")
keyboard.add_hotkey(start_stop, on_esc)

while while_flag:
    if not stop_flag:
        mouse.position = position1
        time.sleep(_time)
        mouse.click(Button.left, count1)
        time.sleep(_time)
        #mouse.move(160, 190)
        mouse.position = position2
        time.sleep(_time)
        mouse.click(Button.left, count2)
        time.sleep(_time)