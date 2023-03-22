import socket
import os
import curses

ESCAPE_KEY = 27


class Command:
    def __init__(self, key, text, msg):
        self.key = key
        self.text = text
        self.msg = msg


commands = [Command(curses.KEY_UP, 'Foward...', 'forward'),
            Command(curses.KEY_DOWN, 'Backward...', 'backward'),
            Command(curses.KEY_LEFT, 'Left...', 'left'),
            Command(curses.KEY_RIGHT, 'Right...', 'right'),
            Command(curses.KEY_PPAGE, 'Robust forward...', 'rforward'),
            Command(curses.KEY_NPAGE, 'Robust backward...',
                    'rbackward'),
            Command(ord(' '), 'Stand...', 'stand'),
            Command(ord('c'), 'Sit...', 'sit'),
            Command(ord('x'), 'Lie...', 'lie')] +\
    [Command(ord(str(i)), f'Emote {i}...', f'emote{i}') for i in range(10)]


if __name__ == '__main__':
    host = '10.42.0.1'
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    os.environ.setdefault('ESCDELAY', '0')
    scr = curses.initscr()
    curses.cbreak()
    # disable echoing of keys
    curses.noecho()
    scr.keypad(1)
    # lower escape delay

    scr.addstr(0, 5, "Hit 'Escape' to quit")
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
                client_socket.send(cmd.msg.encode())
                break
        scr.refresh()
    curses.endwin()
