import argparse

from model_viz.logging import get_logger

logger = get_logger(__name__, level="INFO")


# setup argument parser
parser = argparse.ArgumentParser(description="Argument parser for for the model-viz package.")

# add arguments
parser.add_argument("--dirs", "-d", nargs="?", type=str, default=["src"], help="Directories to search for model files.")
parser.add_argument("--files", "-f", nargs="?", type=str, help="Files to search for model files.")
parser.add_argument(
    "--output", "-o", type=str, default="model-viz.dot", help="Output file to save the visualization file."
)
parser.add_argument("--verbose", "-v", action="store_true", help="Increase verbosity of the output.")

# parse arguments
args = parser.parse_args()
print(args)