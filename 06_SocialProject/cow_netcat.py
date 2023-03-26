import cmd
import threading
import readline
import shlex
import socket
import sys
import select


HOST = '0.0.0.0'
PORT = 1337  


def write(message, socket):
    socket.send(f"{message}\n".encode())

def get_message(socket):
    event, *trash = select.select([socket], [], [], 0.0)
    for sock in event:
        return sock.recv(1024).decode().strip()
    return ""


def recive_messages(socket, cmdline):
    while True:
        data = get_message(socket)
        if data:
            print(f'{data}\n{cmdline.prompt}{readline.get_line_buffer()}', end="", flush=True)


class CowNetcat(cmd.Cmd):

    def __init__(self, socket, locker):
        super(CowNetcat, self).__init__()
        self.sock = socket
        self.locker = locker
        
    def do_who(self, arg):
        write("who", self.sock)

    def do_cows(self, arg):
        write("cows", self.sock)

    def do_login(self, arg):
        login, *trash = shlex.split(arg)
        write(f"login {login}", self.sock)

    def complete_login(self, text, line, begidx, endidx):
        current_args = shlex.split(line)
        args_len = len(current_args)
        if args_len <= 2:
            with self.locker:
                write("cows", self.sock) 
                return [res for res in get_message(self.sock) if res.startwith(text.lower())]    

    def do_say(self, arg):
        cow_name, message, *trash = shlex.split(arg)
        write(f"say {cow_name} {message}", self.sock)

    def complete_say(self, text, line, begidx, endidx):
        pass  

    def do_yield(self, arg):
        message, *trash = shlex.split(arg)
        write(f"yield {message}", self.sock)

    def complete_yield(self, text, line, begidx, endidx):
        pass  

    def do_quit(self, arg):
        write("quit", self.sock)
        exit(0)

        

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

        locker = threading.Lock()
        cmdline = CowNetcat(s, locker)
        thread = threading.Thread(target=recive_messages, args=(s, cmdline))
        thread.start()
        cmdline.cmdloop()

