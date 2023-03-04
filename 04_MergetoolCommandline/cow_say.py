import cmd


class CowSayCmd(cmd.Cmd):
	intro = "Say cow and enter!"
	prompt = "moo>"

	def do_exit(self, arg):
		'End command line'
		return True

if __name__ == "__main__":
	CowSayCmd().cmdloop()