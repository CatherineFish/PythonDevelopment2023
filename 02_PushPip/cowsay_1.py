from cowsay import cowsay
import argparse
import sys

parser = argparse.ArgumentParser(description='Cow say something',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-e', dest='eyes', action='store', default='oo', help="cow's eyes, first two chars wil be used", required=False)
parser.add_argument('-f', dest='cowfile', action='store',
                     default='',
                    help="path to cowfile", required=False)
parser.add_argument('-n', dest='is_wrap', action='store_true',
                    help="the given message will not be word-wrapped", required=False)
parser.add_argument('-T', dest='tongue', action='store',
                    default='',
                    help="cow's tongue, first two chars wil be used", required=False)
parser.add_argument('-W', dest='wrap', action='store',
                    default=40,
                    help="where the message should be wrapped", required=False)
parser.add_argument('message', action='store',
                     default="",
                    help="what cow will say")

print(args)