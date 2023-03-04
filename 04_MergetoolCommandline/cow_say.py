import cmd


class CowSayCmd(cmd.Cmd):
	intro = "Say cow and enter!"
	prompt = "moo>"

if __name__ == "__main__":
	CowSayCmd().cmdloop()