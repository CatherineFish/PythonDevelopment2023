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
    


class CowNetcat(cmd.Cmd):

    def __init__(self, socket):
        super(CowNetcat, self).__init__()
        self.sock = socket
        self.buffer_for_cows = []
        self.buffer_for_who = []
        
    def do_who(self, arg):
        write(f"0 who", self.sock)


    def do_cows(self, arg):
        write(f"0 cows", self.sock)

    def do_login(self, arg):
        login, *trash = shlex.split(arg)
        write(f"0 login {login}", self.sock)

    def complete_login(self, text, line, begidx, endidx):
        current_args = shlex.split(line)
        args_len = len(current_args)
        if args_len <= 2:
            write(f"1 cows", self.sock)
    
            return [res for res in recive_messages(self.sock) if res.startwith(text.lower())]


    def do_say(self, arg):
        cow_name, message, *trash = shlex.split(arg)
        write(f"0 say {cow_name} {message}", self.sock)

    def do_yield(self, arg):
        message, *trash = shlex.split(arg)
        write(f"0 yield {message}", self.sock)

    def do_quit(self, arg):
        write(f"0 quit", self.sock)


    def recive_messages(self):
        while True:
            data = self.soc.recv(1024).decode().strip()
            number = shlex.split(data)[0]
            if int(number) == 1:
                self.buffer_for_cows = data[1:]
                break
            elif int(number) == 2:
                self.buffer_for_who = data[1:]
                break
            if not(data):
                break
            print(f'RESULT {data}\n{cmdline.prompt}{readline.get_line_buffer()}', end="", flush=True)

        

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
        thread = threading.Thread(target=recive_messages, args=(s,))
        thread.start()
        cmdline.cmdloop()

