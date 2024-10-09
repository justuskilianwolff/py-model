import argparse

# setup argument parser
parser = argparse.ArgumentParser(description="Argument parser for for the py-model package.")

# add arguments
parser.add_argument("--dirs", "-d", nargs="*", type=str, help="Directories to search for model files.")
parser.add_argument("--files", "-f", nargs="*", type=str, help="Files to search for model files.")
parser.add_argument(
    "--output", "-o", type=str, default="", help="Output path of the result, if none specified it prints to stdout."
)
parser.add_argument(
    "--verbose", "-v", action="store_true", help="Increase verbosity of the output."
)  # TODO: actually implement this
