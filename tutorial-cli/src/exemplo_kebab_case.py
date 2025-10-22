import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--codigo-negociacao")
args = parser.parse_args()
print(args)
print(args.codigo_negociacao)
