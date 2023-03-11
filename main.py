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
            Command(curses.KEY_NPAGE, 'Clockwise...', 'clockwise'),
            Command(curses.KEY_PPAGE, 'Counterclockwise...',
                    'counterclockwise'),
            Command(ord(' '), 'Stand...', 'stand'),
            Command(ord('c'), 'Sit...', 'sit'),
            Command(ord('x'), 'Lie...', 'lie')]


if __name__ == '__main__':
    host = os.getenv('SHARO_ADDR')
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
