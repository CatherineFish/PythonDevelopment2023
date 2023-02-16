from cowsay import cowsay
import argparse

parser = argparse.ArgumentParser(description='Cow say something', prog='PROG',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-e', dest='eyes', action='store_const',
                    const='oo', default='oo',
                    help="cow's eyes, first two chars wil be used", required=False)
parser.add_argument('-f', dest='cowfile', action='store_const',
                    const='', default='',
                    help="path to cowfile", required=False)
parser.add_argument('-n', action='store_true',
                    help="the given message will not be word-wrapped", required=False)
parser.add_argument('-T', dest='tongue', action='store_const',
                    const='', default='',
                    help="cow's tongue, first two chars wil be used", required=False)
parser.add_argument('-W', dest='wrap', action='store_const',
                    const=40, default=40,
                    help="where the message should be wrapped", required=False)
parser.add_argument('message', action='store_const',
                    const="", default="",
                    help="what cow will say")

args = parser.parse_args()


print(args)