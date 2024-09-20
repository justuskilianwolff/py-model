from model_viz.logging import get_logger

logger = get_logger(__name__)


# def get_attr_repr(attribute: ast.AnnAssign | ast.Assign, type: bool = True) -> str:
#     """
#     Return a string representation of an attribute.

#     Args:
#         attribute (ast.AnnAssign | ast.Assign): The attribute to print.

#     Returns:
#         str: The string representation of the attribute.
#     """
#     if isinstance(attribute, ast.Assign):
#         attribute_str = indicate_access_level(attribute.value.id)
#     elif isinstance(attribute, ast.AnnAssign):
#         attribute_str = indicate_access_level(attribute.target.id)
#         if type:
#             if isinstance(attribute.annotation, ast.Name):
#                 attribute_str += f": {attribute.annotation.id}"
#             else:
#                 attribute_str += ": not implemented"
#                 logger.warning(f"Unknown attribute type for attribute: {attribute.target.id}")
#     else:
#         raise NotImplementedError()

#     return attribute_str
