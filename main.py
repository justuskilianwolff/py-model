from python_template.logging import get_logger
from python_template.utils import set_project_name

logger = get_logger(__name__, level="INFO")

logger.info("Hello, world!")


project_name = "my-project"

set_project_name(project_name)

logger.info(f"Project name is {project_name}")
