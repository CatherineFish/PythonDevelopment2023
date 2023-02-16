import cowsay
import argparse
import sys

parser = argparse.ArgumentParser(
    description="Cow say something",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "-e",
    dest="eyes",
    action="store",
    default="oo",
    help="cow's eyes, first two chars wil be used",
    required=False,
)
parser.add_argument(
    "-f",
    dest="cowfile",
    action="store",
    default="",
    help="path to cowfile",
    required=False,
)
parser.add_argument(
    "-n",
    dest="is_wrap",
    action="store_true",
    help="the given message will not be word-wrapped",
    required=False,
)
parser.add_argument(
    "-T",
    dest="tongue",
    action="store",
    default="",
    help="cow's tongue, first two chars wil be used",
    required=False,
)
parser.add_argument(
    "-W",
    dest="wrap",
    action="store",
    default=40,
    help="where the message should be wrapped",
    required=False,
)

parser.add_argument(
    "-b",
    dest="apperance",
    action="append_const",
    const='b',
    default=[''],
    help="option initiates Borg mode",
    required=False,
)


parser.add_argument(
    "-d",
    dest="apperance",
    action="append_const",
    const='d',
    default=[''],
    help="causes the cow to appear dead",
    required=False,
)


parser.add_argument(
    "-g",
    dest="apperance",
    action="append_const",
    const='g',
    default=[''],
    help="invokes greedy mode",
    required=False,
)


parser.add_argument(
    "-p",
    dest="apperance",
    action="append_const",
    const='p',
    default=[''],
    help="causes a state of paranoia to come over the cow",
    required=False,
)


parser.add_argument(
    "-s",
    dest="apperance",
    action="append_const",
    const='s',
    default=[''],
    help="makes the cow appear thoroughly stoned",
    required=False,
)


parser.add_argument(
    "-t",
    dest="apperance",
    action="append_const",
    const='t',
    default=[''],
    help="yields a tired cow",
    required=False,
)


parser.add_argument(
    "-w",
    dest="apperance",
    action="append_const",
    const='w',
    default=[''],
    help="initiates wired mode",
    required=False,
)


parser.add_argument(
    "-y",
    dest="apperance",
    action="append_const",
    const='y',
    default=[''],
    help="brings on the cow's youthful appearance",
    required=False,
)

parser.add_argument(
    "-l",
    action="store_true",
    help="list of cows",
    required=False,
)

parser.add_argument("message", action="store", default="", help="what cow will say", nargs='?')

args = parser.parse_args(sys.argv[1:])
print(sys.argv)
if (not(len(args.message)) and args.l):
    print(cowsay.list_cows())
else: 
	print(
		cowsay.cowsay(
			args.message,
			eyes=args.eyes[0:2],
			preset=max(args.apperance),
			tongue=args.tongue[0:2],
			width=args.wrap,
			wrap_text=args.is_wrap,
		)
	)

