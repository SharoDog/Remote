import socket
import os
import curses

ESCAPE_KEY = 27


class Command:
    def __init__(self, key, text, key_name, msg):
        self.key = key
        self.text = text
        self.key_name = key_name
        self.msg = msg


commands = [Command(curses.KEY_UP, 'Foward', 'Arrow Up', 'forward'),
            Command(curses.KEY_DOWN, 'Backward', 'Arrow Down', 'backward'),
            Command(curses.KEY_LEFT, 'Left', 'Arrow Left', 'left'),
            Command(curses.KEY_RIGHT, 'Right', 'Arrow Right', 'right'),
            Command(curses.KEY_PPAGE, 'Robust forward', 'Page Up', 'rforward'),
            Command(curses.KEY_NPAGE, 'Robust backward', 'Page Down',
                    'rbackward'),
            Command(ord(' '), 'Stand', 'Space', 'stand'),
            Command(ord('c'), 'Sit', 'c', 'sit'),
            Command(ord('x'), 'Lie', 'x', 'lie')] +\
    [Command(ord(str(i)), f'Emote {i}', str(
        i), f'emote{i}') for i in range(10)]


if __name__ == '__main__':
    host = '10.42.0.1'
    port = 5000

    client_socket = socket.socket()
    #  client_socket.connect((host, port))
    os.environ.setdefault('ESCDELAY', '0')
    scr = curses.initscr()
    curses.cbreak()
    # disable echoing of keys
    curses.noecho()
    scr.keypad(1)
    # lower escape delay

    scr.addstr(0, 5, "Hit 'Escape' to quit")
    # add instructions
    for (ind, command) in enumerate(commands):
        scr.addstr(4 + ind, 5, f'{command.key_name} -> {command.text}')
    scr.refresh()
    key = ''
    # run until escape
    while key != ESCAPE_KEY:
        key = scr.getch()
        for cmd in commands:
            if key == cmd.key:
                scr.move(2, 0)
                scr.clrtoeol()
                scr.addstr(2, 5, cmd.text)
                #  client_socket.send(cmd.msg.encode())
                break
        scr.refresh()
    curses.endwin()
