import cmd
import cowsay


class CowSayCmd(cmd.Cmd):
	intro = "Say cow and enter!"
	prompt = "moo>"

	def do_exit(self, arg):
		'End command line'
		return True

	def do_list_cows(self, directory=""):
		'Lists all cow file names in the given directory'
		if directory:
			print(cowsay.list_cows(directory))
		else:
			print(cowsay.list_cows())

	def do_make_bubble(self, text):
		'This is the text that appears above the cows'
		print(cowsay.make_bubble(text))

	def do_cowsay(self, text):
		'Display a message as cow phrases'
		print(cowsay.cowsay(text))

	def do_cowthink(self, text):
		'Display a message as cow thought'
		print(cowsay.cowthink(text))


if __name__ == "__main__":
	CowSayCmd().cmdloop()