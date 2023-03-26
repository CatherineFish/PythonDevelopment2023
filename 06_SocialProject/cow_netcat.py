import cmd
import threading
import readline
import shlex
import socket
import sys


HOST = '0.0.0.0'
PORT = 1337  


def write(message, socket):
    socket.send(f"{message}\n".encode())
    

#async def send_messages_as(reader):
#    send = asyncio.create_task(reader.readline())
#    while not reader.at_eof():
#        done, pending = await asyncio.wait([send], return_when=asyncio.ALL_COMPLETED)
#        for q in done:
#            send = asyncio.create_task(reader.readline())
#            print(f'{q.result().decode()}\n{cmdline.prompt}{readline.get_line_buffer()}', end="", flush=True)


class CowNetcat(cmd.Cmd):

    def __init__(self, socket):
        super(CowNetcat, self).__init__()
        self.sock = socket
        
    def do_who(self, arg):
        write("who", self.sock)

    def do_cows(self, arg):
        write("cows", self.sock)

    def do_login(self, arg):
        login, *trash = shlex.split(arg)
        write(f"login {login}", self.sock)

    def do_say(self, arg):
        cow_name, message, *trash = shlex.split(arg)
        write(f"say {cow_name} {message}", self.sock)

    def do_yield(self, arg):
        message, *trash = shlex.split(arg)
        write(f"yield {message}", self.sock)

    def do_quit(self, arg):
        write("quit", self.sock)


    #def send_messages(self):
    #    send_messages_as(self.reader))
        

if __name__ == "__main__":
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
            s.setblocking(False)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    with s:
        cmdline = CowNetcat(s)
        cmdline.cmdloop()
    

    
#sender.run()
    
