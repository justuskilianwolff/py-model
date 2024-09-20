from model_viz.logging import get_logger
from model_viz.navigation import get_classes, get_filepath_set
from model_viz.parser import parser
from model_viz.types.class_instance import ClassInstance

args = parser.parse_args()

logger = get_logger(__name__, level="ERROR")

# convert args to a dictionary
args_dict = vars(args)

# for testing purposes add dir
args_dict["dirs"] = ["example_models/model_set_1"]

# get the file paths
filepaths = get_filepath_set(dirs=args_dict.get("dirs"), files=args_dict.get("files"))


class_instances: list[ClassInstance] = list()

for filepath in sorted(filepaths):
    logger.info(f"File path: {filepath}")
    classes = get_classes(filepath)

    # create class instances
    for cls in classes:
        class_instance = ClassInstance(cls=cls, filepath=filepath)
        class_instances.append(class_instance)


# convert to list
for class_instance in class_instances:
    print(class_instance)

# joined_attributes = []
# class_names = []
# for cls in class_instances:
#     for attr in cls.attributes:
#         joined_attributes.append(attr)
#         class_names.append(cls.class_name)

# print(joined_attributes)

# for cls_name, attr in zip(class_names, joined_attributes):
#     print(cls_name + " " + get_attr_repr(attr))
