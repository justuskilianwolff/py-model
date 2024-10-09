import os

from py_model.logging import get_logger
from py_model.navigation import get_classes, get_filepath_set
from py_model.parser import parser
from py_model.parsing import Class
from py_model.writing import SupportedTypes


def main():
    args = parser.parse_args()
    # convert args to a dictionary
    args_dict = vars(args)

    # get verbosity level -> other loggers inherit from this one
    if args_dict['verbose']:
        logger = get_logger(__name__, level="INFO")
    else:
        logger = get_logger(__name__, level="WARNING")

    # get the file paths
    filepaths = get_filepath_set(dirs=args_dict.get("dirs"), files=args_dict.get("files"))

    class_instances: list[Class] = list()

    for filepath in sorted(filepaths):
        classes = get_classes(filepath)

        # create class instances
        for cls in classes:
            class_instance = Class.from_ast(cls)
            class_instances.append(class_instance)

    # create the result string
    result = ""
    # obtain desired output type
    output_file = args_dict.get("output")

    if (output_file is None) or (output_file == parser.get_default("output")):
        # print to stdout
        for class_instance in class_instances:
            result += str(class_instances)

        print(result)
    else:
        _, ext = os.path.splitext(output_file)
        if ext == ".dot":
            supported_dtype = SupportedTypes.dot
        elif ext == ".ts":
            supported_dtype = SupportedTypes.ts

        for class_instance in class_instances:
            result += class_instance.get_string(supported_type=supported_dtype)

        # write file
        with open(output_file, "wt") as f:
            f.write(result)


if __name__ == "__main__":
    main()
