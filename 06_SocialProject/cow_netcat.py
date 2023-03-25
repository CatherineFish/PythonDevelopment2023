import cmd
import threading
import time
import readline
import sys, shlex
import asyncio

async def write(message, writer):
    writer.write(f"{message}\n".encode())
    await writer.drain()

class CowNetcat(cmd.Cmd):

    def __init__(self, reader, writer):
        super(CowNetcat, self).__init__()
        self.reader, self.writer = reader, writer

    def do_who(self, arg):
        asyncio.run(write("who", self.writer))

    def do_cows(self, arg):
        asyncio.run(write("cows", self.writer))

    def do_login(self, arg):
        login, *trash = shlex.split(arg)
        asyncio.run(write(f"login {login}", self.writer))

    def do_say(self, arg):
        cow_name, message, *trash = shlex.split(arg)
        asyncio.run(write(f"say {cow_name} {message}", self.writer))

    def do_yield(self, arg):
        message, *trash = shlex.split(arg)
        asyncio.run(write(f"yield {message}", self.writer))

    def do_quit(self, arg):
        asyncio.run(write("quit", self.writer))


def spam(cmdline, timeout, count):
    for i in range(count):
        time.sleep(timeout)
        print(f"\nI'm a message № {i}!\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)



#timer = threading.Thread(target=spam, args=(cmdline, 3, 10))
#timer.start()

async def main():
    reader, writer = await asyncio.open_connection('0.0.0.0', 1337)
    cmdline = CowNetcat(reader, writer)
    return cmdline


cmd = asyncio.run(main())
cmd.cmdloop()
