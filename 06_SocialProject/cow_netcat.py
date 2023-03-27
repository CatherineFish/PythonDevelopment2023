import cmd
import threading
import readline
import shlex
import socket
import sys
import select


HOST = '0.0.0.0'
PORT = 1337  
s = None
    

def write(message):
    s.send(f"{message}\n".encode())

def get_message(timeout):
    try:
        event, *trash = select.select([s], [], [], timeout)
        for sock in event:
            return sock.recv(1024).decode().strip()
        return ""
    except ValueError:
        sys.exit(0)
    

def recive_messages(cmdline, locker):
    while True:
        with locker:
            data = get_message(0)
        if data:
            print(f'\n{data}\n{cmdline.prompt}{readline.get_line_buffer()}', end="", flush=True)


class CowNetcat(cmd.Cmd):

    def __init__(self, locker):
        super(CowNetcat, self).__init__()
        self.locker = locker
        
    def do_who(self, arg):
        """
        who
        Lists all registered users
        """
        write("who")

    def do_cows(self, arg):
        """
        cows
        Lists all possible cow login name
        """
        write("cows")

    def do_login(self, arg):
        """
        login your_login
        Register with <yur_login> name
        """
        login, *trash = shlex.split(arg)
        write(f"login {login}")
        self.my_log = login

    def complete_login(self, text, line, begidx, endidx):
        current_args = shlex.split(line)
        args_len = len(current_args)
        if args_len <= 2:
            with self.locker:
                write(f"cows\n")
                data = get_message(timeout=None)
                cows = list(map(lambda x: x.replace("'", "").strip(), data[1:-1].split(",")))
                return [s for s in cows if s.startswith(text)] 

    def do_say(self, arg):
        """
        say user_login message
        Send <message> to <user_login>
        """
        cow_name, message, *trash = shlex.split(arg)
        write(f"say {cow_name} {message}")

    def complete_say(self, text, line, begidx, endidx):
        current_args = shlex.split(line)
        args_len = len(current_args)
        if args_len <= 2:
            with self.locker:
                write(f"who\n")
                data = get_message(timeout=None)
                cows = list(map(lambda x: x.replace("'", "").strip(), data[18:].split(",")))
                return [res for res in cows if res.startswith(text) and res != self.my_log] 

    def do_yield(self, arg):
        """
        yield message
        Send <message> to everyone
        """
        message, *trash = shlex.split(arg)
        write(f"yield {message}")

    def do_quit(self, args):
        """
        quit
        Disconnect from chat
        """
        write(f"quit")
        sys.exit(0)


if __name__ == "__main__":
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
        cmdline = CowNetcat(locker)
        thread = threading.Thread(target=recive_messages, args=(cmdline, locker))
        thread.start()
        cmdline.cmdloop()

