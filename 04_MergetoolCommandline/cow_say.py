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

	def do_list_cows(self, arg):
		"""
		list_cows [dir]
		Lists all cow file names in the given directory or default cow list
		"""
		if arg:
			print(*cowsay.list_cows(shlex.split(arg)[0]))
		else:
			print(*cowsay.list_cows())

	def do_make_bubble(self, arg):
		'''
		make_buble [width [wrap_text [brackets ]]]
		This is the text that appears above the cows
		'''
		message, *options = shlex.split(arg)
		width = 40
		wrap_text = True
		brackets = cowsay.THOUGHT_OPTIONS['cowsay']
		if options:
			width = int(options[0]) if options[0] else width
			if len(options) > 1:
				wrap_text = bool(options[1] == 'True') if options[1] else wrap_text
				if len(options) > 2:
					brackets = options[2] if options[2] else brackets
		print(cowsay.make_bubble(message, brackets=brackets, width=width, wrap_text=wrap_text))

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
			cow = options[0] if options[0] else cow
			if len(options) > 1:
				eyes = options[1] if options[1] else eyes
				if len(options) > 2:
					tongue = options[2] if options[2] else tongue
		print(cowsay.cowsay(message, eyes=eyes, tongue=tongue, cow=cow))

	def do_cowthink(self, arg):
		'''
		cowthink message [cow [eyes [tongue]]]
		Display a message as cow thought
		'''
		message, *options = shlex.split(arg)
		print(options)
		cow = 'default'
		eyes = 'oo'
		tongue = '  '
		if options:
			cow = options[0] if options[0] else cow
			if len(options) > 1:
				eyes = options[1] if options[1] else eyes
				if len(options) > 2:
					tongue = options[2] if options[2] else tongue
		print(cowsay.cowthink(message, eyes=eyes, tongue=tongue, cow=cow))


if __name__ == "__main__":
	CowSayCmd().cmdloop()