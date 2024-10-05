from py_model.logging import get_logger
from py_model.navigation import get_classes, get_filepath_set
from py_model.parser import parser
from py_model.parsing import Class


def main():
    args = parser.parse_args()

    logger = get_logger(__name__, level="DEBUG")

    # convert args to a dictionary
    args_dict = vars(args)

    # get the file paths
    filepaths = get_filepath_set(dirs=args_dict.get("dirs"), files=args_dict.get("files"))

    class_instances: list[Class] = list()

    for filepath in sorted(filepaths):
        logger.info(f"File path: {filepath}")
        classes = get_classes(filepath)

        # create class instances
        for cls in classes:
            class_instance = Class.from_ast(cls)
            class_instances.append(class_instance)

    # convert to list
    for class_instance in class_instances:
        print(class_instance)


if __name__ == "__main__":
    main()
