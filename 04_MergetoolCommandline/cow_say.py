import cmd
import cowsay
import shlex
import readline


def complete_cowsay(text, line, begidx, endidx):
	current_args = shlex.split(line)
	args_len = len(current_args)
	default_eyes = ["OO", "XX", "PP", "ZZ", "FF", "AO", "AB"]
	default_tongue = ["II", "MN", "QK", "DF", "DK", "UU"]
	if (text == current_args[-1]):
		if args_len == 3:
			return [c for c in cowsay.list_cows() if c.startswith(text)]
		if args_len == 4:
			return [c for c in default_eyes if c.startswith(text)]
		if args_len == 5:
			return [c for c in default_tongue if c.startswith(text)]
	else:
		if args_len == 2:
			return [c for c in cowsay.list_cows() if c.startswith(text)]
		if args_len == 3:
			return [c for c in default_eyes if c.startswith(text)]
		if args_len == 4:
			return [c for c in default_tongue if c.startswith(text)]


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
		make_buble [wrap_text [width [brackets ]]]
		This is the text that appears above the cows
		'''
		message, *options = shlex.split(arg)
		wrap_text = True
		width = 40
		brackets = cowsay.THOUGHT_OPTIONS['cowsay']
		if options:
			wrap_text = bool(options[0] == 'True') if options[0] else wrap_text
			if len(options) > 1:
				width = int(options[1]) if options[1] else width
				if len(options) > 2:
					brackets = options[2] if options[2] else brackets
		print(cowsay.make_bubble(message, brackets=brackets, width=width, wrap_text=wrap_text))


	def complete_make_bubble(self, text, line, begidx, endidx):
		current_args = shlex.split(line)
		args_len = len(current_args)
		
		if ((args_len == 2 and current_args[-1] != text) or 
			(args_len == 3 and current_args[-1] == text)):
			wrap_options = ['True', 'False']
			return [res for res in wrap_options if res.lower().startswith(text.lower())]


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


	def complete_cowsay(self, text, line, begidx, endidx):
		return complete_cowsay(text, line, begidx, endidx)


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


	def complete_cowthink(self, text, line, begidx, endidx):
		return complete_cowsay(text, line, begidx, endidx)


if __name__ == "__main__":
	CowSayCmd().cmdloop()