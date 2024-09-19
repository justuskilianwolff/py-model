from model_viz.logging import get_logger
from model_viz.navigation import get_filepath_set
from model_viz.parser import parser

args = parser.parse_args()

logger = get_logger(__name__, level="INFO")

# convert args to a dictionary
args_dict = vars(args)

# for testing purposes add dir
# args_dict["dirs"] = ["example_models/model_set_1"]

# get the file paths
filepaths = get_filepath_set(dirs=args_dict.get("dirs"), files=args_dict.get("files"))


for filepath in filepaths:
    logger.info(f"File path: {filepath}")
