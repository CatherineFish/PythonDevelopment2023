import cmd
import cowsay
import shlex
import readline


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

	def do_cowsay(self, arg):
		'''
		cowsay message [cow [eyes [tongue]]]
		Display a message as cow phrases
		'''
		message, *options = shlex.split(arg)
		cow = 'default'
		eyes = 'oo'
		tongue = '  '
		if options:
			cow = options[0]
			if len(options) > 1:
				eyes = options[1]
				if len(options) > 2:
					tongue = options[2]
		print(cowsay.cowsay(message, eyes=eyes, tongue=tongue, cow=cow))

	def do_cowthink(self, text):
		'Display a message as cow thought'
		print(cowsay.cowthink(text))


if __name__ == "__main__":
	CowSayCmd().cmdloop()