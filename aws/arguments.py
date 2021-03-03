import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--environment', '-e',
    type=str,
    required=True,
)
parser.add_argument(
    '--region', '-r',
    type=str,
    required=True,
)
parser.add_argument(
    '--branch', '-b',
    action='store',
)
parser.add_argument(
    '--suffix',
    type=str,
    required=True,
)
parser.add_argument(
    '--amitype',
    type=str,
    required=True,
)
parser.add_argument(
    '--replace',
    dest='replace',
    action='store_true'
)
parser.add_argument(
    '--no-replace',
    dest='replace',
    action='store_false'
)
parser.set_defaults(replace=False)
args = parser.parse_args()
