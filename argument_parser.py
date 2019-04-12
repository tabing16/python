import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--reg", nargs='+', type=str, action='append', required=True,
                    help="channel number and unit of measure")
parser.add_argument("-m", "--meter", nargs='+', type=str, required=True)
parser.add_argument("-f", "--from", nargs='+', type=str, required=True, help="start period of the reading")
parser.add_argument("-t", "--to", nargs='+', type=str, required=True, help="end period of the reading")

args = parser.parse_args()

# print(len(args.reg))

print(args.reg)

print(args.meter)

